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
# @package sheet
# @brief A sheet contains a title, subtitle, exercises list & answers title.

from . import S_Structure
from . import S_Generic
from . import AlgebraExpressionReduction
from . import AlgebraExpressionExpansion
from . import AlgebraShortTest
from . import AlgebraBalance_01
from . import AlgebraBinomialIdentityExpansion
from . import EquationsBasic
from . import EquationsClassic
from . import EquationsHarder
from . import EquationsShortTest
from . import EquationsTest
from . import FractionSimplification
from . import FractionsProductAndQuotient
from . import FractionsSum
from . import AlgebraFactorization_01
from . import AlgebraFactorization_02
from . import AlgebraFactorization_03
from . import AlgebraTest2
from . import AlgebraMiniTest0
from . import AlgebraMiniTest1
from . import PythagoreanTheoremShortTest
from . import ConverseAndContrapositiveOfPythagoreanTheoremShortTest

S_Structure = S_Structure.S_Structure
S_Generic = S_Generic.S_Generic
AlgebraExpressionReduction = \
    AlgebraExpressionReduction.AlgebraExpressionReduction
AlgebraExpressionExpansion = \
    AlgebraExpressionExpansion.AlgebraExpressionExpansion
EquationsBasic = EquationsBasic.EquationsBasic
EquationsClassic = EquationsClassic.EquationsClassic
EquationsHarder = EquationsHarder.EquationsHarder
EquationsShortTest = EquationsShortTest.EquationsShortTest
EquationsTest = EquationsTest.EquationsTest
AlgebraShortTest = AlgebraShortTest.AlgebraShortTest
AlgebraBalance_01 = AlgebraBalance_01.AlgebraBalance_01
# StructureShortTest = StructureShortTest.StructureShortTest
AlgebraBinomialIdentityExpansion = \
    AlgebraBinomialIdentityExpansion.AlgebraBinomialIdentityExpansion
FractionSimplification = FractionSimplification.FractionSimplification
FractionsProductAndQuotient = \
    FractionsProductAndQuotient.FractionsProductAndQuotient
FractionsSum = FractionsSum.FractionsSum
AlgebraFactorization_01 = AlgebraFactorization_01.AlgebraFactorization_01
AlgebraFactorization_02 = AlgebraFactorization_02.AlgebraFactorization_02
AlgebraFactorization_03 = AlgebraFactorization_03.AlgebraFactorization_03
AlgebraTest2 = AlgebraTest2.AlgebraTest2
AlgebraMiniTest0 = AlgebraMiniTest0.AlgebraMiniTest0
AlgebraMiniTest1 = AlgebraMiniTest1.AlgebraMiniTest1
PythagoreanTheoremShortTest = \
    PythagoreanTheoremShortTest.PythagoreanTheoremShortTest
ConverseAndContrapositiveOfPythagoreanTheoremShortTest = \
    ConverseAndContrapositiveOfPythagoreanTheoremShortTest.\
    ConverseAndContrapositiveOfPythagoreanTheoremShortTest


AVAILABLE = {"algebra-expression-reduction": (AlgebraExpressionReduction, ""),
             "algebra-expression-expansion": (AlgebraExpressionExpansion, ""),
             "algebra-binomial-identities-expansion":
                 (AlgebraBinomialIdentityExpansion, ""),
             "algebra-short-test": (AlgebraShortTest, ""),
             "algebra-balance-01": (AlgebraBalance_01, ""),
             "algebra-factorization-01": (AlgebraFactorization_01, ""),
             "algebra-factorization-02": (AlgebraFactorization_02, ""),
             "algebra-factorization-03": (AlgebraFactorization_03, ""),
             "algebra-test-2": (AlgebraTest2, ""),
             "algebra-mini-test-0": (AlgebraMiniTest0, ""),
             "algebra-mini-test-1": (AlgebraMiniTest1, ""),
             "equations-basic": (EquationsBasic, ""),
             "equations-classic": (EquationsClassic, ""),
             "equations-harder": (EquationsHarder, ""),
             "equations-test": (EquationsTest, ""),
             "equations-short-test": (EquationsShortTest, ""),
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
