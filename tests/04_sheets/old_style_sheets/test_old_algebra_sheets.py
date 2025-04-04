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

from mathmaker.lib import shared
from mathmaker.lib.old_style_sheet import AVAILABLE


def test_expression_reduction():
    """
    Checks if 'algebra-expression-reduction' is generated without any error.
    """
    shared.machine.write_out(
        str(AVAILABLE['algebra-expression-reduction'][0]()))


def test_binomial_identities_expansion():
    """
    Checks if 'algebra-binomial-identities-expansion' is generated
    without any error.
    """
    shared.machine.write_out(
        str(AVAILABLE['algebra-binomial-identities-expansion'][0]()))


def test_factorization_01():
    """Checks if 'algebra-factorization-01' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['algebra-factorization-01'][0]()))


def test_factorization_03():
    """Checks if 'algebra-factorization-03' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['algebra-factorization-03'][0]()),
                             pdf_output=True)


def test_mini_test_0():
    """Checks if 'algebra-mini-test-0' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['algebra-mini-test-0'][0]()),
                             pdf_output=True)
