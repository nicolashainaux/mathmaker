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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package mc_modules
# @brief All question objects should be "declared" here.

from . import (multi_direct, multi_reversed, multi_hole, divi_direct,
               multi_clever,
               addi_direct, subtr_direct, rank_direct, rank_reversed,
               rank_numberof, vocabulary_simple_part_of_a_number,
               vocabulary_simple_multiple_of_a_number,
               vocabulary_multi, vocabulary_divi,
               vocabulary_addi, vocabulary_subtr, area_rectangle, area_square,
               perimeter_rectangle, perimeter_square,
               rectangle_length_or_width)

__all__ = ['multi_direct', 'multi_reversed', 'multi_hole', 'divi_direct',
           'multi_clever',
           'addi_direct', 'subtr_direct', 'rank_direct', 'rank_reversed',
           'rank_numberof', 'vocabulary_simple_part_of_a_number',
           'vocabulary_simple_multiple_of_a_number', 'vocabulary_multi',
           'vocabulary_divi', 'vocabulary_addi', 'vocabulary_subtr',
           'area_rectangle', 'area_square', 'perimeter_rectangle',
           'perimeter_square', 'rectangle_length_or_width', ]
