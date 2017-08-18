#!/usr/bin/env python3
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
- all single ints from 2 to 500
- all single decimal numbers with one digit from 0.0 to 100.0
- all integers pairs from 2 to 500
- a list of "clever" couples of (integer, decimal) (for multiplications)
- a list of angles' ranges (around 0, 90, 180, 270)
- the list of variants identification numbers (from 0 to 23 and 100 to 155,
  so far) for calculation_order_of_operations questions
"""

import os
import sys
import sqlite3

from mathmaker import settings
from mathmaker.lib.tools import po_file_get_list_of, check_unique_letters_words
from mathmaker.lib.tools.frameworks import get_attributes


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
    sys.stderr.write('Create new database...\n')
    open(settings.path.db_dist, 'a').close()
    sys.stderr.write('Connect to database...\n')
    db = sqlite3.connect(settings.path.db_dist)

    sys.stderr.write('Create tables...\n')
    # Creation of the tables
    db.execute('''CREATE TABLE w3l
              (id INTEGER PRIMARY KEY,
              language TEXT, word TEXT, drawDate INTEGER)''')
    db.execute('''CREATE TABLE w4l
              (id INTEGER PRIMARY KEY,
              language TEXT, word TEXT, drawDate INTEGER)''')
    db.execute('''CREATE TABLE w5l
              (id INTEGER PRIMARY KEY,
              language TEXT, word TEXT, drawDate INTEGER)''')
    db.execute('''CREATE TABLE names
              (id INTEGER PRIMARY KEY,
              language TEXT, gender TEXT, name TEXT, drawDate INTEGER)''')
    db.execute('''CREATE TABLE mini_pb_wordings
              (id INTEGER PRIMARY KEY,
              wording_context TEXT, wording TEXT,
              nb1_min INTEGER, nb1_max INTEGER,
              nb2_min INTEGER, nb2_max INTEGER,
              q_id TEXT, drawDate INTEGER)''')
    db.execute('''CREATE TABLE single_ints
              (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''')
    db.execute('''CREATE TABLE single_deci1
              (id INTEGER PRIMARY KEY, nb1 DECIMAL(4, 1), drawDate INTEGER)''')
    db.execute('''CREATE TABLE angle_ranges
              (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
              drawDate INTEGER)''')
    db.execute('''CREATE TABLE int_pairs
              (id INTEGER PRIMARY KEY,
              nb1 INTEGER, nb2 INTEGER,
              lock_equal_products INTEGER, drawDate INTEGER,
              clever INTEGER, suits_for_deci1 INTEGER,
              suits_for_deci2 INTEGER)''')
    # As int_deci_clever_pairs may be 'unioned' with int_pairs, its ids will be
    # determined starting from the max id of int_pairs, in order to have unique
    # ids over the two tables.
    db.execute('''CREATE TABLE int_deci_clever_pairs
              (id INTEGER,
              nb1 FLOAT, nb2 FLOAT,
              drawDate INTEGER,
              clever INTEGER)''')
    db.execute('''CREATE TABLE calculation_order_of_operations_variants
              (id INTEGER PRIMARY KEY, nb1 INTEGER, drawDate INTEGER)''')

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
                           [w['q_id'] for w in wordings],
                           [0 for _ in range(len(wordings))]))
        db.executemany("INSERT "
                       "INTO mini_pb_wordings(wording_context, wording, "
                       "nb1_min, nb1_max, nb2_min, nb2_max, "
                       "q_id, drawDate) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                       db_rows)

    sys.stderr.write('Insert integers pairs...\n')
    # Insert integers pairs into the db
    # Tables of 1, 2, 3... 500
    db_rows = [(i + 1, j + 1, 0, 0, 0, 1, 1)
               for i in range(500)
               for j in range(500)
               if j >= i]
    db.executemany("INSERT "
                   "INTO int_pairs(nb1, nb2, lock_equal_products, drawDate, "
                   "clever, suits_for_deci1, suits_for_deci2) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?)",
                   db_rows)

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

    sys.stderr.write(
        'Setup integers pairs: suitable for one-digit decimals...\n')
    for couple in [(i + 1, j + 1)
                   for i in range(500) for j in range(500)
                   if ((i + 1) % 10 == 0 and (j + 1) % 10 == 0)]:
        db.execute("UPDATE int_pairs SET suits_for_deci1 = 0"
                   + " WHERE nb1 = '" + str(couple[0])
                   + "' and nb2 = '" + str(couple[1]) + "';")

    sys.stderr.write(
        'Setup integers pairs: suitable for two-digits decimals...\n')
    for couple in [(i + 1, j + 1)
                   for i in range(500) for j in range(500)
                   if ((i + 1) % 10 == 0 or (j + 1) % 10 == 0)]:
        db.execute("UPDATE int_pairs SET suits_for_deci2 = 0"
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
    db_rows = [(i + 1, 0) for i in range(500)]
    db.executemany("INSERT "
                   "INTO single_ints(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert single decimals...\n')
    # Single decimal numbers
    db_rows = [(i / 10, 0) for i in range(1001)]
    db.executemany("INSERT "
                   "INTO single_deci1(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Insert angle ranges...\n')
    # Angle ranges
    db_rows = [(i - 20, i + 20, 0) for i in [0, 90, 180, 270]]
    db.executemany("INSERT "
                   "INTO angle_ranges(nb1, nb2, drawDate) "
                   "VALUES(?, ?, ?)",
                   db_rows)

    sys.stderr.write('Insert variants of calculation_order_of_operations...\n')
    # Variant numbers for calculation_order_of_operations questions.
    db_rows = [(i, 0) for i in range(24)]
    db.executemany("INSERT "
                   "INTO calculation_order_of_operations_variants"
                   "(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)
    db_rows = [(i + 100, 0) for i in range(88)]
    db.executemany("INSERT "
                   "INTO calculation_order_of_operations_variants"
                   "(nb1, drawDate) "
                   "VALUES(?, ?)",
                   db_rows)

    sys.stderr.write('Commit changes to database...\n')
    db.commit()
    sys.stderr.write('Close database...\n')
    db.close()
    sys.stderr.write('Done!\n')


if __name__ == '__main__':
    __main__()
