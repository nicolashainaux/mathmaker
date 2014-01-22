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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package sheet
# @brief A sheet contains a title, subtitle, exercises list & answers title.

import S_Structure
import AlgebraExpressionReduction
import AlgebraExpressionExpansion
import AlgebraShortTest
import AlgebraBalance_01
import AlgebraBinomialIdentityExpansion
import EquationsBasic
import EquationsClassic
import EquationsHarder
import EquationsShortTest
import EquationsTest
import FractionSimplification
import FractionsProductAndQuotient
import FractionsSum
import AlgebraFactorization_01
import AlgebraFactorization_02
import AlgebraFactorization_03
import MentalCalculation
import AlgebraTest2
import AlgebraMiniTest0
import AlgebraMiniTest1
import PythagoreanTheoremShortTest
import ConverseAndContrapositiveOfPythagoreanTheoremShortTest

S_Structure = S_Structure.S_Structure
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
#StructureShortTest = StructureShortTest.StructureShortTest
AlgebraBinomialIdentityExpansion = \
            AlgebraBinomialIdentityExpansion.AlgebraBinomialIdentityExpansion
FractionSimplification = FractionSimplification.FractionSimplification
FractionsProductAndQuotient = \
                    FractionsProductAndQuotient.FractionsProductAndQuotient
FractionsSum = FractionsSum.FractionsSum
AlgebraFactorization_01 = AlgebraFactorization_01.AlgebraFactorization_01
AlgebraFactorization_02 = AlgebraFactorization_02.AlgebraFactorization_02
AlgebraFactorization_03 = AlgebraFactorization_03.AlgebraFactorization_03
MentalCalculation = MentalCalculation.MentalCalculation
AlgebraTest2 = AlgebraTest2.AlgebraTest2
AlgebraMiniTest0 = AlgebraMiniTest0.AlgebraMiniTest0
AlgebraMiniTest1 = AlgebraMiniTest1.AlgebraMiniTest1
PythagoreanTheoremShortTest = PythagoreanTheoremShortTest.PythagoreanTheoremShortTest
ConverseAndContrapositiveOfPythagoreanTheoremShortTest = \
    ConverseAndContrapositiveOfPythagoreanTheoremShortTest.\
        ConverseAndContrapositiveOfPythagoreanTheoremShortTest


AVAILABLE = {"algebra-expression-reduction" : \
                 (AlgebraExpressionReduction,
                     ""),
             "algebra-expression-expansion" : \
                 (AlgebraExpressionExpansion,
                     ""),
             "algebra-binomial-identities-expansion" : \
                 (AlgebraBinomialIdentityExpansion,
                     ""),
             "algebra-short-test" : \
                 (AlgebraShortTest,
                     ""),
             "algebra-balance-01" : \
                 (AlgebraBalance_01,
                     ""),
             "algebra-factorization-01" : \
                 (AlgebraFactorization_01,
                  ""),
             "algebra-factorization-02" : \
                 (AlgebraFactorization_02,
                  ""),
             "algebra-factorization-03" : \
                 (AlgebraFactorization_03,
                  ""),
             "algebra-test-2" : \
                 (AlgebraTest2,
                  ""),
             "algebra-mini-test-0" :\
                 (AlgebraMiniTest0,
                  ""),
             "algebra-mini-test-1" :\
                 (AlgebraMiniTest1,
                  ""),
             "equations-basic" : \
                 (EquationsBasic,
                  ""),
             "equations-classic" : \
                 (EquationsClassic,
                   ""),
             "equations-harder" : \
                 (EquationsHarder,
                  ""),
             "equations-test" : \
                 (EquationsTest,
                  ""),
             "equations-short-test" : \
                 (EquationsShortTest,
                  ""),
             "fraction-simplification" : \
                 (FractionSimplification,
                  ""),
             "fractions-product-and-quotient" : \
                 (FractionsProductAndQuotient,
                  ""),
             "fractions-sum": \
                 (FractionsSum,
                  ""),
             "mental-calculation": \
                 (MentalCalculation,
                  ""),
             "pythagorean-theorem-short-test" : \
                 (PythagoreanTheoremShortTest,
                  ""),
             "converse-and-contrapositive-of-pythagorean-theorem-short-test": \
                 (ConverseAndContrapositiveOfPythagoreanTheoremShortTest,
                  "")
             }
