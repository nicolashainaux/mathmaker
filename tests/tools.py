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

"""Auxiliary functions to help writing tests."""

import re


def wrap_nb(s):
    r"""
    All numbers of the string s get wrapped inside \\text{}.

    Dots are taken into account, but not signs.
    This function is meant to lighten the writing of LaTeX expressions.

    :Example:

    >>> wrap_nb('34\\times 67.2 + 6 - 4 + (-5)')
    '\\text{34}\\times \\text{67.2} + \\text{6} - \\text{4} + (-\\text{5})'
    >>> wrap_nb(' - (+7.2)')
    ' - (+\\text{7.2})'
    """
    p = re.compile(r'((\d*\.\d+)|(\d+))', re.LOCALE)
    return p.sub(r'\\text{' + r'\1' + r'}', s)
