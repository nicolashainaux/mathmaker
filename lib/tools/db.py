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
from lib.common import settings, shared

log = settings.mainlogger

class source(object):

    def __init__(self, table_name, col, **kwargs):
        self.table_name = table_name
        self.col = col
        self.language = kwargs['language'] if 'language' in kwargs else ""

    def reset(self):
        shared.db.execute(\
        "UPDATE " + self.table_name + " SET drawDate = 0;")

    def __next__(self):
        return self.next()

    def next(self, **kwargs):
        l = "AND language = '" + self.language + "' " if self.language != ""\
                                                     else ""
        kw_conditions = ""
        for kw in kwargs:
            if kw.endswith("_to_check"):
                k = kw[:-9]
                kw_conditions += " AND " + k + "_min" + " <= " + str(kwargs[kw]) + " "
                kw_conditions += " AND " + k + "_max" + " >= " + str(kwargs[kw]) + " "
            elif kw == "source_id":
                pass
            else:
                kw_conditions += " AND " + kw + " = '" + kwargs[kw] + "' "

        select_part = "SELECT id," + self.col + " FROM " + self.table_name
        if 'source_id' in kwargs and kwargs['source_id'] == "mini_pb_wording":
            select_part = "SELECT id," + self.col + ",wording_context FROM " \
                          + self.table_name

        cmd = select_part + " WHERE drawDate = 0 " + l + kw_conditions + \
              "ORDER BY random() LIMIT 1;"
        query_result = tuple(shared.db.execute(cmd))
        if not len(query_result):
            self.reset()
            query_result = tuple(shared.db.execute(cmd))

        if len(query_result[0]) == 2:
            ID, word = query_result[0]
            shared.db.execute(\
            "UPDATE " + self.table_name + \
            " SET drawDate = datetime() WHERE id = " + str(ID) + ";")
        elif len(query_result[0]) == 3:
            ID, word, wording_context = query_result[0]
            shared.db.execute(\
            "UPDATE " + self.table_name + \
            " SET drawDate = datetime() WHERE wording_context = '" \
            + str(wording_context) + "';")
        return word

