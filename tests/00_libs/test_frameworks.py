# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# TODO: add yaml validation tests (per json schema?)

import copy
import pytest
from collections import OrderedDict

from ruamel.yaml.compat import ordereddict
from ruamel.yaml.comments import CommentedOrderedMap
from ruamel import yaml

from mathmaker.lib.tools.frameworks import list_all_sheets
from mathmaker.lib.tools.frameworks import _AttrStr
from mathmaker.lib.tools.frameworks import load_sheet, read_layout
from mathmaker.lib.tools.frameworks import _read_simple_question
from mathmaker.lib.tools.frameworks import _read_mix_question, _read_mix_nb
from mathmaker.lib.tools.frameworks import _get_attributes, _dissolve_block
from mathmaker.lib.tools.frameworks import _expand_alternatives
from mathmaker.lib.constants import MIN_ROW_HEIGHT, DEFAULT_LAYOUT


def test_AttrStr_parse_warnings():
    """Check parse() raises proper warnings in proper cases."""
    with pytest.warns(None) as record:
        _AttrStr('').parse()
    assert len(record) == 0
    with pytest.warns(UserWarning) as record:
        _AttrStr('rowxcol=?×2,  , spacing=').parse()
    assert len(record) == 1
    assert str(record[0].message) == "Ignoring malformed attributes' string" \
        " (missing =, or empty space between two commas) " \
        "in 'rowxcol=?×2,  , spacing='."


def test_AttrStr_parse():
    """Check parse() in various cases."""
    assert _AttrStr('').parse() == {}
    with pytest.warns(UserWarning):
        assert _AttrStr('rowxcol=?×2,  , spacing=25.0pt').parse() \
            == {'rowxcol': '?×2', 'spacing': '25.0pt'}
        assert _AttrStr('rowxcol=?×2,  , spacing=').parse() \
            == {'rowxcol': '?×2', 'spacing': ''}
    assert _AttrStr('rowxcol=?×2').parse() == {'rowxcol': '?×2'}
    assert _AttrStr('spacing=').parse() == {'spacing': ''}
    assert _AttrStr('rowxcol=?×2,  print=3 3, spacing=').parse() \
        == {'rowxcol': '?×2', 'print': '3 3', 'spacing': ''}
    assert _AttrStr('source=singleint_2to100;;intpairs_2to9, '
                    'variant=2,3,6,7, required=true, ').parse() \
        == {'source': 'singleint_2to100;;intpairs_2to9', 'variant': '2,3,6,7',
            'required': 'true'}


def test_AttrStr_split_clever_exceptions():
    """Check split_clever() raises proper exceptions."""
    with pytest.raises(ValueError) as excinfo:
        _AttrStr('newpage=true, rowxcol=?×2, print=3 3, spacing=') \
            .split_clever('wordings')
    assert 'cannot start with a newpage' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        _AttrStr('print=2, print=1, newpage=true,') \
            .split_clever('answers')
    assert 'same keyword cannot show up several times' in str(excinfo.value)


def test_AttrStr_split_clever():
    """Check split_clever() in various cases."""
    assert _AttrStr('').split_clever('wordings') == [{}]
    assert _AttrStr('rowxcol=?×2, print=3 3, spacing=') \
        .split_clever('wordings') \
        == [{'wordings': 'rowxcol=?×2, print=3 3, spacing='}]
    assert _AttrStr('print=2, newpage=true, print=1') \
        .split_clever('answers') \
        == [{'answers': 'print=2, newpage=true'},
            {'answers': 'print=1'}]
    assert _AttrStr('print=2, rowxcol=?×2, print=3 3') \
        .split_clever('answers') \
        == [{'answers': 'print=2'},
            {'answers': 'rowxcol=?×2, print=3 3'}]


def test_AttrStr_fetch_exception():
    """Test fetch() raises exception for inexisting attribute."""
    with pytest.raises(KeyError) as excinfo:
        _AttrStr('attr1=value 1, picky=7, attr3=valZ').fetch('pick')
    assert str(excinfo.value) == \
        '"Cannot find the attribute \'pick\' in string ' \
        '\'attr1=value 1, picky=7, attr3=valZ\'."'


def test_AttrStr_fetch():
    """Test fetching the value of an attribute from a string."""
    assert _AttrStr('attr1=value 1, pick=7, attr3=valZ').fetch('pick') \
        == '7'
    assert _AttrStr('attr1=value 1, attr3=valZ, pick=7,').fetch('pick') \
        == '7'


def test_AttrStr_remove():
    """Test removing attribute from a string."""
    assert _AttrStr('attr1=value 1, pick=7, attr3=valZ').remove('pick') \
        == 'attr1=value 1, attr3=valZ'


def test_list_all_sheets():
    """Check listing of sheets happens without errors."""
    assert isinstance(list_all_sheets(), str)


def test_read_layout():
    """Check layout is correctly loaded from formatted strings in dict."""
    assert read_layout({}) == DEFAULT_LAYOUT
    default = copy.deepcopy(DEFAULT_LAYOUT)
    default.update({'any attribute': 'any value'})
    assert read_layout({'any attribute': 'any value'}) == default
    layout_data = {'wordings': 'rowxcol=?×2,  print=5 5, spacing=25.0pt',
                   'answers': 'rowxcol=?×2,  print=5 5'}
    assert read_layout(layout_data) == \
        {'exc': [['?', 9, 9], (5, 5)], 'ans': [['?', 9, 9], (5, 5)],
         'spacing_w': '25.0pt', 'spacing_a': 'undefined',
         'min_row_height': MIN_ROW_HEIGHT}
    layout_data = [layout_data]
    assert read_layout(layout_data) == \
        {'exc': [['?', 9, 9], (5, 5)], 'ans': [['?', 9, 9], (5, 5)],
         'spacing_w': '25.0pt', 'spacing_a': 'undefined',
         'min_row_height': MIN_ROW_HEIGHT}
    layout_data = {'wordings': 'rowxcol=?×2,  print=3 3, spacing=25.0pt',
                   'answers': 'rowxcol=?×2,  print=3 3, spacing='}
    assert read_layout(layout_data) == \
        {'exc': [['?', 9, 9], (3, 3)], 'ans': [['?', 9, 9], (3, 3)],
         'spacing_w': '25.0pt', 'spacing_a': '',
         'min_row_height': MIN_ROW_HEIGHT}
    layout_data = {'answers': 'print=2, newpage=true, print=1'}
    assert read_layout(layout_data) == \
        {'exc': [None, 'all'],
         'ans': [None, 2, 'jump', 'next_page', None, 1],
         'spacing_w': 'undefined', 'spacing_a': 'undefined',
         'min_row_height': MIN_ROW_HEIGHT}
    layout_data = {'wordings': 'rowxcol=3×2,  print=1 1 . 2 2 . 1 1, spacing='}
    assert read_layout(layout_data) == \
        {'exc': [[3, 9, 9], (1, 1, 2, 2, 1, 1)], 'ans': [None, 'all'],
         'spacing_w': '', 'spacing_a': 'undefined',
         'min_row_height': MIN_ROW_HEIGHT}
    layout_data = {'wordings': 'rowxcol=3×2,  print=1 1 / 2 2 / 1 1, spacing='}
    assert read_layout(layout_data) == \
        {'exc': [[3, 9, 9], (1, 1, 2, 2, 1, 1)], 'ans': [None, 'all'],
         'spacing_w': '', 'spacing_a': 'undefined',
         'min_row_height': MIN_ROW_HEIGHT}


def test_load_sheet_exceptions():
    """Test wrong theme, subtheme, sheet name do raise an exception."""
    with pytest.raises(IOError) as excinfo:
        load_sheet('dumbtheme', '', '')
    assert str(excinfo.value) == 'Could not find the provided theme ' \
        '(dumbtheme) among the frameworks.'
    with pytest.raises(IOError) as excinfo:
        load_sheet('algebra', 'dumbsubtheme', '')
    assert str(excinfo.value) == 'Could not find the provided subtheme ' \
        '(dumbsubtheme) in the provided theme (algebra).'
    with pytest.raises(ValueError) as excinfo:
        load_sheet('algebra', 'expand', 'dumbsheetname')
    assert str(excinfo.value) == 'No sheet of this name (dumbsheetname) in ' \
        'the provided theme and subtheme (algebra, expand).'


def test_load_sheet():
    """Test right theme, subtheme, sheet name return the right data."""
    d = load_sheet('algebra', 'expand', 'double')
    assert isinstance(d, OrderedDict)
    assert isinstance(d, ordereddict)
    assert isinstance(d, CommentedOrderedMap)
    assert d == ordereddict([
        ('title',
         'Algebra: expand and reduce double brackets'),
        ('exercise',
         ordereddict([('details_level', 'medium'),
                      ('text_exc',
                       'Expand and reduce the following '
                       'expressions:'),
                      ('text_ans', 'Example of solutions:'),
                      ('questions',
                       'expand double -> intpairs_2to9;;intpairs_2to9 (5)')
                      ]))])


def test__expand_alternatives():
    """Test alternatives are correctly replaced by one value."""
    assert _expand_alternatives(
        'percent direct '
        '-> percents_{quarters|tenths|twentieths|ntenths} (20)') \
        == ['percent direct -> percents_quarters (20)',
            'percent direct -> percents_tenths (20)',
            'percent direct -> percents_twentieths (20)',
            'percent direct -> percents_ntenths (20)']
    assert _expand_alternatives(
        'percent {direct|reversed} '
        '-> percents_{quarters|tenths|twentieths|ntenths} (20)') \
        == ['percent direct -> percents_quarters (20)',
            'percent direct -> percents_tenths (20)',
            'percent direct -> percents_twentieths (20)',
            'percent direct -> percents_ntenths (20)',
            'percent reversed -> percents_quarters (20)',
            'percent reversed -> percents_tenths (20)',
            'percent reversed -> percents_twentieths (20)',
            'percent reversed -> percents_ntenths (20)']


def test__dissolve_block_exceptions():
    """Test _dissolve_block() raises an exception when appropriate."""
    q_block = ['7', 'fourth id, attr4=some value, attr4=yet another value '
                    '-> label_4 (1)\n'
                    'fifth id -> label_5, attr=7.5pt (1)\n'
                    'sixth id, attr5=random value -> label_6 (1)']
    with pytest.raises(ValueError) as excinfo:
        _dissolve_block(q_block)
    assert str(excinfo.value) == 'YAML File Format error: there are more ' \
        'questions to create (7) than available (3).'


def test__dissolve_block():
    """Test a block is correctly dissolved into a list of questions"""
    q_block = ['3', 'fourth id, attr4=some value, attr4=yet another value '
                    '-> label_4 (2)\n'
                    'fifth id -> label_5, attr=7.5pt (4)\n'
                    'sixth id, attr5=random value -> label_6 (7)']
    result = _dissolve_block(q_block)
    assert type(result) == list
    assert len(result) == 3
    # assert result == []
    assert all([r in ['fourth id, attr4=some value, attr4=yet another value '
                      '-> label_4 (1)',
                      'fifth id -> label_5, attr=7.5pt (1)',
                      'sixth id, attr5=random value -> label_6 (1)']
                for r in result])


def test__read_simple_question_exceptions():
    """Test malformed simple questions raise the right exceptions."""
    with pytest.raises(ValueError) as excinfo:
        _read_simple_question(' -> intpairs_2to9;;intpairs_2to9 (5)')
    assert 'missing question\'s name' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        _read_simple_question('expand double -> '
                              'intpairs_2to9;;intpairs_2to9 5)')
    assert 'are not built correctly' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        _read_simple_question('expand double ->> (5)')
    assert 'incorrect numbers\' source:' in str(excinfo.value)


def test__read_simple_question():
    """Test simple questions are read correctly."""
    assert _read_simple_question(
        'expand double -> intpairs_2to9;;intpairs_2to9 (5)') == \
        [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 5]]
    assert _read_simple_question(
        'expand double -> intpairs_2to9;;intpairs_2to9 (3) '
        'expand double -> intpairs_10to20;;intpairs_2to9 (7)') == \
        [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 3],
         [{'id': 'expand double'}, ['intpairs_10to20', 'intpairs_2to9'], 7]]
    assert _read_simple_question(
        'expand double -> intpairs_2to9;;intpairs_2to9 (3) '
        '              -> intpairs_10to20;;intpairs_2to9 (7)') == \
        [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 3],
         [{'id': 'expand double'}, ['intpairs_10to20', 'intpairs_2to9'], 7]]
    assert _read_simple_question(
        'expand double -> intpairs_2to9;;intpairs_2to9 (3) '
        '              -> intpairs_10to20;;intpairs_2to9 (7)'
        'expand simple -> intpairs_2to9;;intpairs_2to9 (10)') == \
        [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 3],
         [{'id': 'expand double'}, ['intpairs_10to20', 'intpairs_2to9'], 7],
         [{'id': 'expand simple'}, ['intpairs_2to9', 'intpairs_2to9'], 10]]
    assert _read_simple_question(
        'expand double, spacing=10.0pt -> intpairs_2to9;;intpairs_2to9 (1)') \
        == [[{'id': 'expand double', 'spacing': '10.0pt'},
             ['intpairs_2to9', 'intpairs_2to9'], 1]]
    assert _read_simple_question(
        'expand double, variant=anything -> intpairs_2to9;;intpairs_2to9 (3) '
        '              -> intpairs_10to20;;intpairs_2to9 (7)') == \
        [[{'id': 'expand double', 'variant': 'anything'},
          ['intpairs_2to9', 'intpairs_2to9'], 3],
         [{'id': 'expand double', 'variant': 'anything'},
          ['intpairs_10to20', 'intpairs_2to9'], 7]]
    assert _read_simple_question(
        'subtr direct, subvariant=only_positive'
        ' -> intpairs_2to9, complement=10 (2)') == \
        [[{'id': 'subtr direct', 'subvariant': 'only_positive',
           'complement': '10', },
          ['intpairs_2to9'], 2]
         ]
    assert _read_simple_question('multi direct -> intpairs_2to9×4to9 (6)') == \
        [[{'id': 'multi direct'},
          ['intpairs_2to9×4to9'], 6]
         ]
    example_with_block = _read_simple_question(
        """first id, attr1=a value, attr2=value 2 -> label_1 (5)
        second id -> label_2, attr=5.0pt (12)
        third id, attr3=random value -> label_3 (1)
        [3][fourth id, attr4=some value, attr4=yet another value -> label_4 (2)
            fifth id -> label_5, attr=7.5pt (4)
            sixth id, attr5=random value -> label_6 (7)]
        seventh id, attr4=some value, attr4=yet another value -> label_4 (2)
        eighth id -> label_5, attr=7.5pt (4)
        yet another id, attr5=random value -> label_6 (7)"""
    )
    assert example_with_block[:3] == \
        [[{'attr1': 'a value', 'attr2': 'value 2', 'id': 'first id'},
          ['label_1'], 5],
         [{'attr': '5.0pt', 'id': 'second id'}, ['label_2'], 12],
         [{'attr3': 'random value', 'id': 'third id'}, ['label_3'], 1],
         ]
    # assert example_with_block == []
    assert \
        all([q in [[{'attr5': 'random value', 'id': 'sixth id'},
                    ['label_6'], 1],
                   [{'attr': '7.5pt', 'id': 'fifth id'}, ['label_5'], 1],
                   [{'attr4': 'yet another value', 'id': 'fourth id'},
                    ['label_4'], 1]]
             for q in example_with_block[3:-3]])
    assert example_with_block[-3:] == \
        [[{'attr4': 'yet another value', 'id': 'seventh id'}, ['label_4'], 2],
         [{'attr': '7.5pt', 'id': 'eighth id'}, ['label_5'], 4],
         [{'attr5': 'random value', 'id': 'yet another id'}, ['label_6'], 7],
         ]
    assert _read_simple_question(
        'percent direct '
        '-> percents_{quarters|tenths|twentieths|ntenths} (20)')[0][1][0] \
        in ['percents_quarters', 'percents_tenths', 'percents_twentieths',
            'percents_ntenths']
    example_with_block = _read_simple_question(
        """[2][q id1, attr1={val1|val2} -> source1 (2)
            q id2 -> source2 (1)]"""
    )
    assert ([{'attr1': 'val1', 'id': 'q id1'}, ['source1'], 1]
            in example_with_block
            or [{'attr1': 'val2', 'id': 'q id1'}, ['source1'], 1]
            in example_with_block)
    example_with_block = _read_simple_question(
        """[2][{q id1|q id3} -> source1 (2)
            q id2 -> source2 (1)]"""
    )
    assert ([{'id': 'q id1'}, ['source1'], 1]
            in example_with_block
            or [{'id': 'q id3'}, ['source1'], 1]
            in example_with_block)
    example_with_block = _read_simple_question(
        """[2][{q id1} -> {source1|source2} (2)
            q id2 -> source2 (1)]"""
    )
    assert ([{'id': 'q id1'}, ['source1'], 1]
            in example_with_block
            or [{'id': 'q id1'}, ['source2'], 1]
            in example_with_block)


def test__read_mix_question():
    """Test mix questions are read correctly."""
    assert _read_mix_question(
        'q id1, attr1=val1, attr2=value 2, q id2, attr1=val1, attr3=val3, '
        'pick=3, q id3') == \
        [{'id': 'q id1', 'attr1': 'val1', 'attr2': 'value 2'},
         {'id': 'q id2', 'attr1': 'val1', 'attr3': 'val3'},
         {'id': 'q id2', 'attr1': 'val1', 'attr3': 'val3'},
         {'id': 'q id2', 'attr1': 'val1', 'attr3': 'val3'},
         {'id': 'q id3'}]
    assert _read_mix_question(
        'calculation order_of_operations, subvariant=only_positive, '
        'spacing=15.0pt') == \
        [{'id': 'calculation order_of_operations',
          'subvariant': 'only_positive', 'spacing': '15.0pt'}]


def test__read_mix_nb():
    """Test mix numbers' sources are read correctly."""
    assert _read_mix_nb('singleint_2to100;;intpairs_2to9, variant=2,3,6,7,'
                        ' required=true (1)') == \
        [[['singleint_2to100;;intpairs_2to9'],
          {'source': 'singleint_2to100;;intpairs_2to9',
           'variant': '2,3,6,7',
           'required': 'true'},
          1]]
    assert _read_mix_nb(' singleint_2to100;;intpairs_2to9 , variant=2,3,6,7,'
                        ' required=true (1) ') == \
        [[['singleint_2to100;;intpairs_2to9'],
          {'source': 'singleint_2to100;;intpairs_2to9',
           'variant': '2,3,6,7',
           'required': 'true'},
          1]]
    assert _read_mix_nb('singleint_2to100;;intpairs_2to9, variant=2,3,6,7,'
                        ' required=true (3)') == \
        [[['singleint_2to100;;intpairs_2to9'],
          {'source': 'singleint_2to100;;intpairs_2to9',
           'variant': '2,3,6,7',
           'required': 'true'},
          1],
         [['singleint_2to100;;intpairs_2to9'],
          {'source': 'singleint_2to100;;intpairs_2to9',
           'variant': '2,3,6,7',
           'required': 'true'},
          1],
         [['singleint_2to100;;intpairs_2to9'],
          {'source': 'singleint_2to100;;intpairs_2to9',
           'variant': '2,3,6,7',
           'required': 'true'},
          1]]
    assert _read_mix_nb('singleint_2to100;;intpairs_2to9, variant=2,3,6,7, '
                        'required=true (1)'
                        'singleint_3to12;;intpairs_2to9, variant=8-23,100-187,'
                        ' (2)') == \
        [[['singleint_2to100;;intpairs_2to9'],
          {'source': 'singleint_2to100;;intpairs_2to9',
           'variant': '2,3,6,7',
           'required': 'true'},
          1],
         [['singleint_3to12;;intpairs_2to9'],
          {'source': 'singleint_3to12;;intpairs_2to9',
           'variant': '8-23,100-187'},
          1],
         [['singleint_3to12;;intpairs_2to9'],
          {'source': 'singleint_3to12;;intpairs_2to9',
           'variant': '8-23,100-187'},
          1]]


def test_get_attributes():
    data = """
wording1:
  - wording_context: marbles
  - wording: "{name1} has {nb1} marbles... ?"
  - nb1_min: 2
  - nb1_max: 1000
  - nb2_min: 2
  - nb2_max: 1000
  - q_id: "addi_direct"

wording2:
  - wording_context: "golden goose"
  - wording: "Yesterday, my golden goose laid ...?"
  - nb1_min: 2
  - nb1_max: 100
  - nb2_min: 2
  - nb2_max: 100
  - q_id: "addi_direct"
"""
    assert _get_attributes(yaml.safe_load(data), 'wording') == \
        [{'wording_context': 'marbles',
          'wording': '{name1} has {nb1} marbles... ?',
          'nb1_min': 2,
          'nb1_max': 1000,
          'nb2_min': 2,
          'nb2_max': 1000,
          'q_id': 'addi_direct',
          },
         {'wording_context': 'golden goose',
          'wording': 'Yesterday, my golden goose laid ...?',
          'nb1_min': 2,
          'nb1_max': 100,
          'nb2_min': 2,
          'nb2_max': 100,
          'q_id': 'addi_direct',
          }]
