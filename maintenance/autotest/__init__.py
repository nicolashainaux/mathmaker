# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
import gettext
from optparse import OptionParser

from lib import *
from lib.common import software
from . import common
from . import obj_test
from . import lib_test
import sheet
import machine
import time

AVAILABLE_UNITS = [ ("items",
                     obj_test.calc_test.items_test),
                    #("functional_items_test",
                    # obj_test.calc_test.functional_items_test),
                    ("values",
                     obj_test.calc_test.values_test),
                    ("products",
                     obj_test.calc_test.products_test),
                    ("monomials",
                     obj_test.calc_test.monomials_test),
                    ("product_reduction",
                     obj_test.calc_test.product_reduction_test),
                    ("sums",
                     obj_test.calc_test.sums_test),
                    ("sum_reduction",
                     obj_test.calc_test.sum_reduction_test),
                    ("quotients",
                     obj_test.calc_test.quotients_test),
                    ("fraction_simplification",
                     obj_test.calc_test.fraction_simplification_test),
                    ("fractions_products",
                     obj_test.calc_test.fractions_products_test),
                    ("fractions_quotients",
                     obj_test.calc_test.fractions_quotients_test),
                    ("fractions_sums",
                     obj_test.calc_test.fractions_sums_test),
                    ("equations",
                     obj_test.equations_test),
                    ("expansion_and_reduction",
                     obj_test.calc_test.expansion_and_reduction_test),
                    ("squareroots",
                     obj_test.calc_test.squareroots_test),
                    ("point",
                     obj_test.geo_test.point_test),
                    ("right_triangle",
                     obj_test.geo_test.right_triangle_test),
                    ("triangle",
                     obj_test.geo_test.triangle_test),
                    ("utils",
                     lib_test.utils_test),
                    ("table",
                     obj_test.table_test),
                    ("cross_product_equations",
                     obj_test.cross_product_equations_test),
                    ("table_UP",
                     obj_test.table_uncomplete_proportional_test) # ,
                   # ("functional_items",
                   #  obj_test.calc_test.functional_items_test)
                  ]

AVAILABLE_UNIT_NAMES = [AVAILABLE_UNITS[i][0] \
                        for i in range(len(AVAILABLE_UNITS))]

AVAILABLE_UNITS_LEXICON = {}
for i in range(len(AVAILABLE_UNITS)):
    AVAILABLE_UNITS_LEXICON[AVAILABLE_UNIT_NAMES[i]] = AVAILABLE_UNITS[i][1]


def short_test_run(lang):
    M = machine.LaTeX(lang, create_pic_file='no')
    for elt in sheet.catalog.XML_SHEETS:
        M.write(str(sheet.S_Generic(M, filename=sheet.catalog.XML_SHEETS[elt])))
    for elt in sheet.AVAILABLE:
        M.write(str(sheet.AVAILABLE[elt][0](M)))

def long_test_run(n, lang):
    for i in range(n):
        short_test_run(lang)
        #time.sleep(2)

def fraction_simplification_coverage(n):
    number_of_failed = 0
    for i in range(int(n)):
        os.write(common.output, bytes("\n" + str(i+1), 'utf-8'))
        for j in range(int(n)):
            # test if the Fraction i over j is reduced the right way
            f = common.Fraction(('+', i+1, j+1))
            if f.is_reducible():
                go_on = True
                while go_on:
                    g = f.simplified()
                    if not g.is_reducible():
                        os.write(common.output, bytes(".", 'utf-8'))
                        go_on = False
                    elif g.numerator.factor[0].raw_value == \
                                              f.numerator.factor[0].raw_value \
                         and g.denominator.factor[0].raw_value == \
                                             f.denominator.factor[0].raw_value:
                    #___
                        os.write(common.err_output,
                                 bytes("\nFAILED : " \
                                 + str(i+1) + "/" + str(j+1) \
                                 + " -------- Step " \
                                 + str(g.numerator.factor[0].raw_value) \
                                 + "/" \
                                 + str(g.denominator.factor[0].raw_value) \
                                 + "\n", 'utf-8'))
                        go_on = False
                        number_of_failed += 1

                    else:
                        f = g
                        # go_on is still True
            else:
                os.write(common.output, bytes(".", 'utf-8'))

    os.write(common.output, bytes("\nNumber of failed : " + \
                                     str(number_of_failed) + "\n", 'utf-8'))


def main():
    parser = OptionParser(usage="usage: %prog [options] arg",
                          version="autotest for " + software.NAME + "\n" \
                                  + software.NAME + " " + software.VERSION \
                                  + "\nLicense : " + software.LICENSE \
                                  + "\n" + software.COPYRIGHT + " " \
                                  + software.AUTHOR)

    parser.add_option("-l", "--language",
                      action="store",
                      dest="lang",
                      default='en',
                      metavar="LANGUAGE",
                      help="will check if LANGUAGE is available and if yes," \
                           + " will produce the output in LANGUAGE.")

    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="will turn on verbose mode (more details will be" \
                           + " written to the output.)")

    parser.add_option("-V", "--superverbose",
                      action="store_true",
                      dest="superverbose",
                      default=False,
                      help="will turn on superverbose mode (much more " \
                           + "details will be written to the output.)")

    parser.add_option("--short-test-run",
                      action="store_true",
                      dest="short_test_run",
                      default=False,
                      help="will start a short test run (writes once each" \
                           + " of the available sheets on the std err " \
                           + "output) instead of a unit test.")

    parser.add_option("--long-test-run",
                      action="store",
                      type="int",
                      dest="long_test_run",
                      default=0,
                      help="will start a long test run (writes n times the" \
                           + " available sheets on the std err output) " \
                           + "instead of a unit test." \
                           + " This option will be ignored if " \
                           + "--short-test-run is specified.")

    parser.add_option("-F", "--fraction-simplification-coverage",
                      action="store",
                      type="int",
                      dest="fraction_simplification_coverage",
                      metavar="N",
                      default=0,
                      help="will start a special test to check the " \
                           + "simplification of fractions. It will test " \
                           + "all fractions from 1/1 to N/N")

    parser.add_option("-u", "--unit",
                      action="append",
                      type="string",
                      dest="units",
                      help="will test only the given unit, instead of all of" \
                           + "them (default behaviour). This option can be" \
                           + " repeated to test several units, for instance " \
                           + ": autotest-mathmaker -u item -u " \
                           + "product will check only these two units :" \
                           + " item_test and product_test")

    parser.add_option("--units-list",
                      action="store_true",
                      dest="units_list",
                      default=False,
                      help="will write the list of available units and exit.")

    (options, args) = parser.parse_args()

    if options.verbose:
        common.verbose = True
        common.verbose_space = " "
        common.OK = "ok "
        common.FAILED = "FAILED :\n"
        common.MISSING = "MISSING : "

    elif options.superverbose:
        common.verbose = True
        common.superverbose = True
        common.verbose_space = " "
        common.OK = "ok "
        common.FAILED = "FAILED ]\n"
        common.MISSING = "MISSING : "
        common.superverbose_opening_token = "[#"
        common.superverbose_closing_token = "] "

    if options.lang == 'en':
        gettext.translation(software.NAME,
                            common.localdir,
                            ['en']).install()
    else:
        common.tested_language = options.lang
        language_test(options.lang)

    if options.units_list:
        os.write(common.output,
                 bytes("List of available test units :\n", 'utf-8'))
        for u in AVAILABLE_UNITS:
            os.write(common.output, bytes(u[0] + "\n", 'utf-8'))

    elif options.short_test_run:
        short_test_run(common.tested_language)

    elif options.long_test_run != 0:
        long_test_run(options.long_test_run, common.tested_language)

    elif options.fraction_simplification_coverage != 0:
        fraction_simplification_coverage(\
                                      options.fraction_simplification_coverage)

    else:
        tested_units = []
        if options.units != None and len(options.units) != 0:
            for i in range(len(options.units)):
                if options.units[i] in AVAILABLE_UNIT_NAMES:
                    tested_units.append(AVAILABLE_UNITS_LEXICON[\
                                                             options.units[i]])
                else:
                    os.write(common.output,
                                     bytes("You requested to test the unit '" \
                                     + options.units[i] \
                                     + "' but it's not available. " \
                                     + "Run autotest-mathmaker --units-list" \
                                     + " for more information.\n", 'utf-8'))
        else:
            for u in AVAILABLE_UNITS:
                tested_units.append(u[1])

        for unit in tested_units:
            common.counter = 0
            common.superverbose_counter = 0
            unit.action()
            if common.verbose:
                os.write(common.output, bytes("\n", 'utf-8'))

        if not common.verbose:
            os.write(common.output, bytes("\n", 'utf-8'))

        os.write(common.output,
                 bytes("FAILED : " + str(common.failed_counter) \
                 + " MISSING : " + str(common.missing_counter) \
                 + "\nTotal OK : " \
                 + str(common.global_counter - \
                       common.missing_counter - \
                       common.failed_counter)\
                 + "/" + str(common.global_counter) + "\n", 'utf-8'))
