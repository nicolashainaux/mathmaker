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

import sqlite3

from mathmaker import settings
from mathmaker.lib.machine import LaTeX
from mathmaker.lib.common import latex


def init():
    global db
    global four_letters_words_source
    global five_letters_words_source
    global names_source
    global mini_problems_wordings_source
    global markup
    global int_pairs_source
    global single_ints_source
    global angle_ranges_source
    global int_deci_clever_pairs_source
    global rank_words_source
    global int_fracs_source
    global deci_10_100_1000_multi_source
    global deci_10_100_1000_divi_source
    global deci_one_digit_multi_source
    global deci_one_digit_divi_source
    global mc_source
    global machine
    global number_of_the_question

    log = settings.mainlogger

    db = sqlite3.connect(settings.path.db)

    from mathmaker.lib.tools import db as database
    four_letters_words_source = database.source("w4l", ["id", "word"],
                                                language=settings.language)

    five_letters_words_source = database.source("w5l", ["id", "word"],
                                                language=settings.language)
    names_source = database.source("names", ["id", "name"],
                                   language=settings.language)
    mini_problems_wordings_source = database.source("mini_pb_wordings",
                                                    ["wording_context",
                                                     "wording"])
    int_pairs_source = database.source("int_pairs", ["id", "nb1", "nb2"])
    single_ints_source = database.source("single_ints", ["id", "nb1"])
    angle_ranges_source = database.source("angle_ranges", ["id", "nb1", "nb2"])
    int_deci_clever_pairs_source = database.source("int_deci_clever_pairs",
                                                   ["id", "nb1", "nb2"])

    markup = latex.MARKUP

    from mathmaker.lib import sources
    rank_words_source = sources.sub_source('rank_words')
    int_fracs_source = sources.sub_source('int_irreducible_frac')
    deci_10_100_1000_multi_source = sources.sub_source(
        'decimal_and_10_100_1000_for_multi')
    deci_10_100_1000_divi_source = sources.sub_source(
        'decimal_and_10_100_1000_for_divi')
    deci_one_digit_multi_source = sources.sub_source(
        'decimal_and_one_digit_for_multi')
    deci_one_digit_divi_source = sources.sub_source(
        'decimal_and_one_digit_for_divi')
    mc_source = sources.mc_source()

    try:
        machine = LaTeX(settings.language)
    except Exception:
        log.error("An exception occured while creating the LaTeX machine.",
                  exc_info=True)

    number_of_the_question = 0
