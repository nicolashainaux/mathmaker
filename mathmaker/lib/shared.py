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

import sqlite3

from mathmaker import settings
from mathmaker.lib.machine import LaTeX
from mathmaker.lib.constants import latex


def init():
    global db
    global shapes_db
    global three_letters_words_source
    global four_letters_words_source
    global five_letters_words_source
    global names_source
    global mini_problems_wordings_source
    global markup
    global int_pairs_source
    global int_triples_source
    global simple_fractions_source
    global single_ints_source
    global single_deci1_source
    global angle_ranges_source
    global int_deci_clever_pairs_source
    global digits_places_source
    global fracdigits_places_source
    global int_fracs_source
    global deci_10_100_1000_multi_source
    global deci_10_100_1000_divi_source
    global deci_one_digit_multi_source
    global deci_one_digit_divi_source
    global trigo_functions_source
    global trigo_vocabulary_source
    global mc_source
    global machine
    global number_of_the_question
    global order_of_operations_variants_source
    global unitspairs_source
    global alternate_source  # , alternate_source2
    global decimals_source
    global extdecimals_source
    global dvipsnames_selection_source
    global polygons_source
    global scalene_triangle_shapes_source
    global right_triangle_shapes_source
    global isosceles_triangle_shapes_source
    global equilateral_triangle_shapes_source
    global ls_marks_source
    global enable_js_form

    enable_js_form = False

    log = settings.mainlogger

    db = sqlite3.connect(settings.path.db)
    shapes_db = sqlite3.connect(settings.path.shapes_db)

    from mathmaker.lib.tools import database
    three_letters_words_source = database.source("w3l", ["id", "word"],
                                                 language=settings.language)
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
    int_triples_source = database.source("int_triples",
                                         ["id", "nb1", "nb2", "nb3"])
    simple_fractions_source = database.source('simple_fractions',
                                              ['id', 'nb1', 'nb2'])
    single_ints_source = database.source("single_ints", ["id", "nb1"])
    single_deci1_source = database.source("single_deci1", ["id", "nb1"])
    angle_ranges_source = database.source("angle_ranges", ["id", "nb1", "nb2"])
    int_deci_clever_pairs_source = database.source("int_deci_clever_pairs",
                                                   ["id", "nb1", "nb2"])
    order_of_operations_variants_source = database.source(
        'order_of_operations_variants', ['id', 'nb1'])
    unitspairs_source = database.source('units_conversions',
                                        ['id', 'unit1', 'unit2',
                                         'direction', 'category',
                                         'level'])
    decimals_source = database.source('decimals', ['id', 'nb1'])
    digits_places_source = database.source('digits_places', ['id', 'place'])
    fracdigits_places_source = database.source('fracdigits_places',
                                               ['id', 'place'])
    dvipsnames_selection_source = database.source('dvipsnames_selection',
                                                  ['id', 'color_name'])
    ls_marks_source = database.source('ls_marks', ['id', 'mark'])
    polygons_source = database.source('polygons',
                                      ['id', 'sides_nb', 'type', 'special',
                                       'codename', 'sides_particularity',
                                       'level', 'variant', 'table2', 'table3',
                                       'table4', 'table5', 'table6'],
                                      db=shapes_db)
    scalene_triangle_shapes_source = database.source('scalene_triangle_shapes',
                                                     ['id', 'shape_nb'],
                                                     db=shapes_db)
    right_triangle_shapes_source = database.source('right_triangle_shapes',
                                                   ['id', 'shape_nb'],
                                                   db=shapes_db)
    isosceles_triangle_shapes_source = database.source(
        'isosceles_triangle_shapes', ['id', 'shape_nb'], db=shapes_db)
    equilateral_triangle_shapes_source = database.source(
        'equilateral_triangle_shapes', ['id', 'shape_nb'], db=shapes_db)

    markup = latex.MARKUP

    from mathmaker.lib.tools.database import sub_source, mc_source
    from mathmaker.lib.tools.database import generate_random_decimal_nb
    extdecimals_source = sub_source('extdecimals', ondemand=True,
                                    generator_fct=generate_random_decimal_nb)
    alternate_source = sub_source('alternate')
    # alternate_source2 = sub_source('alternate2')
    trigo_functions_source = sub_source('trigo_functions')
    trigo_vocabulary_source = sub_source('trigo_vocabulary')
    int_fracs_source = sub_source('int_irreducible_frac')
    deci_10_100_1000_multi_source = sub_source(
        'decimal_and_10_100_1000_for_multi')
    deci_10_100_1000_divi_source = sub_source(
        'decimal_and_10_100_1000_for_divi')
    deci_one_digit_multi_source = sub_source(
        'decimal_and_one_digit_for_multi')
    deci_one_digit_divi_source = sub_source(
        'decimal_and_one_digit_for_divi')
    mc_source = mc_source()

    try:
        machine = LaTeX(settings.language)
    except TypeError:
        log.error('An exception occured while creating the LaTeX machine.',
                  exc_info=True)
        raise RuntimeError('Could not create the machine object! '
                           'Check logfile')

    number_of_the_question = 0
