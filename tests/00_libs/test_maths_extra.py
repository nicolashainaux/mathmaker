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

from mathmaker.lib.maths_lib import ten_power_gcd


def test_ten_power_gcd_1():
    """Checks ten_power_gcd() on a couple of integers."""
    assert ten_power_gcd(3, 4) == 1


def test_ten_power_gcd_2():
    """Checks ten_power_gcd() on a couple of integers."""
    assert ten_power_gcd(10, 4) == 1


def test_ten_power_gcd_3():
    """Checks ten_power_gcd() on a couple of integers."""
    assert ten_power_gcd(10, 10) == 10


def test_ten_power_gcd_4():
    """Checks ten_power_gcd() on a couple of integers."""
    assert ten_power_gcd(200, 50) == 10


def test_ten_power_gcd_5():
    """Checks ten_power_gcd() on a couple of integers."""
    assert ten_power_gcd(21000, 400) == 100
