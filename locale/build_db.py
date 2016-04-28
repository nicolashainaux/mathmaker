#!/usr/bin/env python3
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

import sys, os, inspect
import sqlite3
import argparse

current_dir = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(os.path.sep)])
from lib.common import settings
from lib.tools import po_file
sys.path.pop(0)
os.chdir('..')
settings.init()
from lib.common.settings import CONFIG

# Existent db is deleted. A brand new empty db is created.
if os.path.isfile(settings.path.db_dist):
    os.remove(settings.path.db_dist)
open(settings.path.db_dist, 'a').close()
db = sqlite3.connect(settings.path.db_dist)

# Creation of the tables
db.execute('''CREATE TABLE w4l
          (id INTEGER PRIMARY KEY,
          language TEXT, word TEXT, drawDate INTEGER)''')
db.execute('''CREATE TABLE names
          (language TEXT, gender TEXT, name TEXT, drawDate INTEGER)''')

# Extract data from po(t) files and insert them into the db
for l in next(os.walk(settings.localedir))[1]:
    settings.language = l
    if os.path.isfile(settings.localedir + l + "/LC_MESSAGES/w4l.po"):
        words = po_file.get_list_of('words', l, 4)
        db_rows = list(zip([l for _ in range(len(words))],
                            words,
                            [0 for _ in range(len(words))]))
        db.executemany(\
                    "INSERT INTO w4l(language, word, drawDate) VALUES(?, ?, ?)",
                    db_rows)

    for gender in ["masculine", "feminine"]:
        if os.path.isfile(settings.localedir + l \
                          + "/LC_MESSAGES/" + gender + "_names.po"):
        #___
            names = po_file.get_list_of('names', l, gender)
            db_rows = list(zip([l for _ in range(len(names))],
                                [gender for _ in range(len(names))],
                                names,
                                [0 for _ in range(len(names))]))
            db.executemany("INSERT "\
                           "INTO names(language, gender, name, drawDate) "\
                           "VALUES(?, ?, ?, ?)",
                           db_rows)


db.commit()
db.close()

