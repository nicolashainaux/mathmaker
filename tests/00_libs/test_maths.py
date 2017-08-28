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

from mathmaker.lib.tools.maths import ten_power_gcd, prime_factors, coprimes_to


def test_ten_power_gcd():
    """Checks ten_power_gcd() on couples of integers."""
    assert ten_power_gcd(3, 4) == 1
    assert ten_power_gcd(10, 4) == 1
    assert ten_power_gcd(10, 10) == 10
    assert ten_power_gcd(200, 50) == 10
    assert ten_power_gcd(21000, 400) == 100


def test_prime_factors_exception():
    """Checks prime_factors() raises exception on wrong argument."""
    with pytest.raises(TypeError) as excinfo:
        prime_factors('a')
    assert str(excinfo.value) == 'n must be an int'


def test_prime_factors():
    """Checks prime_factors() results."""
    assert prime_factors(1) == []
    assert prime_factors(2) == [2]
    assert prime_factors(3) == [3]
    assert prime_factors(4) == [2, 2]
    assert prime_factors(10) == [2, 5]
    assert prime_factors(16) == [2, 2, 2, 2]
    assert prime_factors(31) == [31]
    assert prime_factors(16065) == [3, 3, 3, 5, 7, 17]
    assert all(type(n) is int for n in prime_factors(210))


def test_coprimes_to():
    """Checks coprimes_to() results."""
    assert coprimes_to(9, [i + 1 for i in range(12)]) == [1, 2, 4, 5, 7, 8, 10,
                                                          11]
    assert coprimes_to(1, [i + 1 for i in range(12)]) == [1, 2, 3, 4, 5, 6, 7,
                                                          8, 9, 10, 11, 12]
    assert coprimes_to(3, [3, 6, 9]) == []
