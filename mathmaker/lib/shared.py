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
    global solids_db
    global natural_nb_tuples_db
    global unique_letters_words_source
    global names_source
    global mini_problems_wordings_source
    global mini_problems_prop_wordings_source
    global mini_problems_time_wordings_source
    global divisibility_statements_source
    global markup
    global deci_int_triples_for_prop_source
    global int_pairs_source
    global int_triples_source
    global int_quadruples_source
    global int_quintuples_source
    global int_sextuples_source
    global nnpairs_source
    global nn_deci_clever_pairs_source
    global nntriples_source
    global nnquadruples_source
    global nnquintuples_source
    global nnsextuples_source
    global simple_fractions_source
    global single_ints_source
    global single_deci1_source
    global angle_decorations_source
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
    global alternate_2masks_source
    global alternate_3masks_source
    global alternate_4masks_source
    global alternate_nb2nb3_in_mini_pb_prop_source
    global decimals_source
    global extdecimals_source
    global dvipsnames_selection_source
    global polygons_source
    global anglessets_source
    global anglessets_1_1_source
    global anglessets_1_1r_source
    global anglessets_2_source
    global anglessets_1_1_1_source
    global anglessets_1_1_1r_source
    global anglessets_2_1_source
    global anglessets_2_1r_source
    global anglessets_3_source
    global scalene_triangle_shapes_source
    global right_triangle_shapes_source
    global triangle_2_1_shapes_source
    global triangle_3_shapes_source
    global quadrilateral_1_1_1_1_shapes_source
    global quadrilateral_2_1_1_shapes_source
    global quadrilateral_2_2_shapes_source
    global quadrilateral_3_1_shapes_source
    global quadrilateral_4_shapes_source
    global pentagon_1_1_1_1_1_shapes_source
    global pentagon_2_1_1_1_shapes_source
    global pentagon_2_2_1_shapes_source
    global pentagon_3_1_1_shapes_source
    global pentagon_3_2_shapes_source
    global pentagon_4_1_shapes_source
    global pentagon_5_shapes_source
    global hexagon_1_1_1_1_1_1_shapes_source
    global hexagon_2_1_1_1_1_shapes_source
    global hexagon_2_2_1_1_shapes_source
    global hexagon_2_2_2_shapes_source
    global hexagon_3_1_1_1_shapes_source
    global hexagon_3_2_1_shapes_source
    global hexagon_3_3_shapes_source
    global hexagon_4_1_1_shapes_source
    global hexagon_4_2_shapes_source
    global hexagon_5_1_shapes_source
    global hexagon_6_shapes_source
    global rightcuboids_source
    global ls_marks_source
    global enable_js_form
    global distcodes_source
    global directions_source
    global times_source

    enable_js_form = False

    log = settings.mainlogger

    db = sqlite3.connect(settings.path.db)
    shapes_db = sqlite3.connect(settings.path.shapes_db)
    anglessets_db = sqlite3.connect(settings.path.anglessets_db)
    solids_db = sqlite3.connect(settings.path.solids_db)
    natural_nb_tuples_db = sqlite3.connect(settings.path.natural_nb_tuples_db)

    from mathmaker.lib.tools import database
    unique_letters_words_source = {}
    for n in settings.available_wNl:
        source_name = 'w{}l'.format(n)
        unique_letters_words_source.update(
            {n: database.source(source_name, ['id', 'word'],
                                language=settings.language)})
    names_source = database.source("names", ["id", "name"],
                                   language=settings.language)
    mini_problems_wordings_source = database.source("mini_pb_wordings",
                                                    ["id", "wording_context",
                                                     "wording"])
    mini_problems_prop_wordings_source = database.source(
        "mini_pb_prop_wordings", ["id", "wording_context", "wording",
                                  "nb1_xcoeff", "nb2_xcoeff", "nb3_xcoeff"])
    mini_problems_time_wordings_source = database.source(
        "mini_pb_time_wordings", ["id", "wording_context", "type", "wording",
                                  "mini_start_hour",
                                  "mini_start_minute", "maxi_start_hour",
                                  "maxi_start_minute", "mini_duration_hour",
                                  "mini_duration_minute", "maxi_duration_hour",
                                  "maxi_duration_minute", "mini_end_hour",
                                  "mini_end_minute", "maxi_end_hour",
                                  "maxi_end_minute"])
    divisibility_statements_source = database.source("divisibility_statements",
                                                     ["id", "wording"])
    deci_int_triples_for_prop_source = database.source(
        "deci_int_triples_for_prop", ["id", "coeff", "nb1", "nb2", "nb3",
                                      "solution"])

    int_pairs_source = database.source("int_pairs", ["id", "nb1", "nb2"])
    int_triples_source = database.source("int_triples",
                                         ["id", "nb1", "nb2", "nb3"])
    int_quadruples_source = database.source("int_quadruples",
                                            ["id", "nb1", "nb2", "nb3", "nb4"])
    int_quintuples_source = database.source("int_quintuples",
                                            ["id", "nb1", "nb2", "nb3", "nb4",
                                             "nb5"])
    nnpairs_source = database.source("pairs", ["id", "nb1", "nb2"],
                                     db=natural_nb_tuples_db)
    nn_deci_clever_pairs_source = database.source("nn_deci_clever_pairs",
                                                  ["id", "nb1", "nb2"])
    nntriples_source = database.source("triples", ["id", "nb1", "nb2", "nb3"],
                                       db=natural_nb_tuples_db)
    nnquadruples_source = database.source("quadruples",
                                          ["id", "nb1", "nb2", "nb3", "nb4"],
                                          db=natural_nb_tuples_db)
    nnquintuples_source = database.source("quintuples",
                                          ["id", "nb1", "nb2", "nb3", "nb4",
                                           "nb5"], db=natural_nb_tuples_db)
    nnsextuples_source = database.source("sextuples",
                                         ["id", "nb1", "nb2", "nb3", "nb4",
                                          "nb5", "nb6"],
                                         db=natural_nb_tuples_db)
    int_sextuples_source = database.source("int_sextuples",
                                           ["id", "nb1", "nb2", "nb3", "nb4",
                                            "nb5", "nb6"])
    simple_fractions_source = database.source('simple_fractions',
                                              ['id', 'nb1', 'nb2'])
    single_ints_source = database.source("single_ints", ["id", "nb1"])
    single_deci1_source = database.source("single_deci1", ["id", "nb1"])
    angle_ranges_source = database.source("angle_ranges", ["id", "nb1", "nb2"])
    angle_decorations_source = database.source(
        'angle_decorations', ['id', 'variety', 'hatchmark'])
    int_deci_clever_pairs_source = database.source("int_deci_clever_pairs",
                                                   ["id", "nb1", "nb2"])
    order_of_operations_variants_source = database.source(
        'order_of_operations_variants', ['id', 'nb1'])
    unitspairs_source = database.source('units_conversions',
                                        ['id', 'unit1', 'unit2',
                                         'direction', 'category',
                                         'level', 'dimension'])
    decimals_source = database.source('decimals', ['id', 'nb1'])
    digits_places_source = database.source('digits_places', ['id', 'place'])
    fracdigits_places_source = database.source('fracdigits_places',
                                               ['id', 'place'])
    dvipsnames_selection_source = database.source('dvipsnames_selection',
                                                  ['id', 'color_name'])
    ls_marks_source = database.source('ls_marks', ['id', 'mark'])
    distcodes_source = database.source('distcodes', ['id', 'distcode'])
    directions_source = database.source('directions', ['id', 'direction'])
    times_source = database.source('times', ['id', 'hour', 'minute'])
    anglessets_source = database.source('anglessets',
                                        ['id', 'nbof_angles', 'distcode',
                                         'variant', 'nbof_right_angles',
                                         'equal_angles', 'table2',
                                         'table3', 'table4', 'table5',
                                         'table6'],
                                        db=anglessets_db)
    anglessets_1_1_source = database.source(
        '_1_1_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_1_1r_source = database.source(
        '_1_1r_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_2_source = database.source(
        '_2_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_1_1_1_source = database.source(
        '_1_1_1_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_1_1_1r_source = database.source(
        '_1_1_1r_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_2_1_source = database.source(
        '_2_1_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_2_1r_source = database.source(
        '_2_1r_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
    anglessets_3_source = database.source(
        '_3_subvariants', ['id', 'subvariant_nb'], db=anglessets_db)
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
    triangle_2_1_shapes_source = database.source(
        'triangle_2_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    triangle_3_shapes_source = database.source(
        'triangle_3_shapes', ['id', 'shape_nb'], db=shapes_db)
    quadrilateral_1_1_1_1_shapes_source = database.source(
        'quadrilateral_1_1_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    quadrilateral_2_1_1_shapes_source = database.source(
        'quadrilateral_2_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    quadrilateral_2_2_shapes_source = database.source(
        'quadrilateral_2_2_shapes', ['id', 'shape_nb'], db=shapes_db)
    quadrilateral_3_1_shapes_source = database.source(
        'quadrilateral_3_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    quadrilateral_4_shapes_source = database.source(
        'quadrilateral_4_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_1_1_1_1_1_shapes_source = database.source(
        'pentagon_1_1_1_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_2_1_1_1_shapes_source = database.source(
        'pentagon_2_1_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_2_2_1_shapes_source = database.source(
        'pentagon_2_2_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_3_1_1_shapes_source = database.source(
        'pentagon_3_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_3_2_shapes_source = database.source(
        'pentagon_3_2_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_4_1_shapes_source = database.source(
        'pentagon_4_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    pentagon_5_shapes_source = database.source(
        'pentagon_5_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_1_1_1_1_1_1_shapes_source = database.source(
        'hexagon_1_1_1_1_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_2_1_1_1_1_shapes_source = database.source(
        'hexagon_2_1_1_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_2_2_1_1_shapes_source = database.source(
        'hexagon_2_2_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_2_2_2_shapes_source = database.source(
        'hexagon_2_2_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_3_1_1_1_shapes_source = database.source(
        'hexagon_3_1_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_3_2_1_shapes_source = database.source(
        'hexagon_3_2_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_3_3_shapes_source = database.source(
        'hexagon_3_3_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_4_1_1_shapes_source = database.source(
        'hexagon_4_1_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_4_2_shapes_source = database.source(
        'hexagon_4_2_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_5_1_shapes_source = database.source(
        'hexagon_5_1_shapes', ['id', 'shape_nb'], db=shapes_db)
    hexagon_6_shapes_source = database.source(
        'hexagon_6_shapes', ['id', 'shape_nb'], db=shapes_db)
    rightcuboids_source = database.source(
        'polyhedra', ['id', 'faces_nb', 'variant'],
        db=solids_db)

    markup = latex.MARKUP

    from mathmaker.lib.tools.database import sub_source, mc_source
    from mathmaker.lib.tools.database import generate_random_decimal_nb
    extdecimals_source = sub_source('extdecimals', ondemand=True,
                                    generator_fct=generate_random_decimal_nb)
    alternate_source = sub_source('alternate')
    alternate_2masks_source = sub_source('alternate_2masks')
    alternate_3masks_source = sub_source('alternate_3masks')
    alternate_4masks_source = sub_source('alternate_4masks')
    alternate_nb2nb3_in_mini_pb_prop_source = \
        sub_source('alternate_nb2nb3_in_mini_pb_prop')
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
