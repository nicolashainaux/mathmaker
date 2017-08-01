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

from mathmaker.lib.maths_lib import ten_power_gcd, prime_factors


def test_ten_power_gcd():
    """Checks ten_power_gcd() on couples of integers."""
    assert ten_power_gcd(3, 4) == 1
    assert ten_power_gcd(10, 4) == 1
    assert ten_power_gcd(10, 10) == 10
    assert ten_power_gcd(200, 50) == 10
    assert ten_power_gcd(21000, 400) == 100


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
