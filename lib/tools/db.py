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
    ##
    #   @brief  Initializer
    def __init__(self, table_name, col, **kwargs):
        self.table_name = table_name
        self.col = col
        self.language = kwargs['language'] if 'language' in kwargs else ""

    ##
    #   @brief  Resets the drawDate of all table's entries (to 0)
    def reset(self):
        shared.db.execute(\
        "UPDATE " + self.table_name + " SET drawDate = 0;")

    ##
    #   @brief  Creates the "SELECT ...,...,... FROM ...." part of the query
    def _select_part(self, **kwargs):
        return "SELECT id," + self.col + " FROM " + self.table_name

    ##
    #   @brief  Creates the language condition part of the query
    def _language_part(self, **kwargs):
        return "AND language = '" + self.language + "' " if self.language != ""\
                                                     else ""

    ##
    #   @brief  Creates the conditions of the query, from the given kwargs
    def _kw_conditions(self, **kwargs):
        return "".join(" AND " + kw + " = '" + kwargs[kw] + "' " \
                       for kw in kwargs)

    ##
    #   @brief  Concatenates the different parts of the query
    def _cmd(self, **kwargs):
        return self._select_part(**kwargs) + " WHERE drawDate = 0 " \
               + self._language_part(**kwargs) + self._kw_conditions(**kwargs) \
               + "ORDER BY random() LIMIT 1;"

    ##
    #   @brief  Executes the query. If no result, resets the table and executes
    #           the query again. Returns the query's result.
    def _query_result(self, cmd):
        qr = tuple(shared.db.execute(cmd))
        if not len(qr):
            self.reset()
            qr = tuple(shared.db.execute(cmd))
        return qr

    ##
    #   @brief  Set the drawDate to datetime() in all entries where col_name
    #           has a value of col_match.
    def update_after_query(self, col_name, col_match):
        shared.db.execute(\
        "UPDATE " + self.table_name + \
        " SET drawDate = datetime()"\
        " WHERE " + col_name + " = '" + str(col_match) + "';")

    ##
    #   @brief  Synonym of self.next(), but makes the source an Iterator.
    def __next__(self):
        return self.next()

    ##
    #   @brief  Handles the choice of the next value to return from the database
    def next(self, **kwargs):
        ID, word = self._query_result(self._cmd(**kwargs))[0]
        self.update_after_query('id', ID)
        return word


class wordings_source(source):

    ##
    #   @brief  Creates the "SELECT ...,...,... FROM ...." part of the query.
    #           Wordings require to retrieve the 'wording_context' value instead
    #           of the id.
    def _select_part(self, **kwargs):
        return "SELECT " + self.col + ",wording_context FROM " \
               + self.table_name

    ##
    #   @brief  Creates the conditions of the query, from the given kwargs
    #           Wordings require to make special checks, like nb1_min <= ...
    #           and nb1_max >= ...
    def _kw_conditions(self, **kwargs):
        result = ""
        for kw in kwargs:
            if kw.endswith("_to_check"):
                k = kw[:-9]
                result += " AND " + k + "_min" + " <= " + str(kwargs[kw]) + " "
                result += " AND " + k + "_max" + " >= " + str(kwargs[kw]) + " "
            else:
                result += " AND " + kw + " = '" + kwargs[kw] + "' "
        return result

    ##
    #   @brief  Handles the choice of the next value to return from the database
    #           In the case of wordings, the wording_context will be used to
    #           (temporarily) remove entries sharing the same context as the
    #           chosen one.
    def next(self, **kwargs):
        word, wording_context = self._query_result(self._cmd(**kwargs))[0]
        self.update_after_query('wording_context', str(wording_context))
        return word

