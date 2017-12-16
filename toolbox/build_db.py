#!/usr/bin/env python3
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

"""
This script adds new entries to the database.

It actually erases the database and builds it entirely.
It will add all entries:
- from files mini_pb_addi_direct.yaml, mini_pb_divi_direct.yaml,
  mini_pb_subtr_direct.yaml and mini_pb_multi_direct.yaml from data/wordings/,
- from all w3l.po files from locale/*/LC_MESSAGES/
- from all w4l.po files from locale/*/LC_MESSAGES/
- from all w5l.po files from locale/*/LC_MESSAGES/
- from all *_names.po files from locale/*/LC_MESSAGES/
- all single ints from 2 to SINGLEINTS_MAX
- all single decimal numbers with one digit from 0.0 to 100.0
- all integers pairs from 2 to INTPAIRS_MAX
- all integers triples from 2 to INTPAIRS_MAX
- a list of "clever" couples of (integer, decimal) (for multiplications)
- a list of angles' ranges (around 0, 90, 180, 270)
- the list of variants identification numbers (from 0 to 23 and 100 to 155,
  so far) for order_of_operations questions
- all unit conversions, sorted in categories and levels,
- decimals from 0.001 to 9.999
- digits positions: one table for thousands to thousandths, another for
  tenths to thousandths.
- simple fractions: 1/2 to 1/10, 2/3 to 2/10 etc. until 9/10
- dvipsnames_selection for LaTeX package 'xcolor'
- polygons shapes
"""

import os
import sys
import json
import sqlite3
from math import gcd
from decimal import Decimal

from mathmakerlib.calculus import Number

from mathmaker import settings
from mathmaker.lib.tools import po_file_get_list_of, check_unique_letters_words
from mathmaker.lib.tools.frameworks import get_attributes
from mathmaker.lib.tools.database import parse_sql_creation_query
from mathmaker.lib.constants.numeration import DIGITSPLACES
from mathmaker.lib.constants.numeration import DIGITSPLACES_DECIMAL

INTPAIRS_MAX = 1000
INTTRIPLES_MAX = 200
INTQUADRUPLES_MAX = 50
SINGLEINTS_MAX = 1000


def _suits_for_deci1(i, j):
    return not(i % 10 == 0 and j % 10 == 0)


def _suits_for_deci2(i, j):
    return not(i % 10 == 0 or j % 10 == 0)


def _code(*numbers):
    """Identifies a tuple of numbers depending on its composition."""
    already_found = []
    code = []
    for n in numbers:
        if n not in already_found:
            already_found.append(n)
            code.append(numbers.count(n))
    code.sort(reverse=True)
    return '_'.join([str(_) for _ in code])


def __main__():
    settings.init()

    WORDINGS_DIR = settings.datadir + "wordings/"
    WORDINGS_FILES = [WORDINGS_DIR + n + ".yaml"
                      for n in ["mini_pb_addi_direct",
                                "mini_pb_divi_direct",
                                "mini_pb_subtr_direct",
                                "mini_pb_multi_direct"]]

    # Existent db is deleted. A brand new empty db is created.
    if os.path.isfile(settings.path.db_dist):
        sys.stderr.write('Remove previous database...\n')
        os.remove(settings.path.db_dist)
    if os.path.isfile(settings.path.shapes_db_dist):
        sys.stderr.write('Remove previous shapes database...\n')
        os.remove(settings.path.shapes_db_dist)
    sys.stderr.write('Create new databases...\n')
    open(settings.path.db_dist, 'a').close()
    open(settings.path.shapes_db_dist, 'a').close()
    sys.stderr.write('Connect to databases...\n')
    db = sqlite3.connect(settings.path.db_dist)
    shapes_db = sqlite3.connect(settings.path.shapes_db_dist)

    sys.stderr.write('Create tables...\n')
    # Creation of the tables
    db_creation_queries = \
        ['''CREATE TABLE w3l
            (id INTEGER PRIMARY KEY, language TEXT, word TEXT,
             drawDate INTEGER)''',
         '''CREATE TABLE w4l
            (id INTEGER PRIMARY KEY, language TEXT, word TEXT,
             drawDate INTEGER)''',
         '''CREATE TABLE w5l
            (id INTEGER PRIMARY KEY, language TEXT, word TEXT,
             drawDate INTEGER)''',
         '''CREATE TABLE names
            (id INTEGER PRIMARY KEY, language TEXT, gender TEXT, name TEXT,
             drawDate INTEGER)''',
         '''CREATE TABLE mini_pb_wordings
            (id INTEGER PRIMARY KEY, wording_context TEXT, wording TEXT,
             nb1_min INTEGER, nb1_max INTEGER,
             nb2_min INTEGER, nb2_max INTEGER,
             back_to_unit TEXT, q_id TEXT, drawDate INTEGER)''',
         '''CREATE TABLE single_ints
            (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''',
         # DECIMAL(4, 1) stands for up to 4 integer digits, up to 1 fractional
         # digit but these values may have no effect (purpose is only
         # documentation)
         '''CREATE TABLE single_deci1
            (id INTEGER PRIMARY KEY, nb1 DECIMAL(4, 1), drawDate INTEGER)''',
         '''CREATE TABLE angle_ranges
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             drawDate INTEGER)''',
         '''CREATE TABLE units_conversions
            (id INTEGER PRIMARY KEY, unit1 TEXT, unit2 TEXT, direction TEXT,
             category TEXT, level INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE int_pairs
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             lock_equal_products INTEGER, drawDate INTEGER, clever INTEGER,
             suits_for_deci1 INTEGER, suits_for_deci2 INTEGER)''',
         '''CREATE TABLE int_triples
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
             code TEXT, triangle INTEGER, isosceles INTEGER,
             equilateral INTEGER, pythagorean INTEGER, equal_sides INTEGER,
             drawDate INTEGER)''',
         '''CREATE TABLE simple_fractions
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             reducible INTEGER, drawDate INTEGER)''',
         # As int_deci_clever_pairs may be 'unioned' with int_pairs, its ids
         # will be determined starting from the max id of int_pairs, in order
         # to have unique ids over the two tables.
         '''CREATE TABLE int_deci_clever_pairs
            (id INTEGER, nb1 FLOAT, nb2 FLOAT, drawDate INTEGER,
             clever INTEGER)''',
         '''CREATE TABLE order_of_operations_variants
            (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''',
         # DECIMAL(2, 3) stands for up to 2 integer digits,
         # up to 3 fractional digits
         # but these values may have no effect (purpose is only documentation)
         # nz stands for "Non Zero digits (number)"
         # iz stands for "Isolated Zeros (number)"
         # fd stands for "Fractional Digits (number)"
         '''CREATE TABLE decimals
            (id INTEGER PRIMARY KEY, nb1 DECIMAL(2, 3), nz INTEGER,
             iz INTEGER, fd INTEGER, overlap_level INTEGER,
             pure_half INTEGER, pure_quarter INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE digits_places
            (id INTEGER PRIMARY KEY, place DECIMAL(4, 3), drawDate INTEGER)''',
         '''CREATE TABLE fracdigits_places
            (id INTEGER PRIMARY KEY, place DECIMAL(4, 3), drawDate INTEGER)''',
         '''CREATE TABLE dvipsnames_selection
            (id INTEGER PRIMARY KEY, color_name TEXT, drawDate INTEGER)''',
         ]

    for qr in db_creation_queries:
        db.execute(qr)

    sys.stderr.write('Insert data from locale/*/LC_MESSAGES/*.pot files...\n')
    # Extract data from po(t) files and insert them into the db
    for lang in next(os.walk(settings.localedir))[1]:
        settings.language = lang
        for n in [3, 4, 5]:
            if os.path.isfile(settings.localedir + lang
                              + "/LC_MESSAGES/w{}l.po".format(str(n))):
                words = po_file_get_list_of('words', lang, n)
                check_unique_letters_words(words, n)
                db_rows = list(zip([lang for _ in range(len(words))],
                                   words,
                                   [0 for _ in range(len(words))]))
                db.executemany(
                    "INSERT INTO w{}l(language, word, drawDate) "
                    "VALUES(?, ?, ?)".format(str(n)),
                    db_rows)

        for gender in ["masculine", "feminine"]:
            if os.path.isfile(settings.localedir + lang
                              + "/LC_MESSAGES/" + gender + "_names.po"):
                # __
                names = po_file_get_list_of('names', lang, gender)
                db_rows = list(zip([lang for _ in range(len(names))],
                                   [gender for _ in range(len(names))],
                                   names,
                                   [0 for _ in range(len(names))]))
                db.executemany("INSERT "
                               "INTO names(language, gender, name, drawDate) "
                               "VALUES(?, ?, ?, ?)",
                               db_rows)

    sys.stderr.write(
        'Insert data from data/frameworks/wordings/*.yaml files...\n')
    # Extract data from yaml files and insert them into the db
    for f in WORDINGS_FILES:
        wordings = get_attributes(f, "wording")
        db_rows = list(zip([w['wording_context'] for w in wordings],
                           [w['wording'] for w in wordings],
                           [w['nb1_min'] for w in wordings],
                           [w['nb1_max'] for w in wordings],
                           [w['nb2_min'] for w in wordings],
                           [w['nb2_max'] for w in wordings],
                           [w['back_to_unit'] for w in wordings],
                           [w['q_id'] for w in wordings],
                           [0 for _ in range(len(wordings))]))
        db.executemany("INSERT "
                       "INTO mini_pb_wordings(wording_context, wording, "
                       "nb1_min, nb1_max, nb2_min, nb2_max, back_to_unit, "
                       "q_id, drawDate) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       db_rows)

    sys.stderr.write('Insert integers pairs...')
    # Tables of 1, 2, 3... INTPAIRS_MAX
    db_rows = [(i + 1, j + 1, 0, 0, 0,
                _suits_for_deci1(i + 1, j + 1),
                _suits_for_deci2(i + 1, j + 1))
               for i in range(INTPAIRS_MAX)
               for j in range(INTPAIRS_MAX)
               if j >= i]
    for i in range(100):
        sys.stderr.write('\rInsert integers pairs... {} %'.format(i))
        db.executemany("INSERT "
                       "INTO int_pairs(nb1, nb2, lock_equal_products, "
                       "drawDate, clever, suits_for_deci1, suits_for_deci2) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?)",
                       db_rows[i * len(db_rows) // 100:
                               (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert integers pairs... 100 %\n')

    sys.stderr.write('Create integers triples...\n')
    # Tables of 1, 2, 3... INTTRIPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1,  # nb1, nb2, nb3
                _code(i + 1, j + 1, k + 1),  # code
                k + 1 < i + j + 2,  # triangle?
                (i == j and j != k) or (i == k and i != j)
                or (j == k and i != j),  # isosceles? (but not equilateral)
                i == j == k,  # equilateral?
                (k + 1) ** 2 == (i + 1) ** 2 + (j + 1) ** 2,  # pythagorean?
                (i == j or j == k or k == i),  # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(INTTRIPLES_MAX)
               for j in range(INTTRIPLES_MAX)
               for k in range(INTTRIPLES_MAX)
               if k >= j >= i and k - i <= 60]
    sys.stderr.write('Insert integers triples...')
    for i in range(100):
        sys.stderr.write('\rInsert integers triples... {} %'.format(i))
        db.executemany("INSERT "
                       "INTO int_triples(nb1, nb2, nb3, code, triangle, "
                       "isosceles, equilateral, pythagorean, equal_sides, "
                       "drawDate) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       db_rows[i * len(db_rows) // 100:
                               (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert integers triples... 100 %\n')

    creation_query = '''CREATE TABLE int_quadruples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        nb4 INTEGER, code TEXT, quadrilateral INTEGER, equilateral INTEGER,
        equal_sides INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    sys.stderr.write('Create integers quadruples...\n')
    # Tables of 1, 2, 3... INTQUADRUPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1, n + 1,  # nb1, nb2, nb3, nb4
                _code(i + 1, j + 1, k + 1, n + 1),  # code
                n + 1 < i + j + k + 3,  # quadrilateral?
                i == j == k == n,  # equilateral?
                (i == j or j == k or k == i or i == n or j == n or k == n),
                # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(INTQUADRUPLES_MAX)
               for j in range(INTQUADRUPLES_MAX)
               for k in range(INTQUADRUPLES_MAX)
               for n in range(INTQUADRUPLES_MAX)
               if n >= k >= j >= i and k - i <= 20]

    sys.stderr.write('Insert integers quadruples...')
    for i in range(100):
        sys.stderr.write('\rInsert integers quadruples... {} %'.format(i))
        db.executemany("INSERT "
                       "INTO int_quadruples(nb1, nb2, nb3, nb4, code, "
                       "quadrilateral, equilateral, equal_sides, "
                       "drawDate) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       db_rows[i * len(db_rows) // 100:
                               (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert integers quadruples... 100 %\n')
    # sys.stderr.flush()

    sys.stderr.write('Setup integers pairs: clever (5)...\n')
    for couple in [(2, 5), (2, 50), (2, 500), (5, 20), (5, 200)]:
        db.execute("UPDATE int_pairs SET clever = 5"
                   + " WHERE nb1 = '" + str(couple[0])
                   + "' and nb2 = '" + str(couple[1]) + "';")

    sys.stderr.write('Setup integers pairs: clever (4)...\n')
    for couple in [(4, 25), (4, 250)]:
        db.execute("UPDATE int_pairs SET clever = 4"
                   + " WHERE nb1 = '" + str(couple[0])
                   + "' and nb2 = '" + str(couple[1]) + "';")

    sys.stderr.write('Insert integer×decimal "clever" pairs...\n')
    # Insert integer/decimal "clever" pairs into the db
    # The tenths series (only one yet) is identified by a 10
    # the quarters series by a 4
    # the halfs/fifths series by a 5
    start_id = tuple(db.execute("SELECT MAX(id) FROM int_pairs "))[0][0] + 1
    db_rows = list(zip([i + start_id for i in range(5)],
                       [0.2, 2, 4, 4, 0.1],
                       [5, 0.5, 0.25, 2.5, 10],
                       [0, 0, 0, 0, 0],
                       [5, 5, 4, 4, 10]))

    db.executemany("INSERT "
                   "INTO int_deci_clever_pairs(id, nb1, nb2, drawDate, "
                   "clever) "
                   "VALUES(?, ?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert single integers...\n')
    # Single ints
    db_rows = [(i + 1, 0) for i in range(SINGLEINTS_MAX)]
    db.executemany("INSERT "
                   "INTO single_ints(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert simple fractions...\n')
    db_rows = [(i + 1, j + 1, 0 if gcd(i + 1, j + 1) == 1 else 1, 0)
               for i in range(10)
               for j in range(10)
               if j > i]
    db.executemany("INSERT "
                   "INTO simple_fractions(nb1, nb2, reducible, drawDate) "
                   "VALUES(?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert single decimals from 0.0 to 100.0...\n')
    # Single decimal numbers
    db_rows = [(i / 10, 0) for i in range(1001)]
    db.executemany("INSERT "
                   "INTO single_deci1(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Generate single decimals from 0.001 to 10.000...')
    # Single decimal numbers
    db_rows = []
    for j in range(100):
        sys.stderr.write(
            '\rGenerate single decimals from 0.001 to 10.000... {} %'
            .format(j))
        db_rows += [((100 * j + i + 1) / 1000,
                    Number((Decimal(100 * j + i + 1)) / Decimal(1000))
                    .nonzero_digits_nb(),
                    Number((Decimal(100 * j + i + 1)) / Decimal(1000))
                    .isolated_zeros(),
                    Number((Decimal(100 * j + i + 1)) / Decimal(1000))
                    .fracdigits_nb(),
                    Number((Decimal(100 * j + i + 1)) / Decimal(1000))
                    .overlap_level(),
                    Number((Decimal(100 * j + i + 1)) / Decimal(1000))
                    .is_pure_half(),
                    Number((Decimal(100 * j + i + 1)) / Decimal(1000))
                    .is_pure_quarter(),
                    0)
                    for i in range(100)]
    sys.stderr.write('\rGenerate single decimals from 0.001 to 10.000...'
                     ' 100 %\n')
    sys.stderr.write('Insert single decimals from 0.001 to 10.000...\n')
    db.executemany("INSERT "
                   "INTO decimals(nb1, nz, iz, fd, overlap_level, "
                   "pure_half, pure_quarter, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert angle ranges...\n')
    # Angle ranges
    db_rows = [(i - 20, i + 20, 0) for i in [0, 90, 180, 270]]
    db.executemany("INSERT "
                   "INTO angle_ranges(nb1, nb2, drawDate) "
                   "VALUES(?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert variants of order_of_operations...\n')
    # Variant numbers for order_of_operations questions.
    db_rows = [(i, 0) for i in range(24)]
    db.executemany("INSERT "
                   "INTO order_of_operations_variants"
                   "(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)
    db_rows = [(i + 100, 0) for i in range(88)]
    db.executemany("INSERT "
                   "INTO order_of_operations_variants"
                   "(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert unit conversions...\n')
    db_rows = [('km', 'hm', 'right', 'length', 1, 0),
               ('hm', 'dam', 'right', 'length', 1, 0),
               ('dam', 'm', 'right', 'length', 1, 0),
               ('m', 'dm', 'right', 'length', 1, 0),
               ('dm', 'cm', 'right', 'length', 1, 0),
               ('cm', 'mm', 'right', 'length', 1, 0),
               ('km', 'm', 'right', 'length', 1, 0),
               ('m', 'cm', 'right', 'length', 1, 0),
               ('hL', 'daL', 'right', 'capacity', 1, 0),
               ('daL', 'L', 'right', 'capacity', 1, 0),
               ('L', 'dL', 'right', 'capacity', 1, 0),
               ('dL', 'cL', 'right', 'capacity', 1, 0),
               ('cL', 'mL', 'right', 'capacity', 1, 0),
               ('hL', 'L', 'right', 'capacity', 1, 0),
               ('kg', 'hg', 'right', 'mass', 1, 0),
               ('hg', 'dag', 'right', 'mass', 1, 0),
               ('dag', 'g', 'right', 'mass', 1, 0),
               ('g', 'dg', 'right', 'mass', 1, 0),
               ('dg', 'cg', 'right', 'mass', 1, 0),
               ('cg', 'mg', 'right', 'mass', 1, 0),
               ('kg', 'g', 'right', 'mass', 1, 0),
               ('hm', 'km', 'left', 'length', 1, 0),
               ('dam', 'hm', 'left', 'length', 1, 0),
               ('m', 'dam', 'left', 'length', 1, 0),
               ('dm', 'm', 'left', 'length', 1, 0),
               ('cm', 'dm', 'left', 'length', 1, 0),
               ('mm', 'cm', 'left', 'length', 1, 0),
               ('m', 'km', 'left', 'length', 1, 0),
               ('cm', 'm', 'left', 'length', 1, 0),
               ('daL', 'hL', 'left', 'capacity', 1, 0),
               ('L', 'daL', 'left', 'capacity', 1, 0),
               ('dL', 'L', 'left', 'capacity', 1, 0),
               ('cL', 'dL', 'left', 'capacity', 1, 0),
               ('mL', 'cL', 'left', 'capacity', 1, 0),
               ('L', 'hL', 'left', 'capacity', 1, 0),
               ('hg', 'kg', 'left', 'mass', 1, 0),
               ('dag', 'hg', 'left', 'mass', 1, 0),
               ('g', 'dag', 'left', 'mass', 1, 0),
               ('dg', 'g', 'left', 'mass', 1, 0),
               ('cg', 'dg', 'left', 'mass', 1, 0),
               ('mg', 'cg', 'left', 'mass', 1, 0),
               ('g', 'kg', 'left', 'mass', 1, 0)]
    db.executemany("INSERT "
                   "INTO units_conversions"
                   "(unit1, unit2, direction, category, level, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert digits places...\n')
    db_rows = [(str(elt), 0) for elt in DIGITSPLACES]
    db.executemany("INSERT "
                   "INTO digits_places"
                   "(place, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert fractional digits places...\n')
    db_rows = [(str(elt), 0) for elt in DIGITSPLACES_DECIMAL]
    db.executemany("INSERT "
                   "INTO fracdigits_places"
                   "(place, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert dvipsnames selection...\n')
    db_rows = [('Apricot', 0), ('BurntOrange', 0), ('Dandelion', 0),
               ('Goldenrod', 0), ('Lavender', 0), ('LimeGreen', 0),
               ('NavyBlue', 0), ('Red', 0), ('SkyBlue', 0), ('Periwinkle', 0)]
    db.executemany("INSERT "
                   "INTO dvipsnames_selection(color_name, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert line segments\' marks...\n')
    creation_query = '''CREATE TABLE ls_marks
                        (id INTEGER PRIMARY KEY, mark TEXT,
                         drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    db_rows = [('|', 0), ('||', 0), ('|||', 0), ('O', 0), (r'\triangle', 0),
               (r'\square', 0), (r'\lozenge', 0), (r'\bigstar', 0)]
    db.executemany("INSERT "
                   "INTO ls_marks(mark, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    shapes_db_creation_queries = []
    sys.stderr.write('Shapes db: insert polygons...\n')
    creation_query = '''CREATE TABLE polygons
                        (id INTEGER PRIMARY KEY,
                         sides_nb INTEGER, type TEXT, special TEXT,
                         codename TEXT, sides_particularity TEXT,
                         level INTEGER, variant INTEGER,
                         table2 INTEGER, table3 INTEGER, table4 INTEGER,
                         table5 INTEGER, table6 INTEGER,
                         drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(3, 'triangle', 'scalene_triangle', 'triangle_1_1_1',
                'all_different', 2, 0, 0, 0, 0, 0, 0, 0),
               (3, 'triangle', 'right_triangle', 'triangle_1_1_1',
                'all_different', 2, 1, 0, 0, 0, 0, 0, 0),
               (3, 'triangle', 'isosceles_triangle', 'triangle_2_1', 'none',
                2, 0, 1, 0, 0, 0, 0, 0),
               (3, 'triangle', 'equilateral_triangle', 'triangle_3',
                'equilateral', 1, 0, 0, 1, 0, 0, 0, 0),
               (4, 'quadrilateral', '', 'quadrilateral_1_1_1_1',
                'all_different', 3, 0, 0, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', '', 'quadrilateral_2_1_1', 'none',
                3, 0, 1, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', '', 'quadrilateral_2_1_1', 'none',
                3, 1, 1, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', '', 'quadrilateral_2_2', 'none',
                3, 0, 1, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', '', 'quadrilateral_2_2', 'none',
                3, 1, 1, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', 'rectangle', 'quadrilateral_2_2', 'none',
                2, 2, 1, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', '', 'quadrilateral_3_1', 'none',
                2, 0, 0, 1, 0, 0, 0, 0),
               (4, 'quadrilateral', 'rhombus', 'quadrilateral_4',
                'equilateral', 1, 0, 0, 0, 1, 0, 0, 0),
               (4, 'quadrilateral', 'square', 'quadrilateral_4', 'equilateral',
                1, 1, 0, 0, 1, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_1_1_1_1_1', 'all_different',
                4, 0, 0, 0, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_2_1_1_1', 'none',
                4, 0, 1, 0, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_2_1_1_1', 'none',
                4, 1, 1, 0, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_2_2_1', 'none',
                4, 0, 1, 0, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_2_2_1', 'none',
                4, 1, 1, 0, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_2_2_1', 'none',
                4, 2, 1, 0, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_3_1_1', 'none',
                3, 0, 0, 1, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_3_1_1', 'none',
                3, 1, 0, 1, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_3_2', 'none',
                3, 0, 1, 1, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_3_2', 'none',
                3, 1, 1, 1, 0, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_4_1', 'none',
                2, 0, 0, 0, 1, 0, 0, 0),
               (5, 'pentagon', '', 'pentagon_5', 'equilateral',
                1, 0, 0, 0, 0, 1, 0, 0),
               (6, 'hexagon', '', 'hexagon_1_1_1_1_1_1', 'all_different',
                5, 0, 0, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_1_1_1_1', 'none',
                5, 0, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_1_1_1_1', 'none',
                5, 1, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_1_1_1_1', 'none',
                5, 2, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 0, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 1, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 2, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 3, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 4, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 5, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_2', 'none',
                3, 0, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_2', 'none',
                3, 1, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_2', 'none',
                3, 2, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_2', 'none',
                3, 3, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_1_1_1', 'none',
                4, 0, 0, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_1_1_1', 'none',
                4, 1, 0, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_1_1_1', 'none',
                4, 2, 0, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_2_1', 'none',
                4, 0, 1, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_2_1', 'none',
                4, 1, 1, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_2_1', 'none',
                4, 2, 1, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_2_1', 'none',
                4, 3, 1, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_3', 'none',
                3, 0, 0, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_3', 'none',
                3, 1, 0, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_3_3', 'none',
                3, 2, 0, 1, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_4_1_1', 'none',
                3, 0, 0, 0, 1, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_4_1_1', 'none',
                3, 1, 0, 0, 1, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_4_1_1', 'none',
                3, 2, 0, 0, 1, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_4_2', 'none',
                3, 0, 1, 0, 1, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_4_2', 'none',
                3, 1, 1, 0, 1, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_4_2', 'none',
                3, 2, 1, 0, 1, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_5_1', 'none',
                2, 0, 0, 0, 0, 1, 0, 0),
               (6, 'hexagon', '', 'hexagon_6', 'equilateral',
                1, 0, 0, 0, 0, 0, 1, 0)]
    shapes_db.executemany(
        "INSERT INTO polygons("
        "sides_nb, type, special, codename, sides_particularity, level, "
        "variant, table2, table3, table4, table5, table6, drawDate) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        db_rows)

    sys.stderr.write('Shapes db: insert shapes variants: scalene triangles...')
    creation_query = '''CREATE TABLE scalene_triangle_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO scalene_triangle_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles...')
    creation_query = '''CREATE TABLE right_triangle_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
    shapes_db.executemany(
        "INSERT INTO right_triangle_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles, isosceles triangles...')
    creation_query = '''CREATE TABLE isosceles_triangle_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
    shapes_db.executemany(
        "INSERT INTO isosceles_triangle_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles, isosceles triangles, equilateral '
                     'triangles...')
    creation_query = '''CREATE TABLE equilateral_triangle_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO equilateral_triangle_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles, isosceles triangles, equilateral '
                     'triangles, quadrilaterals...\n')
    creation_query = '''CREATE TABLE quadrilateral_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO quadrilateral_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('Commit changes to databases...\n')
    db.commit()
    shapes_db.commit()
    sys.stderr.write('Close databases...\n')
    db.close()
    shapes_db.close()
    sys.stderr.write('Create databases\' indices...\n')
    db_index = {}
    for qr in db_creation_queries:
        key, value = parse_sql_creation_query(qr)
        db_index.update({key: value})
    with open(settings.db_index_path, 'w') as f:
        json.dump(db_index, f, indent=4)
        f.write('\n')
    shapes_db_index = {}
    for qr in shapes_db_creation_queries:
        key, value = parse_sql_creation_query(qr)
        shapes_db_index.update({key: value})
    with open(settings.shapes_db_index_path, 'w') as f:
        json.dump(shapes_db_index, f, indent=4)
        f.write('\n')
    sys.stderr.write('Done!\n')


if __name__ == '__main__':
    __main__()
