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


def distcode(*numbers):
    """Identifies a tuple of numbers depending on its composition."""
    already_found = []
    code = []
    for n in numbers:
        if n not in already_found:
            already_found.append(n)
            code.append(numbers.count(n))
    code.sort(reverse=True)
    return '_'.join([str(c) for c in code])


def nndist(nn_tuple):
    """
    Return a list of pairs (nb of times number shows up, number).

    :Examples:

    >>> nndist((3, 4, 4))
    [(1, 3), (2, 4)]
    >>> nndist((2, 5, 5, 5, 8, 8))
    [(1, 2), (2, 8), (3, 5)]
    """
    return sorted(list(set([(nn_tuple.count(n), n) for n in nn_tuple])))


def expanddist(nndist):
    """
    Perform the opposite of nndist().

    :Examples:

    >>> expanddist([(1, 3), (2, 4)])
    [3, 4, 4]
    >>> expanddist([(1, 2), (2, 8), (3, 5)])
    [2, 5, 5, 5, 8, 8]
    """
    return sorted([item
                   for sublist in [[pair[1]] * pair[0] for pair in nndist]
                   for item in sublist])


def matchdist(nndist, distcode):
    """
    Tell whether the natural numbers' distribution matches the distcode.

    Take care, the order of numbers in the distribution is the contrary of the
    one in the distcode.

    :Examples:

    >>> matchdist([(1, 3), (2, 4)], '2_1')
    True
    >>> matchdist([(1, 2), (2, 8), (3, 5)], '3_2_1')
    True
    >>> matchdist([(2, 2), (2, 6), (3, 4)], '3_3_2')
    False
    """
    distcode_nb = [int(n) for n in distcode.strip('r').split('_')]
    nndist_nb = [pair[0] for pair in nndist]
    return sorted(distcode_nb) == sorted(nndist_nb)
