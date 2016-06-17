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

import sqlite3

import settings
import lib.machine
from lib.common import latex


def init():
    global db
    global four_letters_words_source
    global names_source
    global mini_problems_wordings_source
    global markup
    global int_pairs_source
    global rank_words_source
    global int_fracs_source
    global deci_10_100_1000_multi_source
    global deci_10_100_1000_divi_source
    global deci_one_digit_multi_source
    global deci_one_digit_divi_source
    global mc_source
    global machine

    log = settings.mainlogger

    db = sqlite3.connect(settings.path.db)

    import lib.tools.db
    four_letters_words_source = lib.tools.db.source("w4l", ["id", "word"],
                                                    language=settings.language)
    names_source = lib.tools.db.source("names", ["id", "name"],
                                       language=settings.language)
    mini_problems_wordings_source = lib.tools.db.source("mini_pb_wordings",
                                                ["wording_context", "wording"])
    int_pairs_source = lib.tools.db.source("int_pairs", ["id", "nb1", "nb2"])

    markup = latex.MARKUP

    import lib.sources
    rank_words_source = lib.sources.sub_source('rank_words')
    int_fracs_source = lib.sources.sub_source('int_irreducible_frac')
    deci_10_100_1000_multi_source = lib.sources.sub_source(
                                        'decimal_and_10_100_1000_for_multi')
    deci_10_100_1000_divi_source = lib.sources.sub_source(
                                        'decimal_and_10_100_1000_for_divi')
    deci_one_digit_multi_source = lib.sources.sub_source(
                                        'decimal_and_one_digit_for_multi')
    deci_one_digit_divi_source = lib.sources.sub_source(
                                        'decimal_and_one_digit_for_divi')
    mc_source = lib.sources.mc_source()

    try:
        machine = lib.machine.LaTeX(settings.language)
    except Exception:
        log.error("An exception occured while creating the LaTeX machine.",
                  exc_info=True)

