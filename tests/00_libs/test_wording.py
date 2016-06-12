# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from lib.tools.wording import *
from tools import wrap_nb


class raw_obj(object): pass

@pytest.fixture
def o1():
    o = raw_obj()
    o.name = 'Cosette'
    return o


def test_wrap_01():
    """Checks wrap('s') gives out '{s}'."""
    assert wrap('Something like this.') == '{Something like this.}'


def test_wrap_02():
    """Checks wrap('s', e_str='},') gives out '{s},'."""
    assert wrap('One word', e_str='},') == '{One word},'


def test_unwrapped_01():
    """Checks unwrapped('{Anything}') gives out 'Anything'."""
    assert unwrapped('{Anything}') == 'Anything'


def test_unwrapped_02():
    """Checks unwrapped('{Anything},') gives out 'Anything'."""
    assert unwrapped('{Anything},') == 'Anything'


def test_unwrapped_03():
    """Checks unwrapped('{Anything}.') gives out 'Anything'."""
    assert unwrapped('{Anything}.') == 'Anything'


def test_unwrapped_04():
    """Checks unwrapped('{Anything};') gives out 'Anything'."""
    assert unwrapped('{Anything};') == 'Anything'


def test_unwrapped_05():
    """Checks unwrapped('{Anything}?') gives out 'Anything'."""
    assert unwrapped('{Anything}?') == 'Anything'


def test_unwrapped_06():
    """Checks unwrapped('{Anything}!') gives out 'Anything'."""
    assert unwrapped('{Anything}!') == 'Anything'


def test_unwrapped_07():
    """Checks unwrapped('{Anything}:') gives out 'Anything'."""
    assert unwrapped('{Anything}:') == 'Anything'


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
                             ('How many {nb1} {length_unit} have you been '\
                             'riding?', 'length_unit')


def test_cutoff_hint_from_02():
    """Checks if the hint is removed correctly from the sentence."""
    assert cut_off_hint_from('No hint to remove from this wording, sorry.') ==\
                             ('No hint to remove from this wording, sorry.',
                             '')


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



