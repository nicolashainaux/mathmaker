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

import os
import pytest
import sqlite3

from mathmaker import settings
from mathmaker.lib.tools import db as database


def test_empty_query_result():
    """Check if an empty result raises an error."""
    with pytest.raises(RuntimeError):
        next(database.source('w3l', ['id', 'word'],
                             language='non-existing-code'))


def test_wnl():
    """Check a request in all languages for wNl databases is never empty."""
    for lang in next(os.walk(settings.localedir))[1]:
        settings.language = lang
        for i in [2, 3, 4, 5, 6, 7]:
            try:
                assert len(next(database.source('w' + str(i) + 'l',
                                                ['id', 'word'],
                                language=lang)))
            except sqlite3.OperationalError as e:
                # We ignore the non-existing tables among the ones that are
                # tested here, because we know there are. Any other exception
                # must be raised again.
                if (len(e.args) == 1
                    and e.args[0].startswith('no such table: ')):
                    pass
                else:
                    raise
