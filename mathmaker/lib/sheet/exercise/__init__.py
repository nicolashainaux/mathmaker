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
# @package exercise
# @brief A exercise consists of a questions list plus output methods.

from . import X_Structure
from . import X_Generic

from . import X_AlgebraExpressionExpansion
from . import X_AlgebraExpressionReduction
from . import X_Calculation
from . import X_Equation
from . import X_Factorization
from . import X_RightTriangle

X_Structure = X_Structure.X_Structure
X_Generic = X_Generic.X_Generic

X_AlgebraExpressionExpansion = \
    X_AlgebraExpressionExpansion.X_AlgebraExpressionExpansion
X_AlgebraExpressionReduction = \
    X_AlgebraExpressionReduction.X_AlgebraExpressionReduction
X_Calculation = X_Calculation.X_Calculation
X_Equation = X_Equation.X_Equation
X_Factorization = X_Factorization.X_Factorization
X_RightTriangle = X_RightTriangle.X_RightTriangle
