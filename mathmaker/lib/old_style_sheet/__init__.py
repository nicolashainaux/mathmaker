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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package sheet
# @brief A sheet contains a title, subtitle, exercises list & answers title.

from . import S_Structure
from . import AlgebraExpressionReduction
from . import AlgebraBinomialIdentityExpansion
from . import EquationsBasic
from . import EquationsClassic
from . import EquationsHarder
from . import FractionSimplification
from . import FractionsProductAndQuotient
from . import FractionsSum
from . import AlgebraFactorization_01
from . import AlgebraFactorization_03
from . import AlgebraMiniTest0
from . import PythagoreanTheoremShortTest
from . import ConverseAndContrapositiveOfPythagoreanTheoremShortTest

S_Structure = S_Structure.S_Structure
AlgebraExpressionReduction = \
    AlgebraExpressionReduction.AlgebraExpressionReduction
EquationsBasic = EquationsBasic.EquationsBasic
EquationsClassic = EquationsClassic.EquationsClassic
EquationsHarder = EquationsHarder.EquationsHarder
AlgebraBinomialIdentityExpansion = \
    AlgebraBinomialIdentityExpansion.AlgebraBinomialIdentityExpansion
FractionSimplification = FractionSimplification.FractionSimplification
FractionsProductAndQuotient = \
    FractionsProductAndQuotient.FractionsProductAndQuotient
FractionsSum = FractionsSum.FractionsSum
AlgebraFactorization_01 = AlgebraFactorization_01.AlgebraFactorization_01
AlgebraFactorization_03 = AlgebraFactorization_03.AlgebraFactorization_03
AlgebraMiniTest0 = AlgebraMiniTest0.AlgebraMiniTest0
PythagoreanTheoremShortTest = \
    PythagoreanTheoremShortTest.PythagoreanTheoremShortTest
ConverseAndContrapositiveOfPythagoreanTheoremShortTest = \
    ConverseAndContrapositiveOfPythagoreanTheoremShortTest.\
    ConverseAndContrapositiveOfPythagoreanTheoremShortTest


AVAILABLE = {"algebra-expression-reduction": (AlgebraExpressionReduction, ""),
             "algebra-binomial-identities-expansion":
                 (AlgebraBinomialIdentityExpansion, ""),
             "algebra-factorization-01": (AlgebraFactorization_01, ""),
             "algebra-factorization-03": (AlgebraFactorization_03, ""),
             "algebra-mini-test-0": (AlgebraMiniTest0, ""),
             "equations-basic": (EquationsBasic, ""),
             "equations-classic": (EquationsClassic, ""),
             "equations-harder": (EquationsHarder, ""),
             "fraction-simplification": (FractionSimplification, ""),
             "fractions-product-and-quotient": (FractionsProductAndQuotient,
                                                ""),
             "fractions-sum": (FractionsSum, ""),
             "pythagorean-theorem-short-test": (PythagoreanTheoremShortTest,
                                                ""),
             "converse-and-contrapositive-of-pythagorean-theorem-short-test":
                 (ConverseAndContrapositiveOfPythagoreanTheoremShortTest,
                  "")
             }
