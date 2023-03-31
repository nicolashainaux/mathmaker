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
- proper fractions: 1/2 to 1/10, 2/3 to 2/10 etc. until 9/10
- improper fractions: 2/2, 3/2, ... to 99/2, 3/3, 4/3... to 99/3 etc. until
  99/10
- dvipsnames_selection for LaTeX package 'xcolor'
- polygons shapes
- some more (check the db)
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
from mathmaker.lib.tools.distcode import distcode
from mathmaker.lib.tools.database import parse_sql_creation_query
from mathmaker.lib.constants.numeration import DIGITSPLACES
from mathmaker.lib.constants.numeration import DIGITSPLACES_DECIMAL

INTPAIRS_MAX = 1000
INTTRIPLES_MAX = 200
INTQUADRUPLES_MAX = 50
INTQUINTUPLES_MAX = 36
INTSEXTUPLES_MAX = 25
SINGLEINTS_MAX = 1000

NNSINGLETONS_MAX = 100
NNPAIRS_MAX = 100
NNTRIPLES_MAX = 10
NNQUADRUPLES_MAX = 10
NNQUINTUPLES_MAX = 10
NNSEXTUPLES_MAX = 10

COORD_MAX = 100


def _suits_for_deci1(i, j):
    return not (i % 10 == 0 and j % 10 == 0)


def _suits_for_deci2(i, j):
    return not (i % 10 == 0 or j % 10 == 0)


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
    if os.path.isfile(settings.path.solids_db_dist):
        sys.stderr.write('Remove previous shapes database...\n')
        os.remove(settings.path.solids_db_dist)
    if os.path.isfile(settings.path.anglessets_db_dist):
        sys.stderr.write('Remove previous anglessets database...\n')
        os.remove(settings.path.anglessets_db_dist)
    if os.path.isfile(settings.path.natural_nb_tuples_db_dist):
        sys.stderr.write('Remove previous inttuples database...\n')
        os.remove(settings.path.natural_nb_tuples_db_dist)
    sys.stderr.write('Create new databases...\n')
    open(settings.path.db_dist, 'a').close()
    open(settings.path.shapes_db_dist, 'a').close()
    open(settings.path.solids_db_dist, 'a').close()
    open(settings.path.anglessets_db_dist, 'a').close()
    open(settings.path.natural_nb_tuples_db_dist, 'a').close()
    sys.stderr.write('Connect to databases...\n')
    db = sqlite3.connect(settings.path.db_dist)
    shapes_db = sqlite3.connect(settings.path.shapes_db_dist)
    solids_db = sqlite3.connect(settings.path.solids_db_dist)
    anglessets_db = sqlite3.connect(settings.path.anglessets_db_dist)
    natural_nb_tuples_db = sqlite3.connect(
        settings.path.natural_nb_tuples_db_dist)

    natural_nb_tuples_db_creation_queries = []

    sys.stderr.write('Create tables...\n')
    # Creation of the tables
    db_creation_queries = ['''CREATE TABLE w{}l
        (id INTEGER PRIMARY KEY, language TEXT, word TEXT,
         drawDate INTEGER)'''.format(n) for n in settings.available_wNl]
    db_creation_queries += \
        ['''CREATE TABLE angle_decorations
            (id INTEGER PRIMARY KEY, variety TEXT, hatchmark TEXT,
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
             category TEXT, level INTEGER, easiest TEXT, dimension INTEGER,
             drawDate INTEGER)''',
         '''CREATE TABLE int_pairs
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             lock_equal_products INTEGER, drawDate INTEGER, clever INTEGER,
             suits_for_deci1 INTEGER, suits_for_deci2 INTEGER)''',
         '''CREATE TABLE int_triples
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
             code TEXT, triangle INTEGER, isosceles INTEGER,
             equilateral INTEGER, pythagorean INTEGER, equal_sides INTEGER,
             drawDate INTEGER)''',
         '''CREATE TABLE simple_proper_fractions
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             reducible INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE simple_improper_fractions
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             reducible INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE improper_fractions
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             reducible INTEGER, mod INTEGER, deci DECIMAL(4, 1),
             drawDate INTEGER)''',
         # As int_deci_clever_pairs may be 'unioned' with int_pairs, its ids
         # will be determined starting from the max id of int_pairs, in order
         # to have unique ids over the two tables.
         '''CREATE TABLE int_deci_clever_pairs
            (id INTEGER, nb1 FLOAT, nb2 FLOAT, drawDate INTEGER,
             clever INTEGER)''',
         '''CREATE TABLE order_of_operations_variants
            (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE signed_nb_comparisons
            (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE expressions
            (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''',
         '''CREATE TABLE cols_for_spreadsheets
            (id INTEGER PRIMARY KEY, col TEXT, drawDate INTEGER)''',
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
         '''CREATE TABLE coordinates_xy
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             drawDate INTEGER)''',
         ]

    for qr in db_creation_queries:
        db.execute(qr)

    sys.stderr.write('Insert data from locale/*/LC_MESSAGES/*.pot files...\n')
    # Extract data from po(t) files and insert them into the db
    for lang in next(os.walk(settings.localedir))[1]:
        settings.language = lang
        for n in settings.available_wNl:
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

    sys.stderr.write('Insert angles\'s decorations...\n')
    db_rows = [('single', 'singledash', 0),
               ('single', 'doubledash', 0),
               ('single', 'tripledash', 0),
               ('double', None, 0),
               ('double', 'singledash', 0),
               ('triple', None, 0),
               ('triple', 'singledash', 0),
               ]
    db.executemany("INSERT "
                   "INTO angle_decorations"
                   "(variety, hatchmark, drawDate) "
                   "VALUES(?, ?, ?)",
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

    creation_query = '''CREATE TABLE mini_pb_prop_wordings
                        (id INTEGER PRIMARY KEY, wid INTEGER,
                         wording_context TEXT, wording TEXT,
                         coeff_min INTEGER, coeff_max INTEGER,
                         nb1_min INTEGER, nb1_max INTEGER,
                         nb2_min INTEGER, nb2_max INTEGER,
                         nb3_min INTEGER, nb3_max INTEGER,
                         solution_min INTEGER, solution_max INTEGER,
                         nb1_xcoeff INTEGER, nb2_xcoeff INTEGER,
                         nb3_xcoeff INTEGER,
                         nb1_may_be_deci INTEGER, nb2_may_be_deci INTEGER,
                         nb3_may_be_deci INTEGER, solution_may_be_deci INTEGER,
                         locked INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    PROP_WORDINGS_FILE = WORDINGS_DIR + 'mini_pb_proportionality' + '.yaml'
    wordings = get_attributes(PROP_WORDINGS_FILE, "wording")
    db_rows = list(zip([i + 1 for i in range(len(wordings))],
                       [w.get('wording_context') for w in wordings],
                       [w.get('wording') for w in wordings],
                       [w.get('coeff_min', 0) for w in wordings],
                       [w.get('coeff_max', 10000) for w in wordings],
                       [w.get('nb1_min', 0) for w in wordings],
                       [w.get('nb1_max', 1000) for w in wordings],
                       [w.get('nb2_min', 0) for w in wordings],
                       [w.get('nb2_max', 1000) for w in wordings],
                       [w.get('nb3_min', 0) for w in wordings],
                       [w.get('nb3_max', 10000) for w in wordings],
                       [w.get('solution_min', 0) for w in wordings],
                       [w.get('solution_max', 10000) for w in wordings],
                       [w.get('nb1_xcoeff', 1) for w in wordings],
                       [w.get('nb2_xcoeff', 1) for w in wordings],
                       [w.get('nb3_xcoeff', 1) for w in wordings],
                       [w.get('nb1_may_be_deci', 0) for w in wordings],
                       [w.get('nb2_may_be_deci', 0) for w in wordings],
                       [w.get('nb3_may_be_deci', 0) for w in wordings],
                       [w.get('solution_may_be_deci', 0) for w in wordings],
                       [0 for _ in range(len(wordings))],
                       [0 for _ in range(len(wordings))]))
    db.executemany("INSERT "
                   "INTO mini_pb_prop_wordings(wid, wording_context, wording, "
                   "coeff_min, coeff_max, nb1_min, nb1_max, nb2_min, nb2_max, "
                   "nb3_min, nb3_max, solution_min, solution_max, "
                   "nb1_xcoeff, nb2_xcoeff, nb3_xcoeff, "
                   "nb1_may_be_deci, nb2_may_be_deci, "
                   "nb3_may_be_deci, solution_may_be_deci, "
                   "locked, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                   "?, ?, ?, ?, ?)",
                   db_rows)

    creation_query = '''CREATE TABLE mini_pb_time_wordings
                        (id INTEGER PRIMARY KEY, wid INTEGER,
                         wording_context TEXT, type TEXT, wording TEXT,
                         mini_start_hour INTEGER, mini_start_minute INTEGER,
                         maxi_start_hour INTEGER, maxi_start_minute INTEGER,
                         mini_duration_hour INTEGER,
                         mini_duration_minute INTEGER,
                         maxi_duration_hour INTEGER,
                         maxi_duration_minute INTEGER,
                         mini_end_hour INTEGER, mini_end_minute INTEGER,
                         maxi_end_hour INTEGER, maxi_end_minute INTEGER,
                         locked, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    TIME_WORDINGS_FILE = WORDINGS_DIR + 'mini_pb_time' + '.yaml'
    wordings = get_attributes(TIME_WORDINGS_FILE, 'wording')
    db_rows = list(zip([i + 1 for i in range(len(wordings))],
                       [w.get('wording_context') for w in wordings],
                       [w.get('type') for w in wordings],
                       [w.get('wording') for w in wordings],
                       [w.get('mini_start_hour') for w in wordings],
                       [w.get('mini_start_minute') for w in wordings],
                       [w.get('maxi_start_hour') for w in wordings],
                       [w.get('maxi_start_minute') for w in wordings],
                       [w.get('mini_duration_hour') for w in wordings],
                       [w.get('mini_duration_minute') for w in wordings],
                       [w.get('maxi_duration_hour') for w in wordings],
                       [w.get('maxi_duration_minute') for w in wordings],
                       [w.get('mini_end_hour') for w in wordings],
                       [w.get('mini_end_minute') for w in wordings],
                       [w.get('maxi_end_hour') for w in wordings],
                       [w.get('maxi_end_minute') for w in wordings],
                       [0 for _ in range(len(wordings))],
                       [0 for _ in range(len(wordings))]))
    db.executemany("INSERT "
                   "INTO mini_pb_time_wordings(wid, wording_context, type, "
                   "wording, "
                   "mini_start_hour, mini_start_minute, maxi_start_hour, "
                   "maxi_start_minute, mini_duration_hour,"
                   "mini_duration_minute, maxi_duration_hour, "
                   "maxi_duration_minute, mini_end_hour, mini_end_minute, "
                   "maxi_end_hour, maxi_end_minute, locked, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                   "?, ?)",
                   db_rows)

    creation_query = '''CREATE TABLE divisibility_statements
                        (id INTEGER PRIMARY KEY, wid INTEGER,
                         wording TEXT, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    wordings = get_attributes(WORDINGS_DIR + 'divisibility_statements.yaml',
                              'wording')
    db_rows = list(zip([i + 1 for i in range(len(wordings))],
                       [w.get('wording') for w in wordings],
                       [0 for _ in range(len(wordings))]))
    db.executemany("INSERT "
                   "INTO divisibility_statements"
                   "(wid, wording, drawDate) "
                   "VALUES(?, ?, ?)",
                   db_rows)

    creation_query = '''CREATE TABLE distcodes
                        (id INTEGER PRIMARY KEY, nbof_nb INTEGER,
                         distcode TEXT, equilateral INTEGER,
                         equal_sides INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    db_rows = [(2, '2', 1, 1, 0),
               (2, '1_1', 0, 0, 0),
               (3, '3', 1, 1, 0),
               (3, '2_1', 0, 1, 0),
               (3, '1_1_1', 0, 0, 0),
               (4, '4', 1, 1, 0),
               (4, '3_1', 0, 1, 0),
               (4, '2_2', 0, 1, 0),
               (4, '2_1_1', 0, 1, 0),
               (4, '1_1_1_1', 0, 0, 0),
               (5, '5', 1, 1, 0),
               (5, '4_1', 0, 1, 0),
               (5, '3_2', 0, 1, 0),
               (5, '3_1_1', 0, 1, 0),
               (5, '2_2_1', 0, 1, 0),
               (5, '2_1_1_1', 0, 1, 0),
               (5, '1_1_1_1_1', 0, 0, 0),
               (6, '6', 1, 1, 0),
               (6, '5_1', 0, 1, 0),
               (6, '4_2', 0, 1, 0),
               (6, '4_1_1', 0, 1, 0),
               (6, '3_3', 0, 1, 0),
               (6, '3_2_1', 0, 1, 0),
               (6, '3_1_1_1', 0, 1, 0),
               (6, '2_2_2', 0, 1, 0),
               (6, '2_2_1_1', 0, 1, 0),
               (6, '2_1_1_1_1_1', 0, 1, 0),
               (6, '1_1_1_1_1_1', 0, 0, 0)]
    db.executemany("INSERT "
                   "INTO distcodes"
                   "(nbof_nb, distcode, equilateral, equal_sides, drawDate) "
                   "VALUES(?, ?, ?, ? , ?)",
                   db_rows)

    creation_query = '''CREATE TABLE directions
                        (id INTEGER PRIMARY KEY, direction TEXT,
                         drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    db_rows = [('top-right', 0),
               ('top-left', 0),
               ('bottom-left', 0),
               ('bottom-right', 0)]
    db.executemany("INSERT "
                   "INTO directions"
                   "(direction, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    creation_query = '''CREATE TABLE multiplesof10
                        (id INTEGER PRIMARY KEY, factor1 INTEGER,
                         factor2 INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    db_rows = [(1, 10, 0),
               (1, 100, 0),
               (1, 1000, 0),
               (10, 10, 0),
               (10, 100, 0)]
    db.executemany("INSERT "
                   "INTO multiplesof10"
                   "(factor1, factor2, drawDate) "
                   "VALUES(?, ?, ?)",
                   db_rows)

    creation_query = '''CREATE TABLE times
                        (id INTEGER PRIMARY KEY, hour INTEGER, minute INTEGER,
                         drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    db_rows = [(hour, minute, 0) for hour in range(24) for minute in range(60)]
    db.executemany("INSERT "
                   "INTO times"
                   "(hour, minute, drawDate) "
                   "VALUES(?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert mixed decimals and ints triples for '
                     'proportionality...\n')
    integers = [_ for _ in range(2, 32)]
    integers.append(50)
    integers.append(60)
    integers.append(80)
    integers.append(100)
    db_rows = [(0.666667, n1, n2,
                float((Number('0.666667') * n1).rounded(Number('0.01'))),
                float((Number('0.666667') * n2).rounded(Number('0.01'))), 0, 0)
               for n1 in integers if n1 % 3 == 0
               for n2 in integers
               if n2 != n1 and n2 % n1 != 0 and n2 > n1 / 2 and n2 % 3 == 0]
    db_rows += [(0.75, n1, n2, float(Number('0.75') * n1),
                 float(Number('0.75') * n2), 0, 0)
                for n1 in integers if n1 % 4 == 0
                for n2 in integers
                if n2 != n1 and n2 % n1 and n2 > n1 / 2 and n2 % 4 == 0]
    db_rows += [(1.125, n1, n2, float(Number('1.125') * n1),
                 float(Number('1.125') * n2), 0, 0)
                for n1 in integers if n1 % 8 == 0 and n1 > 8
                for n2 in integers if n2 != n1 and n2 % n1 and n2 > n1 / 2
                and n2 % 8 != 0 and n2 % 4 == 0]
    db_rows += [(1.2, n1, n2, float(Number('1.2') * n1),
                 float(Number('1.2') * n2), 0, 0)
                for n1 in integers if n1 % 5 == 0
                for n2 in integers
                if n2 != n1 and n2 % n1 != 0 and n2 > n1 / 2 and n2 % 5 == 0]
    db_rows += [(1.25, n1, n2, float(Number('1.25') * n1),
                 float(Number('1.25') * n2), 0, 0)
                for n1 in integers if n1 % 4 == 0
                for n2 in integers if n2 != n1 and n2 > n1 / 2 and n2 % 4 != 0
                and n2 % 2 == 0 and n2 % n1]
    db_rows += [(1.25, n1, n2, float(Number('1.25') * n1),
                 float(Number('1.25') * n2), 0, 0)
                for n1 in integers if n1 % 4 == 0
                for n2 in integers if n2 != n1 and n2 > n1 / 2 and n2 % 4 == 0
                and n2 >= 41 and n2 % n1]
    db_rows += [(1.333333, n1, n2,
                float((Number('1.333333') * n1).rounded(Number('0.01'))),
                float((Number('1.333333') * n2).rounded(Number('0.01'))), 0, 0)
                for n1 in integers if n1 % 3 == 0
                for n2 in integers
                if n2 != n1 and n2 % n1 != 0 and n2 > n1 / 2 and n2 % 3 == 0]
    db_rows += [(1.5, n1, n2, float(Number('1.5') * n1),
                 float(Number('1.5') * n2), 0, 0)
                for n1 in integers
                if n1 < 7 or (8 <= n1 <= 24 and n1 % 2 == 0)
                or (n1 >= 30 and n1 % 10 == 0)
                for n2 in integers
                if n2 != n1 and n2 % n1 and n2 > n1 / 2]
    db_rows += [(c, 1.5, n2, float(c * Number('1.5')), float(c * n2), 0, 0)
                for c in [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40,
                          50, 60, 80, 100]
                for n2 in integers
                if n2 != c and n2 > c / 2]
    db_rows += [(2.5, n1, n2, float(Number('2.5') * n1),
                 float(Number('2.5') * n2), 0, 0)
                for n1 in integers if n1 <= 10 or (n1 > 10 and n1 % 10 == 0)
                if not ((n1 >= 12 and n1 % 10 != 0) or n1 in [7, 9])
                for n2 in integers
                if n2 != n1 and n2 % n1 and n2 > n1 / 2 and n2 % 2 != 0]
    db_rows += [(c, 2.5, n2, float(c * Number('2.5')), float(c * n2), 0, 0)
                for c in [2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50, 60, 80, 100]
                for n2 in integers
                if n2 != c and n2 > c / 2]
    creation_query = '''CREATE TABLE deci_int_triples_for_prop
                        (id INTEGER PRIMARY KEY, coeff DECIMAL(1, 6),
                         nb1 DECIMAL(1, 6), nb2 DECIMAL(1, 6),
                         nb3 DECIMAL(1, 6), solution DECIMAL(1, 6),
                         locked INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    db.executemany("INSERT "
                   "INTO deci_int_triples_for_prop(coeff, nb1, nb2, "
                   "nb3, solution, locked, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?)",
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
    db_rows = [(15, 2, 3, 'none', 0, 0, 0, 0, 0, 0),
               (15, 2, 5, 'none', 0, 0, 0, 0, 0, 0),
               (15, 2, 6, 'none', 0, 0, 0, 0, 0, 0),
               (15, 3, 4, 'none', 0, 0, 0, 0, 0, 0),
               (15, 3, 5, 'none', 0, 0, 0, 0, 0, 0),
               (15, 4, 5, 'none', 0, 0, 0, 0, 0, 0),
               (15, 4, 6, 'none', 0, 0, 0, 0, 0, 0),
               (15, 5, 6, 'none', 0, 0, 0, 0, 0, 0),
               (25, 2, 3, 'none', 0, 0, 0, 0, 0, 0),
               (25, 2, 5, 'none', 0, 0, 0, 0, 0, 0),
               (25, 2, 6, 'none', 0, 0, 0, 0, 0, 0),
               (25, 3, 4, 'none', 0, 0, 0, 0, 0, 0),
               (25, 3, 5, 'none', 0, 0, 0, 0, 0, 0),
               (25, 4, 5, 'none', 0, 0, 0, 0, 0, 0),
               (25, 4, 6, 'none', 0, 0, 0, 0, 0, 0),
               (25, 5, 6, 'none', 0, 0, 0, 0, 0, 0)]
    db_rows += [(i + 1, j + 1, k + 1,  # nb1, nb2, nb3
                 distcode(i + 1, j + 1, k + 1),  # code
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
                if k >= j >= i and k - i <= 30]
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
                distcode(i + 1, j + 1, k + 1, n + 1),  # code
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
               if n >= k >= j >= i and n - i <= 18]

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

    creation_query = '''CREATE TABLE int_quintuples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        nb4 INTEGER, nb5 INTEGER, code TEXT, pentagon INTEGER,
        equilateral INTEGER, equal_sides INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    sys.stderr.write('Create integers quintuples...\n')
    # Tables of 1, 2, 3... INTQUINTUPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1, n + 1, p + 1,  # nb1, nb2, nb3, nb4, nb5
                distcode(i + 1, j + 1, k + 1, n + 1, p + 1),  # code
                p + 1 < i + j + k + n + 4,  # pentagon?
                i == j == k == n == p,  # equilateral?
                (i == j or j == k or k == i or i == n or j == n or k == n
                 or i == p or j == p or k == p or n == p),
                # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(INTQUINTUPLES_MAX)
               for j in range(INTQUINTUPLES_MAX)
               for k in range(INTQUINTUPLES_MAX)
               for n in range(INTQUINTUPLES_MAX)
               for p in range(INTQUINTUPLES_MAX)
               if p >= n >= k >= j >= i and p - i <= 16]

    sys.stderr.write('Insert integers quintuples...')
    for i in range(100):
        sys.stderr.write('\rInsert integers quintuples... {} %'.format(i))
        db.executemany("INSERT "
                       "INTO int_quintuples(nb1, nb2, nb3, nb4, nb5, code, "
                       "pentagon, equilateral, equal_sides, "
                       "drawDate) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       db_rows[i * len(db_rows) // 100:
                               (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert integers quintuples... 100 %\n')

    creation_query = '''CREATE TABLE int_sextuples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        nb4 INTEGER, nb5 INTEGER, nb6 INTEGER, code TEXT, hexagon INTEGER,
        equilateral INTEGER, equal_sides INTEGER, drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)
    sys.stderr.write('Create integers sextuples...\n')
    # Tables of 1, 2, 3... INTSEXTUPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1, n + 1, p + 1, q + 1,
                # nb1, nb2, nb3, nb4, nb5, nb6
                distcode(i + 1, j + 1, k + 1, n + 1, p + 1, q + 1),  # code
                q + 1 < i + j + k + n + p + 5,  # hexagon?
                i == j == k == n == p == q,  # equilateral?
                (i == j or j == k or k == i or i == n or j == n or k == n
                 or i == p or j == p or k == p or n == p or i == q or j == q
                 or k == q or n == q or p == q),
                # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(INTSEXTUPLES_MAX)
               for j in range(INTSEXTUPLES_MAX)
               for k in range(INTSEXTUPLES_MAX)
               for n in range(INTSEXTUPLES_MAX)
               for p in range(INTSEXTUPLES_MAX)
               for q in range(INTSEXTUPLES_MAX)
               if q >= p >= n >= k >= j >= i and q - i <= 16]

    sys.stderr.write('Insert integers sextuples...')
    for i in range(100):
        sys.stderr.write('\rInsert integers sextuples... {} %'.format(i))
        db.executemany("INSERT "
                       "INTO int_sextuples(nb1, nb2, nb3, nb4, nb5, nb6, "
                       "code, hexagon, equilateral, equal_sides, "
                       "drawDate) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       db_rows[i * len(db_rows) // 100:
                               (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert integers sextuples... 100 %\n')
    # sys.stderr.flush()

    sys.stderr.write('Create natural numbers singletons...\n')
    creation_query = '''CREATE TABLE singletons
       (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    # Tables of 1, 2, 3... NNSINGLETONS_MAX
    db_rows = [(i + 1, 0) for i in range(NNSINGLETONS_MAX)]
    for i in range(100):
        sys.stderr.write('\rInsert natural numbers singletons... {} %'
                         .format(i))
        natural_nb_tuples_db.executemany(
            "INSERT "
            "INTO singletons(nb1, drawDate) "
            "VALUES(?, ?)",
            db_rows[i * len(db_rows) // 100:
                    (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert natural numbers singletons... 100 %\n')

    sys.stderr.write('Create natural numbers pairs...\n')
    creation_query = '''CREATE TABLE pairs
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, code TEXT,
        lock_equal_products INTEGER, drawDate INTEGER, clever INTEGER,
        suits_for_deci1 INTEGER, suits_for_deci2 INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    # Tables of 1, 2, 3... NNPAIRS_MAX
    db_rows = [(i + 1, j + 1, distcode(i + 1, j + 1), 0, 0, 0,
                _suits_for_deci1(i + 1, j + 1),
                _suits_for_deci2(i + 1, j + 1))
               for i in range(NNPAIRS_MAX)
               for j in range(NNPAIRS_MAX)
               if j >= i]
    for i in range(100):
        sys.stderr.write('\rInsert natural numbers pairs... {} %'.format(i))
        natural_nb_tuples_db.executemany(
            "INSERT "
            "INTO pairs(nb1, nb2, code, lock_equal_products, "
            "drawDate, clever, suits_for_deci1, suits_for_deci2) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            db_rows[i * len(db_rows) // 100:
                    (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert natural numbers pairs... 100 %\n')
    sys.stderr.write('Setup natural numbers pairs: clever (5)...\n')
    for couple in [(2, 5), (2, 50), (2, 500), (5, 20), (5, 200)]:
        natural_nb_tuples_db.execute(
            "UPDATE pairs SET clever = 5 WHERE nb1 = '" + str(couple[0])
            + "' and nb2 = '" + str(couple[1]) + "';")
    sys.stderr.write('Setup natural numbers pairs: clever (4)...\n')
    for couple in [(4, 25), (4, 250)]:
        natural_nb_tuples_db.execute(
            "UPDATE pairs SET clever = 4 WHERE nb1 = '" + str(couple[0])
            + "' and nb2 = '" + str(couple[1]) + "';")

    sys.stderr.write('Create natural number×decimal "clever" pairs...\n')
    creation_query = '''CREATE TABLE nn_deci_clever_pairs
       (id INTEGER, nb1 FLOAT, nb2 FLOAT, drawDate INTEGER,
        clever INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    sys.stderr.write('Insert natural number×decimal "clever" pairs...\n')
    # Insert natural number/decimal "clever" pairs into the db
    # The tenths series (only one yet) is identified by a 10
    # the quarters series by a 4
    # the halfs/fifths series by a 5
    start_id = tuple(natural_nb_tuples_db.execute(
        "SELECT MAX(id) FROM pairs "))[0][0] + 1
    db_rows = list(zip([i + start_id for i in range(5)],
                       [0.2, 2, 4, 4, 0.1],
                       [5, 0.5, 0.25, 2.5, 10],
                       [0, 0, 0, 0, 0],
                       [5, 5, 4, 4, 10]))

    natural_nb_tuples_db.executemany(
        "INSERT INTO nn_deci_clever_pairs(id, nb1, nb2, drawDate, clever) "
        "VALUES(?, ?, ?, ?, ?)", db_rows)

    sys.stderr.write('Create natural numbers triples...\n')
    creation_query = '''CREATE TABLE triples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        code TEXT, constructible INTEGER, isosceles INTEGER,
        equilateral INTEGER, pythagorean INTEGER, equal_sides INTEGER,
        drawDate INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    # Tables of 1, 2, 3... NNTRIPLES_MAX
    db_rows = [(15, 2, 3, 'none', 0, 0, 0, 0, 0, 0),
               (15, 2, 5, 'none', 0, 0, 0, 0, 0, 0),
               (15, 2, 6, 'none', 0, 0, 0, 0, 0, 0),
               (15, 3, 4, 'none', 0, 0, 0, 0, 0, 0),
               (15, 3, 5, 'none', 0, 0, 0, 0, 0, 0),
               (15, 4, 5, 'none', 0, 0, 0, 0, 0, 0),
               (15, 4, 6, 'none', 0, 0, 0, 0, 0, 0),
               (15, 5, 6, 'none', 0, 0, 0, 0, 0, 0),
               (25, 2, 3, 'none', 0, 0, 0, 0, 0, 0),
               (25, 2, 5, 'none', 0, 0, 0, 0, 0, 0),
               (25, 2, 6, 'none', 0, 0, 0, 0, 0, 0),
               (25, 3, 4, 'none', 0, 0, 0, 0, 0, 0),
               (25, 3, 5, 'none', 0, 0, 0, 0, 0, 0),
               (25, 4, 5, 'none', 0, 0, 0, 0, 0, 0),
               (25, 4, 6, 'none', 0, 0, 0, 0, 0, 0),
               (25, 5, 6, 'none', 0, 0, 0, 0, 0, 0)]
    db_rows += [(i + 1, j + 1, k + 1,  # nb1, nb2, nb3
                 distcode(i + 1, j + 1, k + 1),  # code
                 k + 1 < i + j + 2,  # constructible triangle?
                 (i == j and j != k) or (i == k and i != j)
                 or (j == k and i != j),  # isosceles? (but not equilateral)
                 i == j == k,  # equilateral?
                 (k + 1) ** 2 == (i + 1) ** 2 + (j + 1) ** 2,  # pythagorean?
                 (i == j or j == k or k == i),  # at least 2 equal sides?
                 0  # drawDate
                 )
                for i in range(NNTRIPLES_MAX)
                for j in range(NNTRIPLES_MAX)
                for k in range(NNTRIPLES_MAX)
                if k >= j >= i]

    sys.stderr.write('Insert natural numbers triples...')
    for i in range(100):
        sys.stderr.write('\rInsert natural numbers triples... {} %'
                         .format(i))
        natural_nb_tuples_db\
            .executemany("INSERT "
                         "INTO triples(nb1, nb2, nb3, code, "
                         "constructible, isosceles, equilateral, pythagorean,"
                         "equal_sides, drawDate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         db_rows[i * len(db_rows) // 100:
                                 (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert natural numbers triples... 100 %\n')
    # sys.stderr.flush()

    sys.stderr.write('Create natural numbers quadruples...\n')
    creation_query = '''CREATE TABLE quadruples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        nb4 INTEGER, code TEXT, constructible INTEGER,
        equilateral INTEGER, equal_sides INTEGER, drawDate INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    # Tables of 1, 2, 3... NNQUADRUPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1, n + 1,  # nb1, nb2, nb3, nb4
                distcode(i + 1, j + 1, k + 1, n + 1),  # code
                n + 1 < i + j + k + 3,  # constructible quadrilateral?
                i == j == k == n,  # equilateral?
                (i == j or j == k or k == i or i == n or j == n or k == n),
                # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(NNQUADRUPLES_MAX)
               for j in range(NNQUADRUPLES_MAX)
               for k in range(NNQUADRUPLES_MAX)
               for n in range(NNQUADRUPLES_MAX)
               if n >= k >= j >= i]

    sys.stderr.write('Insert natural numbers quadruples...')
    for i in range(100):
        sys.stderr.write('\rInsert natural numbers quadruples... {} %'
                         .format(i))
        natural_nb_tuples_db\
            .executemany("INSERT "
                         "INTO quadruples(nb1, nb2, nb3, nb4, code, "
                         "constructible, equilateral, equal_sides, "
                         "drawDate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         db_rows[i * len(db_rows) // 100:
                                 (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert natural numbers quadruples... 100 %\n')
    # sys.stderr.flush()

    sys.stderr.write('Create natural numbers quintuples...\n')
    creation_query = '''CREATE TABLE quintuples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        nb4 INTEGER, nb5 INTEGER, code TEXT, constructible INTEGER,
        equilateral INTEGER, equal_sides INTEGER, drawDate INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    # Tables of 1, 2, 3... NNQUINTUPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1, n + 1, p + 1,  # nb1, nb2, nb3, nb4, nb5
                distcode(i + 1, j + 1, k + 1, n + 1, p + 1),  # code
                p + 1 < i + j + k + n + 4,  # constructible?
                i == j == k == n == p,  # equilateral?
                (i == j or j == k or k == i or i == n or j == n or k == n
                 or i == p or j == p or k == p or n == p),
                # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(NNQUINTUPLES_MAX)
               for j in range(NNQUINTUPLES_MAX)
               for k in range(NNQUINTUPLES_MAX)
               for n in range(NNQUINTUPLES_MAX)
               for p in range(NNQUINTUPLES_MAX)
               if p >= n >= k >= j >= i]

    sys.stderr.write('Insert natural numbers quintuples...')
    for i in range(100):
        sys.stderr.write('\rInsert natural numbers quintuples... {} %'
                         .format(i))
        natural_nb_tuples_db\
            .executemany("INSERT "
                         "INTO quintuples(nb1, nb2, nb3, nb4, nb5, code, "
                         "constructible, equilateral, equal_sides, "
                         "drawDate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         db_rows[i * len(db_rows) // 100:
                                 (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert natural numbers quintuples... 100 %\n')
    # sys.stderr.flush()

    sys.stderr.write('Create natural numbers sextuples...\n')
    creation_query = '''CREATE TABLE sextuples
       (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER, nb3 INTEGER,
        nb4 INTEGER, nb5 INTEGER, nb6 INTEGER, code TEXT,
        constructible INTEGER, equilateral INTEGER, equal_sides INTEGER,
        drawDate INTEGER)'''
    natural_nb_tuples_db_creation_queries.append(creation_query)
    natural_nb_tuples_db.execute(creation_query)
    # Tables of 1, 2, 3... NNSEXTUPLES_MAX
    db_rows = [(i + 1, j + 1, k + 1, n + 1, p + 1, q + 1,
                # nb1, nb2, nb3, nb4, nb5, nb6
                distcode(i + 1, j + 1, k + 1, n + 1, p + 1, q + 1),  # code
                q + 1 < i + j + k + n + p + 5,  # constructible hexagon?
                i == j == k == n == p == q,  # equilateral?
                (i == j or j == k or k == i or i == n or j == n or k == n
                 or i == p or j == p or k == p or n == p or i == q or j == q
                 or k == q or n == q or p == q),
                # at least 2 equal sides?
                0  # drawDate
                )
               for i in range(NNSEXTUPLES_MAX)
               for j in range(NNSEXTUPLES_MAX)
               for k in range(NNSEXTUPLES_MAX)
               for n in range(NNSEXTUPLES_MAX)
               for p in range(NNSEXTUPLES_MAX)
               for q in range(NNSEXTUPLES_MAX)
               if q >= p >= n >= k >= j >= i]

    sys.stderr.write('Insert natural numbers sextuples...')
    for i in range(100):
        sys.stderr.write('\rInsert natural numbers sextuples... {} %'
                         .format(i))
        natural_nb_tuples_db\
            .executemany("INSERT "
                         "INTO sextuples(nb1, nb2, nb3, nb4, nb5, nb6, code, "
                         "constructible, equilateral, equal_sides, "
                         "drawDate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         db_rows[i * len(db_rows) // 100:
                                 (i + 1) * len(db_rows) // 100])
    sys.stderr.write('\rInsert natural numbers sextuples... 100 %\n')
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

    sys.stderr.write('Insert proper fractions...\n')
    db_rows = [(i + 1, j + 1, 0 if gcd(i + 1, j + 1) == 1 else 1, 0)
               for i in range(10)
               for j in range(10)
               if j > i]
    db.executemany("INSERT "
                   "INTO simple_proper_fractions(nb1, nb2, reducible, "
                   "drawDate) "
                   "VALUES(?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert simple improper fractions...\n')
    db_rows = [(i + 1, j + 2, 0 if gcd(i + 1, j + 2) == 1 else 1, 0)
               for i in range(10)
               for j in range(9)
               if j < i]
    db.executemany("INSERT "
                   "INTO simple_improper_fractions(nb1, nb2, reducible, "
                   "drawDate) "
                   "VALUES(?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert improper fractions...\n')
    db_rows = [(i + 1, j + 2, 0 if gcd(i + 1, j + 2) == 1 else 1,
                (i + 1) % (j + 2),
                float(Number((i + 1) / (j + 2)).rounded(Number('1.00'))), 0)
               for j in range(100)
               for i in range(100)
               if j < i]
    db.executemany("INSERT "
                   "INTO improper_fractions(nb1, nb2, reducible, mod, "
                   "deci, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?)",
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

    sys.stderr.write('Insert (x;y) coordinates...\n')
    db_rows = [(x, y, 0)
               for x in range(-COORD_MAX, COORD_MAX + 1)
               for y in range(-COORD_MAX, COORD_MAX + 1)]
    db.executemany("INSERT "
                   "INTO coordinates_xy (nb1, nb2, drawDate) "
                   "VALUES(?, ?, ?)",
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

    sys.stderr.write('Insert letters for spreadsheet columns...\n')
    db_rows = [(letter, 0) for letter in 'ABCDEFGHIJKLM']
    db.executemany("INSERT "
                   "INTO cols_for_spreadsheets"
                   "(col, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert variants of signed numbers comparisons...\n')
    db_rows = [(i, 0) for i in range(12)]
    db.executemany("INSERT "
                   "INTO signed_nb_comparisons"
                   "(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert variants of expressions...\n')
    db_rows = [(i + 95, 0) for i in range(41)]  # hence from 95 to 135 included
    # + [(i + 200, 0) for i in range(8)]   later, add 20* ids
    db.executemany("INSERT "
                   "INTO expressions"
                   "(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert time units couples...\n')
    creation_query = '''CREATE TABLE time_units_couples
                        (id INTEGER PRIMARY KEY, u1 TEXT, u2 TEXT,
                         drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)

    db_rows = [('h', 'min', 0), ('min', 's', 0)]
    db.executemany("INSERT "
                   "INTO time_units_couples(u1, u2, drawDate) "
                   "VALUES(?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert time units conversions...\n')
    creation_query = '''CREATE TABLE time_units_conversions
                        (id INTEGER PRIMARY KEY, category INTEGER,
                         level INTEGER, direction TEXT,
                         drawDate INTEGER)'''
    db_creation_queries.append(creation_query)
    db.execute(creation_query)

    db_rows = [(1, 1, 'right', 0), (1, 1, 'left', 0),
               (2, 2, 'right', 0), (2, 3, 'left', 0),
               (3, 2, 'right', 0), (3, 3, 'left', 0)]
    db.executemany("INSERT "
                   "INTO time_units_conversions(category, level, direction, "
                   "drawDate) VALUES(?, ?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert unit conversions...\n')
    db_rows = [('km', 'hm', 'right', 'length', 1, 'no', 1, 0),   # simple units
               ('hm', 'dam', 'right', 'length', 1, 'no', 1, 0),  # one column;
               ('dam', 'm', 'right', 'length', 1, 'no', 1, 0),   # "classic"
               ('m', 'dm', 'right', 'length', 1, 'no', 1, 0),    # conversions
               ('dm', 'cm', 'right', 'length', 1, 'no', 1, 0),
               ('cm', 'mm', 'right', 'length', 1, 'no', 1, 0),
               ('km', 'm', 'right', 'length', 1, 'yes', 1, 0),
               ('m', 'cm', 'right', 'length', 1, 'yes', 1, 0),
               ('m', 'mm', 'right', 'length', 1, 'no', 1, 0),
               ('hL', 'daL', 'right', 'capacity', 1, 'no', 1, 0),
               ('daL', 'L', 'right', 'capacity', 1, 'no', 1, 0),
               ('L', 'dL', 'right', 'capacity', 1, 'no', 1, 0),
               ('dL', 'cL', 'right', 'capacity', 1, 'no', 1, 0),
               ('cL', 'mL', 'right', 'capacity', 1, 'no', 1, 0),
               ('hL', 'L', 'right', 'capacity', 1, 'no', 1, 0),
               ('kg', 'hg', 'right', 'mass', 1, 'no', 1, 0),
               ('hg', 'dag', 'right', 'mass', 1, 'no', 1, 0),
               ('dag', 'g', 'right', 'mass', 1, 'no', 1, 0),
               ('g', 'dg', 'right', 'mass', 1, 'no', 1, 0),
               ('dg', 'cg', 'right', 'mass', 1, 'no', 1, 0),
               ('cg', 'mg', 'right', 'mass', 1, 'no', 1, 0),
               ('kg', 'g', 'right', 'mass', 1, 'no', 1, 0),
               ('hm', 'km', 'left', 'length', 1, 'no', 1, 0),
               ('dam', 'hm', 'left', 'length', 1, 'no', 1, 0),
               ('m', 'dam', 'left', 'length', 1, 'no', 1, 0),
               ('dm', 'm', 'left', 'length', 1, 'no', 1, 0),
               ('cm', 'dm', 'left', 'length', 1, 'no', 1, 0),
               ('mm', 'cm', 'left', 'length', 1, 'no', 1, 0),
               ('m', 'km', 'left', 'length', 1, 'yes', 1, 0),
               ('cm', 'm', 'left', 'length', 1, 'yes', 1, 0),
               ('daL', 'hL', 'left', 'capacity', 1, 'no', 1, 0),
               ('L', 'daL', 'left', 'capacity', 1, 'no', 1, 0),
               ('dL', 'L', 'left', 'capacity', 1, 'no', 1, 0),
               ('cL', 'dL', 'left', 'capacity', 1, 'no', 1, 0),
               ('mL', 'cL', 'left', 'capacity', 1, 'no', 1, 0),
               ('L', 'hL', 'left', 'capacity', 1, 'no', 1, 0),
               ('hg', 'kg', 'left', 'mass', 1, 'no', 1, 0),
               ('dag', 'hg', 'left', 'mass', 1, 'no', 1, 0),
               ('g', 'dag', 'left', 'mass', 1, 'no', 1, 0),
               ('dg', 'g', 'left', 'mass', 1, 'no', 1, 0),
               ('cg', 'dg', 'left', 'mass', 1, 'no', 1, 0),
               ('mg', 'cg', 'left', 'mass', 1, 'no', 1, 0),
               ('g', 'kg', 'left', 'mass', 1, 'no', 1, 0),
               ('km', 'dam', 'right', 'length', 2, 'no', 1, 0),  # two columns
               ('hm', 'm', 'right', 'length', 2, 'no', 1, 0),
               ('dam', 'dm', 'right', 'length', 2, 'no', 1, 0),
               ('dm', 'mm', 'right', 'length', 2, 'no', 1, 0),
               ('daL', 'dL', 'right', 'capacity', 2, 'no', 1, 0),
               ('L', 'cL', 'right', 'capacity', 2, 'no', 1, 0),
               ('dL', 'mL', 'right', 'capacity', 2, 'no', 1, 0),
               ('kg', 'dag', 'right', 'mass', 2, 'no', 1, 0),
               ('hg', 'g', 'right', 'mass', 2, 'no', 1, 0),
               ('dag', 'dg', 'right', 'mass', 2, 'no', 1, 0),
               ('g', 'cg', 'right', 'mass', 2, 'no', 1, 0),
               ('dg', 'mg', 'right', 'mass', 2, 'no', 1, 0),
               ('dam', 'km', 'left', 'length', 2, 'no', 1, 0),
               ('m', 'hm', 'left', 'length', 2, 'no', 1, 0),
               ('dm', 'dam', 'left', 'length', 2, 'no', 1, 0),
               ('mm', 'dm', 'left', 'length', 2, 'no', 1, 0),
               ('dL', 'daL', 'left', 'capacity', 2, 'no', 1, 0),
               ('cL', 'L', 'left', 'capacity', 2, 'no', 1, 0),
               ('mL', 'dL', 'left', 'capacity', 2, 'no', 1, 0),
               ('dag', 'kg', 'left', 'mass', 2, 'no', 1, 0),
               ('g', 'hg', 'left', 'mass', 2, 'no', 1, 0),
               ('dg', 'dag', 'left', 'mass', 2, 'no', 1, 0),
               ('cg', 'g', 'left', 'mass', 2, 'no', 1, 0),
               ('mg', 'dg', 'left', 'mass', 2, 'no', 1, 0),
               ('hm', 'dm', 'right', 'length', 3, 'no', 1, 0),  # three columns
               ('dam', 'cm', 'right', 'length', 3, 'no', 1, 0),
               ('dm', 'hm', 'left', 'length', 3, 'no', 1, 0),
               ('cm', 'dam', 'left', 'length', 3, 'no', 1, 0),
               ('hL', 'dL', 'right', 'capacity', 3, 'no', 1, 0),
               ('daL', 'cL', 'right', 'capacity', 3, 'no', 1, 0),
               ('dL', 'hL', 'left', 'capacity', 3, 'no', 1, 0),
               ('cL', 'daL', 'left', 'capacity', 3, 'no', 1, 0),
               ('hg', 'dg', 'right', 'mass', 3, 'no', 1, 0),
               ('dag', 'cg', 'right', 'mass', 3, 'no', 1, 0),
               ('dg', 'hg', 'left', 'mass', 3, 'no', 1, 0),
               ('cg', 'dag', 'left', 'mass', 3, 'no', 1, 0),
               ('km', 'hm', 'right', 'area', 2, 'no', 2, 0),  # area: 1 col[2]
               ('hm', 'dam', 'right', 'area', 2, 'no', 2, 0),
               ('dam', 'm', 'right', 'area', 2, 'no', 2, 0),
               ('m', 'dm', 'right', 'area', 2, 'no', 2, 0),
               ('dm', 'cm', 'right', 'area', 2, 'no', 2, 0),
               ('cm', 'mm', 'right', 'area', 2, 'no', 2, 0),
               ('hm', 'km', 'left', 'area', 2, 'no', 2, 0),
               ('dam', 'hm', 'left', 'area', 2, 'no', 2, 0),
               ('m', 'dam', 'left', 'area', 2, 'no', 2, 0),
               ('dm', 'm', 'left', 'area', 2, 'no', 2, 0),
               ('cm', 'dm', 'left', 'area', 2, 'no', 2, 0),
               ('mm', 'cm', 'left', 'area', 2, 'no', 2, 0),
               ('km', 'dam', 'right', 'area', 4, 'no', 2, 0),  # area: 2 col[4]
               ('hm', 'm', 'right', 'area', 4, 'no', 2, 0),
               ('dam', 'dm', 'right', 'area', 4, 'no', 2, 0),
               ('m', 'cm', 'right', 'area', 4, 'no', 2, 0),
               ('dm', 'mm', 'right', 'area', 4, 'no', 2, 0),
               ('dam', 'km', 'left', 'area', 4, 'no', 2, 0),
               ('m', 'hm', 'left', 'area', 4, 'no', 2, 0),
               ('dm', 'dam', 'left', 'area', 4, 'no', 2, 0),
               ('cm', 'm', 'left', 'area', 4, 'no', 2, 0),
               ('mm', 'dm', 'left', 'area', 4, 'no', 2, 0),
               ('km', 'hm', 'right', 'volume', 3, 'no', 3, 0),  # vol: 1 col[3]
               ('hm', 'dam', 'right', 'volume', 3, 'no', 3, 0),
               ('dam', 'm', 'right', 'volume', 3, 'no', 3, 0),
               ('m', 'dm', 'right', 'volume', 3, 'no', 3, 0),
               ('dm', 'cm', 'right', 'volume', 3, 'no', 3, 0),
               ('cm', 'mm', 'right', 'volume', 3, 'no', 3, 0),
               ('hm', 'km', 'left', 'volume', 3, 'no', 3, 0),
               ('dam', 'hm', 'left', 'volume', 3, 'no', 3, 0),
               ('m', 'dam', 'left', 'volume', 3, 'no', 3, 0),
               ('dm', 'm', 'left', 'volume', 3, 'no', 3, 0),
               ('cm', 'dm', 'left', 'volume', 3, 'no', 3, 0),
               ('mm', 'cm', 'left', 'volume', 3, 'no', 3, 0),
               ('km', 'dam', 'right', 'volume', 6, 'no', 3, 0),  # vol: 2col[6]
               ('hm', 'm', 'right', 'volume', 6, 'no', 3, 0),
               ('dam', 'dm', 'right', 'volume', 6, 'no', 3, 0),
               ('m', 'cm', 'right', 'volume', 6, 'no', 3, 0),
               ('dm', 'mm', 'right', 'volume', 6, 'no', 3, 0),
               ('dam', 'km', 'left', 'volume', 6, 'no', 3, 0),
               ('m', 'hm', 'left', 'volume', 6, 'no', 3, 0),
               ('dm', 'dam', 'left', 'volume', 6, 'no', 3, 0),
               ('cm', 'm', 'left', 'volume', 6, 'no', 3, 0),
               ('mm', 'dm', 'left', 'volume', 6, 'no', 3, 0),
               # vol -> capacity
               ('dm', 'L', 'none', 'volume2capacity', 3, 'no', 3, 0),
               ('cm', 'mL', 'none', 'volume2capacity', 3, 'no', 3, 0),
               ('m', 'L', 'right', 'volume2capacity', 4, 'no', 3, 0),
               ('dm', 'mL', 'right', 'volume2capacity', 4, 'no', 3, 0),
               ('m', 'hL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('m', 'daL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('m', 'dL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('m', 'cL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('m', 'mL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('dm', 'hL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               ('dm', 'daL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               ('dm', 'dL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('dm', 'cL', 'right', 'volume2capacity', 7, 'no', 3, 0),
               ('cm', 'hL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               ('cm', 'daL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               ('cm', 'L', 'left', 'volume2capacity', 4, 'no', 3, 0),
               ('cm', 'dL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               ('cm', 'cL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               ('mm', 'hL', 'left', 'volume2capacity', 8, 'no', 3, 0),
               ('mm', 'daL', 'left', 'volume2capacity', 8, 'no', 3, 0),
               ('mm', 'L', 'left', 'volume2capacity', 8, 'no', 3, 0),
               ('mm', 'dL', 'left', 'volume2capacity', 8, 'no', 3, 0),
               ('mm', 'cL', 'left', 'volume2capacity', 8, 'no', 3, 0),
               ('mm', 'mL', 'left', 'volume2capacity', 7, 'no', 3, 0),
               # capacity -> vol
               ('L', 'dm', 'none', 'capacity2volume', 3, 'no', 3, 0),
               ('mL', 'cm', 'none', 'capacity2volume', 3, 'no', 3, 0),
               ('L', 'm', 'left', 'capacity2volume', 4, 'no', 3, 0),
               ('mL', 'dm', 'left', 'capacity2volume', 4, 'no', 3, 0),
               ('hL', 'm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('daL', 'm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('dL', 'm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('cL', 'm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('mL', 'm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('hL', 'dm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ('daL', 'dm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ('dL', 'dm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('cL', 'dm', 'left', 'capacity2volume', 7, 'no', 3, 0),
               ('hL', 'cm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ('daL', 'cm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ('L', 'cm', 'right', 'capacity2volume', 4, 'no', 3, 0),
               ('dL', 'cm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ('cL', 'cm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ('hL', 'mm', 'right', 'capacity2volume', 8, 'no', 3, 0),
               ('daL', 'mm', 'right', 'capacity2volume', 8, 'no', 3, 0),
               ('L', 'mm', 'right', 'capacity2volume', 8, 'no', 3, 0),
               ('dL', 'mm', 'right', 'capacity2volume', 8, 'no', 3, 0),
               ('cL', 'mm', 'right', 'capacity2volume', 8, 'no', 3, 0),
               ('mL', 'mm', 'right', 'capacity2volume', 7, 'no', 3, 0),
               ]
    db.executemany("INSERT "
                   "INTO units_conversions"
                   "(unit1, unit2, direction, category, level, easiest, "
                   "dimension, drawDate) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
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

    anglessets_db_creation_queries = []
    sys.stderr.write('Anglessets db: insert anglessets...\n')
    creation_query = '''CREATE TABLE anglessets
                        (id INTEGER PRIMARY KEY,
                         nbof_angles INTEGER, distcode TEXT, variant INTEGER,
                         nbof_right_angles INTEGER, equal_angles TEXT,
                         table2 INTEGER, table3 INTEGER,
                         table4 INTEGER, table5 INTEGER, table6 INTEGER,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(2, '1_1', 0, 0, 'all_different', 0, 0, 0, 0, 0, 0),
               (2, '1_1r', 0, 1, 'all_different', 0, 0, 0, 0, 0, 0),
               (2, '1_1r', 1, 1, 'all_different', 0, 0, 0, 0, 0, 0),
               (2, '2', 0, 0, 'equilateral', 1, 0, 0, 0, 0, 0),
               (3, '1_1_1', 0, 0, 'all_different', 0, 0, 0, 0, 0, 0),
               (3, '1_1_1r', 0, 1, 'all_different', 0, 0, 0, 0, 0, 0),
               (3, '1_1_1r', 1, 1, 'all_different', 0, 0, 0, 0, 0, 0),
               (3, '1_1_1r', 2, 1, 'all_different', 0, 0, 0, 0, 0, 0),
               (3, '2_1', 0, 0, 'none', 1, 0, 0, 0, 0, 0),
               (3, '2_1', 1, 0, 'none', 1, 0, 0, 0, 0, 0),
               (3, '2_1', 2, 0, 'none', 1, 0, 0, 0, 0, 0),
               (3, '2_1r', 0, 1, 'none', 1, 0, 0, 0, 0, 0),
               (3, '2_1r', 1, 1, 'none', 1, 0, 0, 0, 0, 0),
               (3, '2_1r', 2, 1, 'none', 1, 0, 0, 0, 0, 0),
               (3, '3', 0, 0, 'equilateral', 0, 1, 0, 0, 0, 0)]
    anglessets_db.executemany(
        "INSERT INTO anglessets("
        "nbof_angles, distcode, variant, nbof_right_angles, equal_angles, "
        "table2, table3, table4, table5, table6, drawDate) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        db_rows)

    sys.stderr.write('Anglessets db: insert anglessets subvariants...\n')

    creation_query = '''CREATE TABLE _1_1_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0)]
    anglessets_db.executemany(
        "INSERT INTO _1_1_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _1_1r_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0)]
    anglessets_db.executemany(
        "INSERT INTO _1_1r_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _2_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0)]
    anglessets_db.executemany(
        "INSERT INTO _2_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _1_1_1_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0)]
    anglessets_db.executemany(
        "INSERT INTO _1_1_1_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _1_1_1r_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0)]
    anglessets_db.executemany(
        "INSERT INTO _1_1_1r_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _2_1_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0)]
    anglessets_db.executemany(
        "INSERT INTO _2_1_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _2_1r_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0)]
    anglessets_db.executemany(
        "INSERT INTO _2_1r_subvariants(subvariant_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    creation_query = '''CREATE TABLE _3_subvariants
                        (id INTEGER PRIMARY KEY, subvariant_nb,
                         drawDate INTEGER)'''
    anglessets_db_creation_queries.append(creation_query)
    anglessets_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0)]
    anglessets_db.executemany(
        "INSERT INTO _3_subvariants(subvariant_nb, drawDate) "
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
               (4, 'quadrilateral', 'kite', 'quadrilateral_2_2', 'none',
                3, 0, 1, 0, 0, 0, 0, 0),
               (4, 'quadrilateral', 'parallelelogram', 'quadrilateral_2_2',
                'none', 3, 1, 1, 0, 0, 0, 0, 0),
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
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 6, 1, 0, 0, 0, 0, 0),
               (6, 'hexagon', '', 'hexagon_2_2_1_1', 'none',
                5, 7, 1, 0, 0, 0, 0, 0),
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
    creation_query = '''CREATE TABLE triangle_2_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
    shapes_db.executemany(
        "INSERT INTO triangle_2_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles, isosceles triangles, equilateral '
                     'triangles...')
    creation_query = '''CREATE TABLE triangle_3_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO triangle_3_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles, isosceles triangles, equilateral '
                     'triangles, quadrilaterals...')
    creation_query = '''CREATE TABLE quadrilateral_1_1_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    shapes_db.executemany(
        "INSERT INTO quadrilateral_1_1_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE quadrilateral_2_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO quadrilateral_2_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE quadrilateral_2_2_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO quadrilateral_2_2_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE quadrilateral_3_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), (3, 0), (4, 0)]
    shapes_db.executemany(
        "INSERT INTO quadrilateral_3_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE quadrilateral_4_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0)]
    shapes_db.executemany(
        "INSERT INTO quadrilateral_4_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    sys.stderr.write('\rShapes db: insert shapes variants: scalene triangles, '
                     'right triangles, isosceles triangles, equilateral '
                     'triangles, quadrilaterals, pentagons...\n')
    creation_query = '''CREATE TABLE pentagon_1_1_1_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_1_1_1_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE pentagon_2_1_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_2_1_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE pentagon_2_2_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_2_2_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE pentagon_3_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_3_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE pentagon_3_2_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_3_2_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE pentagon_4_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_4_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE pentagon_5_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO pentagon_5_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_1_1_1_1_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO hexagon_1_1_1_1_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_2_1_1_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0)]
    shapes_db.executemany(
        "INSERT INTO hexagon_2_1_1_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_2_2_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_2_2_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_2_2_2_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_2_2_2_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_3_1_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_3_1_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_3_2_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_3_2_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_3_3_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_3_3_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_4_1_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_4_1_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_4_2_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_4_2_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_5_1_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_5_1_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)
    creation_query = '''CREATE TABLE hexagon_6_shapes
                        (id INTEGER PRIMARY KEY, shape_nb, drawDate INTEGER)'''
    shapes_db_creation_queries.append(creation_query)
    shapes_db.execute(creation_query)
    db_rows = [(1, 0), (2, 0), ]
    shapes_db.executemany(
        "INSERT INTO hexagon_6_shapes(shape_nb, drawDate) "
        "VALUES(?, ?)",
        db_rows)

    solids_db_creation_queries = []
    sys.stderr.write('Solids db: insert solids...\n')
    # type will be: cuboid, cube, prism etc.
    creation_query = '''CREATE TABLE polyhedra
                        (id INTEGER PRIMARY KEY,
                         faces_nb INTEGER, type TEXT, variant INTEGER,
                         drawDate INTEGER)'''
    solids_db_creation_queries.append(creation_query)
    solids_db.execute(creation_query)
    db_rows = [(6, 'rightcuboid', 0, 0),
               (6, 'rightcuboid', 1, 0),
               (6, 'rightcuboid', 2, 0),
               (6, 'rightcuboid', 3, 0),
               (6, 'rightcuboid', 4, 0),
               (6, 'rightcuboid', 5, 0),
               ]
    solids_db.executemany(
        "INSERT INTO polyhedra("
        "faces_nb, type, variant, drawDate) "
        "VALUES(?, ?, ?, ?)",
        db_rows)

    sys.stderr.write('Commit changes to databases...\n')
    db.commit()
    shapes_db.commit()
    solids_db.commit()
    anglessets_db.commit()
    natural_nb_tuples_db.commit()
    sys.stderr.write('Close databases...\n')
    db.close()
    shapes_db.close()
    solids_db.close()
    anglessets_db.close()
    natural_nb_tuples_db.close()
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
    solids_db_index = {}
    for qr in solids_db_creation_queries:
        key, value = parse_sql_creation_query(qr)
        solids_db_index.update({key: value})
    with open(settings.solids_db_index_path, 'w') as f:
        json.dump(solids_db_index, f, indent=4)
        f.write('\n')
    anglessets_db_index = {}
    for qr in anglessets_db_creation_queries:
        key, value = parse_sql_creation_query(qr)
        anglessets_db_index.update({key: value})
    with open(settings.anglessets_db_index_path, 'w') as f:
        json.dump(anglessets_db_index, f, indent=4)
        f.write('\n')
    natural_nb_tuples_db_index = {}
    for qr in natural_nb_tuples_db_creation_queries:
        key, value = parse_sql_creation_query(qr)
        natural_nb_tuples_db_index.update({key: value})
    with open(settings.natural_nb_tuples_db_index_path, 'w') as f:
        json.dump(natural_nb_tuples_db_index, f, indent=4)
        f.write('\n')
    sys.stderr.write('Done!\n')


if __name__ == '__main__':
    __main__()
