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

from . import settings

def init():
    global db
    global four_letters_words_source
    global names_source
    global mini_problems_wordings_source

    db = sqlite3.connect(settings.path.db)

    import lib.tools.db
    four_letters_words_source = lib.tools.db.source("w4l", "word",
                                                    language=settings.language)
    names_source = lib.tools.db.source("names", "name",
                                       language=settings.language)
    mini_problems_wordings_source = \
                lib.tools.db.wordings_source("mini_pb_wordings", "wording")
