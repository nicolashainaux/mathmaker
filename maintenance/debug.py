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

import os
import sys
from lib.common import cfg

sdt_err_output = sys.stderr.fileno()

ENABLED_STRING = cfg.get_value_from_file("DEBUGGING MODE", "ENABLED")

ENABLED = False

if ENABLED_STRING == "True" or ENABLED_STRING == "true":
    ENABLED = True

into_str_in_item = False
into_str_in_product = False
into_str_in_sum = False
into_str_in_quotient = False
requires_brackets_in_sum = False
requires_inner_brackets_in_product = False
expand_and_reduce_next_step_sum = False
expand_and_reduce_next_step_product = False
expand_in_special_identity = False
reduce_in_sum = False
init_in_exercise_expression_expansion = False
init_in_question_expression_expansion = False
init_in_polynomial = False
solve_next_step = False
calculate_next_step_fraction = False
calculate_next_step_sum = False
calculate_next_step_item = False
replace_striked_out = False
striking_out_in_simplification_line = False
simplification_line_minus_signs = False
simplified = False
monomial_plus = False
throw_away_the_neutrals = False
product_is_reducible = True
get_factors_list_product = True
reduce__product = False
evaluate_in_operation = False




# --------------------------------------------------------------------------
##
#   @brief Writes the given String on the std err if debug mode is activated
#   Activating & de-activating the DEBUG mode is made setting the
#   ENABLED value at the beginning of this file.
#   @param provided_string The string to write on std err
def write(provided_string, **options):
    if ENABLED:
        if len(options) == 0:
            os.write(sdt_err_output, bytes(provided_string, 'utf-8'))

        elif 'case' in options and options['case'] == True:
            os.write(sdt_err_output, bytes(provided_string, 'utf-8'))
