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

from mathmaker import settings
from mathmaker.lib import shared


class source(object):
    ##
    #   @brief  Initializer
    #   @param  table_name  The name of the table in the database
    #   @param  cols        The name of the cols used to return values. The
    #                       first one will be used to _timestamp the retrieved
    #                       data and won't be returned. If only one value is
    #                       returned it is unpacked from the tuple containing
    #                       it.
    def __init__(self, table_name, cols, **kwargs):
        self.table_name = table_name
        self.allcols = cols
        self.idcol = cols[0]
        self.valcols = cols[1:]
        self.language = kwargs['language'] if 'language' in kwargs else ""

    ##
    #   @brief  Resets the drawDate of all table's entries (to 0)
    def _reset(self, **kwargs):
        shared.db.execute("UPDATE " + self.table_name + " SET drawDate = 0;")
        if "multi_reversed" in kwargs:
            shared.db.execute("UPDATE "
                              + self.table_name
                              + " SET multirev_locked = 0;")
        if "union" in kwargs:
            shared.db.execute("UPDATE "
                              + kwargs['union']['table_name']
                              + " SET drawDate = 0;")

    ##
    #   @brief  Creates the "SELECT ...,...,... FROM ...." part of the query
    def _select_part(self, **kwargs):
        table_name = kwargs.get('table_name', self.table_name)
        return "SELECT " + ",".join(self.allcols) + " FROM " + table_name

    ##
    #   @brief  Creates the language condition part of the query
    def _language_part(self, **kwargs):
        return "AND language = '" + self.language + "' " \
            if self.language != ""\
            else ""

    ##
    #   @brief  Creates the conditions of the query, from the given kwargs
    #           Some special checks are allowed, like nb1_min <= ...
    #           and nb1_max >= ...
    def _kw_conditions(self, **kwargs):
        result = ""
        for kw in kwargs:
            if kw == "raw":
                result += " AND " + kwargs[kw] + " "
            elif kw == "triangle_inequality":
                common_nb, t1, t2 = kwargs[kw]
                mini = str(abs(t1 - t2) + 1)  # we avoid "too flat" triangles
                maxi = str(t1 + t2 - 1)
                result += 'AND ('\
                    '(nb1 = ' + str(common_nb) + ' '\
                    'AND (nb2 >= ' + mini + ' AND nb2 <= ' + maxi + ') '\
                    ') OR '\
                    '(nb2 = ' + str(common_nb) + ' '\
                    'AND (nb1 >= ' + mini + ' AND nb1 <= ' + maxi + ') '\
                    '))'
            elif (kw == "prevails" or kw.startswith("info_") or kw == "union"
                  or kw == 'table_name' or kw == 'no_order_by_random'):
                # __
                pass
            elif kw == "multi_reversed":
                result += " AND multirev_locked = 0 "
            elif kw.endswith("_to_check"):
                k = kw[:-9]
                result += " AND " + k + "_min" + " <= " + str(kwargs[kw]) + " "
                result += " AND " + k + "_max" + " >= " + str(kwargs[kw]) + " "
            elif kw.endswith("_min"):
                k = kw[:-4]
                result += " AND " + k + " >= " + str(kwargs[kw]) + " "
            elif kw.endswith("_max"):
                k = kw[:-4]
                result += " AND " + k + " <= " + str(kwargs[kw]) + " "
            elif kw == "not_in":
                updated_notin_list = list(kwargs[kw])
                for c in self.valcols:
                    if c in kwargs and kwargs[c] in updated_notin_list:
                        updated_notin_list.remove(kwargs[c])
                if "prevails" in kwargs:
                    for n in kwargs["prevails"]:
                        if n in updated_notin_list:
                            updated_notin_list.remove(n)
                if len(updated_notin_list):
                    for c in self.valcols:
                        result += " AND " + c + " NOT IN (" + ", "\
                            .join(str(x) for x in updated_notin_list) + ") "
            elif kw.startswith("either_") and kw.endswith("_in"):
                k = kw.split(sep='_')[1:-1]
                result += " AND ( " + k[0] + " IN (" + ", "\
                    .join(str(x) for x in kwargs[kw]) + ") OR "\
                    + k[1] + " IN (" + ", "\
                    .join(str(x) for x in kwargs[kw]) + ") )"
            elif kw.endswith("_in"):
                k = kw[:-3]
                result += " AND " + k + " IN (" + ", "\
                    .join(str(x) for x in kwargs[kw]) + ") "
            elif kw == 'rectangle':
                result += " AND nb1 != nb2 "
            elif kw == 'square':
                result += " AND nb1 = nb2 "
            elif kw == 'diff7atleast':
                result += " AND nb2 - nb1 >= 7 "
            else:
                result += " AND " + kw + " = '" + str(kwargs[kw]) + "' "
        return result

    ##
    #   @brief  Concatenates the different parts of the query
    def _cmd(self, **kwargs):
        if 'union' in kwargs:
            kwargs2 = kwargs.pop('union')
            return "SELECT * FROM (" \
                + self._cmd(no_order_by_random=True, **kwargs) \
                + " UNION " \
                + self._cmd(no_order_by_random=True, **kwargs2) \
                + ") ORDER BY random() LIMIT 1;"
        else:
            order_by_random = "ORDER BY random() LIMIT 1;"
            if 'no_order_by_random' in kwargs:
                order_by_random = ""
            return self._select_part(**kwargs) + " WHERE drawDate = 0 " \
                + self._language_part(**kwargs) \
                + self._kw_conditions(**kwargs) \
                + order_by_random

    ##
    #   @brief  Executes the query. If no result, resets the table and executes
    #           the query again. Returns the query's result.
    def _query_result(self, cmd, **kwargs):
        log = settings.dbg_logger.getChild('db')
        log.debug(cmd)
        qr = tuple(shared.db.execute(cmd))
        if not len(qr):
            self._reset(**kwargs)
            qr = tuple(shared.db.execute(cmd))
        return qr

    ##
    #   @brief  Set the drawDate to datetime() in all entries where col_name
    #           has a value of col_match.
    def _timestamp(self, col_name, col_match, **kwargs):
        shared.db.execute(
            "UPDATE " + self.table_name
            + " SET drawDate = datetime()"
            + " WHERE " + col_name + " = '" + str(col_match) + "';")
        if 'union' in kwargs:
            shared.db.execute(
                "UPDATE " + kwargs['union']['table_name']
                + " SET drawDate = datetime()"
                + " WHERE " + col_name + " = '" + str(col_match) + "';")

    ##
    #   @brief  Will 'lock' some entries
    def _lock(self, t, **kwargs):
        if 'multi_reversed' in kwargs:
            if t in kwargs['info_multirev']:
                for couple in kwargs['info_multirev'][t]:
                    shared.db.execute(
                        "UPDATE " + self.table_name
                        + " SET multirev_locked = 1"
                        + " WHERE nb1 = '" + str(couple[0])
                        + "' and nb2 = '" + str(couple[1]) + "';")

    ##
    #   @brief  Synonym of self.next(), but makes the source an Iterator.
    def __next__(self):
        return self.next()

    ##
    #   @brief  Handles the choice of the next value to return from the
    #           database
    def next(self, **kwargs):
        t = self._query_result(self._cmd(**kwargs), **kwargs)[0]
        self._timestamp(str(self.idcol), str(t[0]), **kwargs)
        self._lock(t[1:len(t)], **kwargs)
        if len(t) == 2:
            return t[1]
        else:
            return t[1:len(t)]
