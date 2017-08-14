# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

import pytest
from collections import OrderedDict

from ruamel.yaml.compat import ordereddict
from ruamel.yaml.comments import CommentedOrderedMap

from mathmaker.lib.tools.frameworks import _AttrStr
from mathmaker.lib.tools.frameworks import load_sheet, read_layout
from mathmaker.lib.tools.frameworks import _read_simple_question
from mathmaker.lib.tools.frameworks import _read_mix_question, _read_mix_nb
from mathmaker.lib.constants import DEFAULT_LAYOUT


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


def test_AttrStr_split_in_pages():
    """Check split_in_pages() in various cases."""
    assert _AttrStr('rowxcol=?×2, print=3 3, spacing=') \
        .split_in_pages('wordings') \
        == [{'wordings': 'rowxcol=?×2, print=3 3, spacing='}]
    assert _AttrStr('print=2, spacing=jump to next page, print=1') \
        .split_in_pages('answers') \
        == [{'answers': 'print=2, spacing=jump to next page'},
            {'answers': 'print=1'}]


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


def test_read_layout():
    """Check layout is correctly loaded from formatted strings in dict."""
    assert read_layout({}) == DEFAULT_LAYOUT
    assert read_layout({'any attribute': 'any value'}) == DEFAULT_LAYOUT
    layout_data = {'wordings': 'rowxcol=?×2,  print=5 5, spacing=25.0pt',
                   'answers': 'rowxcol=?×2,  print=5 5'}
    assert read_layout(layout_data) == \
        {'exc': [['?', 9, 9], (5, 5)], 'ans': [['?', 9, 9], (5, 5)],
         'spacing_w': '25.0pt', 'spacing_a': 'undefined'}
    layout_data = {'wordings': 'rowxcol=?×2,  print=3 3, spacing=25.0pt',
                   'answers': 'rowxcol=?×2,  print=3 3, spacing='}
    assert read_layout(layout_data) == \
        {'exc': [['?', 9, 9], (3, 3)], 'ans': [['?', 9, 9], (3, 3)],
         'spacing_w': '25.0pt', 'spacing_a': ''}
    layout_data = {'answers': 'print=2, spacing=jump to next page, print=1'}
    assert read_layout(layout_data) == \
        {'exc': [None, 'all'],
         'ans': [None, 2, 'jump', 'next_page', None, 1],
         'spacing_w': 'undefined', 'spacing_a': 'undefined'}


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
                      ('questions',
                       'expand double -> intpairs_2to9;;intpairs_2to9 (5)')
                      ]))])


def test__read_simple_question_exceptions():
    """Test malformed simple questions raise the right exceptions."""
    with pytest.raises(ValueError) as excinfo:
        _read_simple_question(' -> intpairs_2to9;;intpairs_2to9 (5)')
    assert 'missing question\'s name' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        _read_simple_question('expand double -> '
                              'intpairs_2to9;;intpairs_2to9 5)')
    assert 'is not built in pairs around the \'->\' symbol' \
        in str(excinfo.value)
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
