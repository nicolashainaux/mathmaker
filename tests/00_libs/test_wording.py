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

import pytest

from mathmakerlib.calculus.unit import MASS_UNITS

from mathmaker.lib import shared
from mathmaker.lib.tools.wording import (wrap, is_wrapped,
                                         is_wrapped_P,
                                         is_wrapped_p, is_unit, is_unitN,
                                         extract_formatting_tags_from,
                                         cut_off_hint_from,
                                         setup_wording_format_of,
                                         handle_valueless_names_tags,
                                         handle_valueless_unit_tags,
                                         process_attr_values,
                                         merge_nb_unit_pairs,
                                         insert_nonbreaking_spaces,
                                         post_process)


class raw_obj(object):
    pass


@pytest.fixture
def o1():
    o = raw_obj()
    o.name = 'Cosette'
    o.capacity_unit = 'L'
    return o


@pytest.fixture
def owbuggy():
    o = raw_obj()
    o.wording = 'A glas of {nb1} {capacity_unit}. |hint:volume_unit|'
    return o


@pytest.fixture
def owbuggy2():
    o = raw_obj()
    o.wording = 'A glas of {nb1} {capacity_unit}. |hint:area_unit|'
    return o


@pytest.fixture
def ow7():
    o = raw_obj()
    o.nb1 = 3
    o.capacity_unit = 'L'
    o.nb = 20
    o.length_unit1 = 'cm'
    o.nb3 = 9
    o.length_unit3 = 'mm'
    o.volume_unit3 = 'mm'
    o.wording = 'A glas of {nb1} {capacity_unit} and a rule of ' \
                '{nb} {length_unit1} long and a dice of {nb3} {volume_unit3}.'
    return o


@pytest.fixture
def ow2():
    o = raw_obj()
    o.nb = 6
    o.nb3 = 11
    o.wording = 'Just a try for a {name}, a {nb} {capacity_unit}; a ' \
                '{nb1=8} {length_unit1} and finally {nb3} {volume_unit3=cm}.'
    return o


@pytest.fixture
def ow1():
    o = raw_obj()
    o.nb1 = 4
    o.wording = 'Calculate the volume of a cube whose side\'s length is ' \
                '{nb1} {length_unit=cm}. |hint:volume_unit|'
    setup_wording_format_of(o)
    return o


@pytest.fixture
def ow2bis():
    o = raw_obj()
    o.nb1 = 4
    o.nb2 = 7
    o.wording = 'How much is {nb1} {length_unit1=dm} '\
                '+ {nb2} {length_unit2=cm}? |hint:length_unit1|'
    setup_wording_format_of(o)
    return o


@pytest.fixture
def ow2ter():
    o = raw_obj()
    o.nb1 = 27
    o.wording = 'What\'s the area of the side of a cube whose volume '\
                'is {nb1} {volume_unit=cm}? |hint:area_unit|'
    setup_wording_format_of(o)
    return o


@pytest.fixture
def ow2qua():
    o = raw_obj()
    o.line1 = 'AB'
    o.line2 = 'MN'
    o.s = 'BC'
    o.wording = '({line1}) is parallel to ({line2}). '\
                'Calculate the length of segment [{s}].'
    setup_wording_format_of(o)
    return o


@pytest.fixture
def ow_units1():
    o = raw_obj()
    o.nb1 = 7
    o.wording = 'The first weighs {nb1} {mass_unit=kg} and the second\'s ' \
        '{mass_unit}.'
    setup_wording_format_of(o)
    return o


def test_wrap_01():
    """Checks wrap('s') gives out '{s}'."""
    assert wrap('Something like this.') == '{Something like this.}'


def test_wrap_02():
    """Checks wrap('s', e_str='},') gives out '{s},'."""
    assert wrap('One word', e_str='},') == '{One word},'


def test_is_wrapped_01():
    """Checks if is_wrapped('{Two words}') is True."""
    assert is_wrapped('{Two words}') is True


def test_is_wrapped_02():
    """Checks if is_wrapped('<Two words>') is False."""
    assert is_wrapped('<Two words>') is False


def test_is_wrapped_03():
    """Checks if is_wrapped('{Two words}:') is False."""
    assert is_wrapped('{Two words}:') is False


def test_is_wrapped_04():
    """Checks if is_wrapped('<Two words>', braces='<>') is True."""
    assert is_wrapped('<Two words>', braces='<>') is True


def test_is_wrapped_p_01():
    """Checks if is_wrapped_p('{Two words}') is True."""
    assert is_wrapped_p('{Two words}') is True


def test_is_wrapped_p_02():
    """Checks if is_wrapped_p('<Two words>') is False."""
    assert is_wrapped_p('<Two words>') is False


def test_is_wrapped_p_03():
    """Checks if is_wrapped_p('{Two words}:') is True."""
    assert is_wrapped_p('{Two words}:') is True


def test_is_wrapped_p_04():
    """Checks if is_wrapped_p('<Two words>', braces='<>') is True."""
    assert is_wrapped_p('<Two words>', braces='<>') is True


def test_is_wrapped_p_05():
    """Checks if is_wrapped_p('<Two words>?', braces='<>') is True."""
    assert is_wrapped_p('<Two words>?', braces='<>') is True


def test_is_wrapped_P_01():
    """Checks if is_wrapped_P('{Two words}') is False."""
    assert is_wrapped_P('{Two words}') is False


def test_is_wrapped_P_02():
    """Checks if is_wrapped_P('<Two words>') is False."""
    assert is_wrapped_P('<Two words>') is False


def test_is_wrapped_P_03():
    """Checks if is_wrapped_P('{Two words}:') is True."""
    assert is_wrapped_P('{Two words}:') is True


def test_is_wrapped_P_04():
    """Checks if is_wrapped_P('<Two words>', braces='<>') is False."""
    assert is_wrapped_P('<Two words>', braces='<>') is False


def test_is_wrapped_P_05():
    """Checks if is_wrapped_P('<Two words>?', braces='<>') is True."""
    assert is_wrapped_P('<Two words>?', braces='<>') is True


def test_extract_formatting_tags_from_01():
    """Checks if {all} {these} {tags}, and even this {one}! are found."""
    assert extract_formatting_tags_from('{all} {these} {tags}, and even '
                                        'this {one}! are found') == \
        ['all', 'these', 'tags', 'one']


def test_is_unit_01():
    """Checks if is_unit('{some_unit}') is True."""
    assert is_unit('{some_unit}') is True


def test_is_unit_02():
    """Checks if is_unit('{ordinary_tag}') is False."""
    assert is_unit('{ordinary_tag}') is False


def test_is_unit_03():
    """Checks if is_unit('ordinary_str') is False."""
    assert is_unit('ordinary_str') is False


def test_is_unit_04():
    """Checks if is_unit('<wrongwrapped_unit>') is False."""
    assert is_unit('<wrongwrapped_unit>') is False


def test_is_unitN_01():
    """Checks if is_unitN('{some_unit}') is False."""
    assert is_unitN('{some_unit}') is False


def test_is_unitN_02():
    """Checks if is_unitN('{ordinary_tag}') is False."""
    assert is_unitN('{ordinary_tag}') is False


def test_is_unitN_03():
    """Checks if is_unitN('ordinary_str') is False."""
    assert is_unitN('ordinary_str') is False


def test_is_unitN_04():
    """Checks if is_unitN('{some_unit1}') is True."""
    assert is_unitN('{some_unit1}') is True


def test_is_unitN_05():
    """Checks if is_unitN('unwrapped_unit0') is False."""
    assert is_unitN('unwrapped_unit0') is False


def test_is_unitN_06():
    """Checks if is_unitN('(wrongwrapped_unit0)') is False."""
    assert is_unitN('(wrongwrapped_unit0)') is False


def test_cutoff_hint_from_01():
    """Checks if the hint is removed correctly from the sentence."""
    assert cut_off_hint_from('How many {nb1} {length_unit} have you been '
                             'riding? |hint:length_unit|') == \
        ('How many {nb1} {length_unit} have you been riding?', 'length_unit')


def test_cutoff_hint_from_02():
    """Checks if the hint is removed correctly from the sentence."""
    assert cut_off_hint_from('No hint to remove from this wording, sorry.') ==\
        ('No hint to remove from this wording, sorry.', '')


def test_handle_valueless_names_tags_01(o1):
    """Checks if only valueless (yet) names tags are handled (correctly)."""
    handle_valueless_names_tags(o1, 'We know her {name} '
                                    'but not her {name_family}')
    assert hasattr(o1, 'name_family')


def test_handle_valueless_names_tags_02(o1):
    """Checks if only valueless (yet) names tags are handled (correctly)."""
    handle_valueless_names_tags(o1, 'We know her {feminine_name} '
                                    'but not her {name}')
    assert hasattr(o1, 'feminine_name')


def test_handle_valueless_names_tags_03(o1):
    """Checks if only valueless (yet) names tags are handled (correctly)."""
    handle_valueless_names_tags(o1, 'We know her {feminine_name} '
                                    'but not her {name}')
    assert o1.name == 'Cosette'


def test_handle_valueless_names_tags_04(o1):
    """Checks if only valueless (yet) names tags are handled (correctly)."""
    handle_valueless_names_tags(o1, 'We know her {feminine_name} '
                                    'but not her {name=Fantine}')
    assert o1.name == 'Cosette'


def test_handle_valueless_names_tags_05(o1):
    """Checks if only valueless (yet) names tags are handled (correctly)."""
    handle_valueless_names_tags(o1, 'We know her {feminine_name=Margaret} '
                                    'but not her {name=Fantine}')
    assert not hasattr(o1, 'feminine_name')


def test_handle_valueless_unit_tags_01(o1):
    """Checks if only valueless (yet) units tags are handled (correctly)."""
    handle_valueless_unit_tags(o1, 'It weighs {nb1} {mass_unit}.')
    assert hasattr(o1, 'mass_unit')


def test_handle_valueless_unit_tags_02(o1):
    """Checks if only valueless (yet) units tags are handled (correctly)."""
    handle_valueless_unit_tags(o1, 'Its area is {nb1} {area_unit}.')
    assert hasattr(o1, 'length_unit')


def test_handle_valueless_unit_tags_03(o1):
    """Checks if only valueless (yet) units tags are handled (correctly)."""
    handle_valueless_unit_tags(o1, 'Its volume is {nb1} {volume_unit}.')
    assert hasattr(o1, 'length_unit')


def test_handle_valueless_unit_tags_04(o1):
    """Checks if only valueless (yet) units tags are handled (correctly)."""
    handle_valueless_unit_tags(o1, 'The first is {nb1} {length_unit1} long '
                                   'and the second\'s area is {nb2} '
                                   '{area_unit2}.')
    assert hasattr(o1, 'length_unit2')


def test_handle_valueless_unit_tags_05(o1):
    """Checks if only valueless (yet) units tags are handled (correctly)."""
    handle_valueless_unit_tags(o1, 'The first weighs {nb1} {mass_unit} '
                                   'and the second\'s.')
    assert hasattr(o1, 'mass_unit')
    assert getattr(o1, 'mass_unit') in MASS_UNITS


def test_handle_valueless_unit_tags_exceptions(o1):
    """Check if incorrect unit tags raise an exception."""
    with pytest.raises(ValueError):
        handle_valueless_unit_tags(o1, 'It weighs {nb1} {fancy_unit}.')


def test_process_attr_values_01():
    """Checks if {such_tags=val} are correctly processed."""
    assert process_attr_values('He likes {animal=cat}. He has a garden '
                               'as wide as {nb1} {area_unit1}. He wants '
                               'a {nb2} {volume_unit2=m} swiming pool.') == \
        ('He likes {animal}. He has a garden as wide as {nb1} {area_unit1}. '
         'He wants a {nb2} {volume_unit2} swiming pool.',
            {'animal': 'cat',
             'length_unit2': 'm',
             'volume_unit2': 'm'})


def test_merge_nb_unit_pairs_01(ow7):
    """Checks if {nb} {*unit} pairs are correctly processed in obj.wording."""
    merge_nb_unit_pairs(ow7)
    assert ow7.wording == 'A glas of {nb1_capacity_unit} and a rule of ' \
        '{nb_length_unit1} long and a dice of {nb3_volume_unit3}.'


def test_merge_nb_unit_pairs_02(ow7):
    """Checks if {nb} {*unit} pairs are correctly processed in obj.wording."""
    merge_nb_unit_pairs(ow7)
    assert ow7.nb_length_unit1 == '\\SI{20}{cm}'


def test_merge_nb_unit_pairs_03(ow7):
    """Checks if {nb} {*unit} pairs are correctly processed in obj.wording."""
    merge_nb_unit_pairs(ow7)
    assert ow7.nb1_capacity_unit == '\\SI{3}{L}'


def test_merge_nb_unit_pairs_04(ow7):
    """Checks if {nb} {*unit} pairs are correctly processed in obj.wording."""
    merge_nb_unit_pairs(ow7)
    assert ow7.nb3_volume_unit3 == '\\SI{9}{mm^{3}}'


def test_setup_wording_format_of_01(ow2):
    """Checks if obj.wording is correctly setup."""
    setup_wording_format_of(ow2)
    assert ow2.wording == 'Just a try for a {name}, a {nb_capacity_unit}; '\
                          'a {nb1_length_unit1} and finally '\
                          '{nb3_volume_unit3}.'


def test_setup_wording_format_of_02(ow2):
    """Checks if obj.wording is correctly setup."""
    setup_wording_format_of(ow2)
    assert hasattr(ow2, 'name')


def test_setup_wording_format_of_03(ow2):
    """Checks if obj.wording is correctly setup."""
    setup_wording_format_of(ow2)
    assert ow2.nb3_volume_unit3 == '\\SI{11}{cm^{3}}'


def test_setup_wording_format_of_04(ow2):
    """Checks if obj.wording is correctly setup."""
    setup_wording_format_of(ow2)
    assert ow2.nb1_length_unit1.startswith('\\SI{8}{')


def test_setup_wording_format_of_05(ow2):
    """Checks if obj.wording is correctly setup."""
    setup_wording_format_of(ow2)
    assert hasattr(ow2, 'nb_capacity_unit')


def test_setup_wording_format_of_06(ow1):
    """Checks if obj.wording is correctly setup."""
    assert hasattr(ow1, 'volume_unit')


def test_setup_wording_format_of_07(ow1):
    """Checks if obj.wording is correctly setup."""
    assert ow1.volume_unit == '\\si{cm^{3}}'


def test_setup_wording_format_of_08(ow2bis):
    """Checks if obj.wording is correctly setup."""
    assert ow2bis.hint == '\\si{dm}'


def test_setup_wording_format_of_09(ow2bis):
    """Checks if obj.wording is correctly setup."""
    assert ow2bis.nb1_length_unit1 == '\\SI{4}{dm}'


def test_setup_wording_format_of_10(ow2ter):
    """Checks if obj.wording is correctly setup."""
    assert ow2ter.volume_unit == '\\si{cm^{3}}'


def test_setup_wording_format_of_11(ow2ter):
    """Checks if obj.wording is correctly setup."""
    assert ow2ter.area_unit == '\\si{cm^{2}}'


def test_setup_wording_format_of_12(ow2qua):
    """Checks if obj.wording is correctly setup."""
    assert ow2qua.wording.format(**ow2qua.wording_format) == \
        '(AB) is parallel to (MN). '\
        'Calculate the length of segment [BC].'


def test_setup_wording_format_of_13(ow_units1):
    """Checks if obj.wording is correctly setup."""
    assert hasattr(ow_units1, 'mass_unit')
    assert getattr(ow_units1, 'mass_unit') == '\\si{kg}'


def test_setup_wording_format_of_exceptions(owbuggy):
    """Check if a wrong hint correctly raises an exception."""
    with pytest.raises(RuntimeError):
        setup_wording_format_of(owbuggy)


def test_setup_wording_format_of_exceptions2(owbuggy2):
    """Check if a wrong hint correctly raises an exception."""
    with pytest.raises(RuntimeError):
        setup_wording_format_of(owbuggy2)


def test_insert_nonbreaking_spaces():
    """Checks if non breaking spaces are correctly inserted."""
    assert insert_nonbreaking_spaces('It weighs about 45 kg.') == \
        'It weighs about 45' + shared.markup['nonbreaking_space'] + 'kg.'


def test_post_process():
    """Checks if non breaking spaces are correctly inserted."""
    assert post_process('It weighs about 45 kg.') == \
        'It weighs about 45' + shared.markup['nonbreaking_space'] + 'kg.'
