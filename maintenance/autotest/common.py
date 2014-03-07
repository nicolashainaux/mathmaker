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
import gettext
import string
from optparse import OptionParser
from lib import *
from core.base_calculus import *
from core.calculus import *
import sheet
import machine



pathname = os.path.dirname(sys.argv[0])
localdir = os.path.abspath(pathname) + "/locale"

tested_language = 'en'

machines = [machine.LaTeX(tested_language)]

output = sys.stderr.fileno()
err_output = sys.stderr.fileno()

OK = "."
FAILED = "×"
MISSING = "!"
verbose = False
verbose_space = ""
superverbose = False
last_was_OK = False
counter = 0
global_counter = 0
failed_counter = 0
missing_counter = 0
section = ""
superverbose_opening_token = ""
superverbose_closing_token = ""
superverbose_counter = 0

def check(t, given_string):
    global global_counter, counter, last_was_OK, superverbose_counter,\
           failed_counter, missing_counter
    counter += 1
    superverbose_counter += 1
    global_counter += 1

    computed_string = []

    if isinstance(t, Printable):
        for i in range(len(machines)):
            computed_string.append(machines[i].type_string(t))
    else:
        computed_string.append(str(t))

    if not isinstance(t, Printable):
        if superverbose:
            n = str(counter)
        else:
            n = ""
        if superverbose_counter == 10 and verbose:
            next_line = "\n"
            superverbose_counter = 0
        else:
            next_line = ""
        if counter < 10 and superverbose:
            add_space = "  "
        elif counter < 100 and superverbose:
            add_space = " "
        else:
            add_space = ""

        if computed_string[0].replace("\n", "") == \
                                             given_string[0].replace("\n", ""):

            os.write(output, bytes(superverbose_opening_token + add_space \
                             + n + verbose_space + OK \
                             + superverbose_closing_token \
                             + next_line, 'utf-8'))
            last_was_OK = True
        else:
            if verbose:
                os.write(output,
                     "\n" + superverbose_opening_token + add_space \
                     + str(counter) + " "                         \
                     + FAILED                                                 \
                     + '"' + computed_string[0].replace("\n", "") + '"'                         \
                     + "\nshould have been\n"                                 \
                     + '"' + given_string[0].replace("\n", "") + '"' + "\n")
            else:
                os.write(output, bytes(FAILED, 'utf-8'))

            failed_counter += 1
            last_was_OK = False

    else:
        for i in range(len(machines)):
            if len(given_string) >= i + 1:
                if superverbose:
                    n = str(counter)
                else:
                    n = ""
                if superverbose_counter == 10 and verbose:
                    next_line = "\n"
                    superverbose_counter = 0
                else:
                    next_line = ""
                if counter < 10 and superverbose:
                    add_space = "  "
                elif counter < 100 and superverbose:
                    add_space = " "
                else:
                    add_space = ""

                if computed_string[i].replace("\n", "") == \
                                             given_string[i].replace("\n", ""):

                    os.write(output, bytes(superverbose_opening_token \
                                     + add_space \
                                     + n + verbose_space + OK \
                                     + superverbose_closing_token \
                                     + next_line, 'utf-8'))
                    last_was_OK = True
                else:
                    if verbose:
                        os.write(output,
                                 "\n" + superverbose_opening_token \
                                 + add_space + str(counter) + " "            \
                                 + FAILED                                     \
                                 + '"' \
                                 + computed_string[i].replace("\n", "") \
                                 + '"'             \
                                 + "\nshould have been\n"                     \
                                 + '"' + given_string[i].replace("\n", "") \
                                 + '"' + "\n")
                    else:
                        os.write(output, bytes(FAILED, 'utf-8'))

                    failed_counter += 1
                    last_was_OK = False

            else:
                if verbose:
                    os.write(output,
                                 "\n" + "[# " + str(counter) + " "            \
                                 + MISSING                                    \
                                 + "more machines than refs strings."
                                 + "\n")
                else:
                    os.write(output, MISSING)

                missing_counter += 1
                last_was_OK = False

        if len(given_string) > len(machines):
            if verbose:
                os.write(output,
                         "\n" + "# " + str(counter) + " "                     \
                         + MISSING                                            \
                         + "more refs strings than machines."
                         + "\n")
            else:
                os.write(output, MISSING)

            missing_counter += 1
            last_was_OK = False

def short_test_run(language):
    M = machine.LaTeX(language)

    for sheet_key in sheet.AVAILABLE:
        M.write(str(sheet_key[0](M)))


def long_test_run(n, language):
    for i in range(n):
        short_test_run(language)


def language_test(language):
    global tested_language
    try:
        gettext.translation(software.NAME,
                            localdir,
                            [language]).install()
    except IOError as msg:
        tested_language = 'en'
        gettext.translation(software.NAME,
                            localdir,
                            ['en']).install()

        print("error to check in source code of autotest/__init__()")
