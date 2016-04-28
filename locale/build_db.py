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
#db.execute('''CREATE TABLE names
#          (language TEXT, gender TEXT, name TEXT)''')

# Extract data from po(t) files and insert them into the db
language = settings.language = CONFIG["LOCALES"]["LANGUAGE"]
words = po_file.get_list_of('words', language, 4)
db_rows = list(zip([language for _ in range(len(words))],
                    words,
                    [0 for _ in range(len(words))]))
db.executemany('''INSERT INTO w4l(language, word, drawDate) VALUES(?,?,?)''',
               db_rows)

db.commit()
db.close()

