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

import re
import copy
import json
import random
import warnings
from decimal import Decimal

from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.constants.numeration import RANKS, RANKS_CONFUSING
from mathmaker.lib.tools.maths import coprime_generator, generate_decimal
from mathmaker.lib.tools.numbers import is_integer, is_number, Number
from mathmaker.lib.core.base_calculus import Fraction

DIGITS_POSITIONS = RANKS

FETCH_TABLE_NAME = re.compile(r'CREATE TABLE (\w+)')
FETCH_TABLE_COLS = re.compile(r', (\w\w+)|\n[ ]+(\w\w+)|\((\w\w+)')


def parse_sql_creation_query(qr):
    """Retrieve table's name and columns' names from sql query."""
    return (FETCH_TABLE_NAME.findall(qr)[0],
            [elt
             for t in FETCH_TABLE_COLS.findall(qr)
             for elt in t
             if elt != ''])


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

    def _twothirds_reset(self):
        """Will reset only two thirds of the already timestamped entries."""
        log = settings.dbg_logger.getChild('db')
        n = tuple(shared.db.execute('SELECT COUNT(*) from {} '
                                    'WHERE drawDate != 0;'
                                    .format(self.table_name)))[0][0]
        lim = Number(Number('0.67') * Number(n)).rounded(Decimal('1'))
        log.debug(' 2/3 RESET: {}/{}\n'.format(lim, n))
        shared.db.execute('UPDATE {table_name} SET drawDate=0 '
                          'WHERE id IN '
                          '(SELECT id FROM {table_name}'
                          ' WHERE drawDate != 0'
                          ' ORDER BY drawDate LIMIT {nb});'
                          .format(table_name=self.table_name,
                                  nb=lim))

    ##
    #   @brief  Resets the drawDate of all table's entries (to 0)
    def _reset(self, **kwargs):
        shared.db.execute("UPDATE " + self.table_name + " SET drawDate = 0;")
        if "lock_equal_products" in kwargs:
            shared.db.execute("UPDATE "
                              + self.table_name
                              + " SET lock_equal_products = 0;")
        if "union" in kwargs:
            shared.db.execute("UPDATE "
                              + kwargs['union']['table_name']
                              + " SET drawDate = 0;")
        if (not len(tuple(shared.db.execute(self._cmd(**kwargs))))
            and 'not_in' in kwargs):
            if 'nb1_min' in kwargs and 'nb1_max' in kwargs:
                kwargs.update({'not_in': [str(n)
                                          for n in kwargs['not_in']
                                          if not (Decimal(kwargs['nb1_min'])
                                                  <= Decimal(n)
                                                  <= Decimal(kwargs['nb1_max'])
                                                  )]
                               })
            if 'nb2_min' in kwargs and 'nb2_max' in kwargs:
                kwargs.update({'not_in': [str(n)
                                          for n in kwargs['not_in']
                                          if not (Decimal(kwargs['nb2_min'])
                                                  <= Decimal(n)
                                                  <= Decimal(kwargs['nb2_max'])
                                                  )]
                               })
        return kwargs

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

        def hook(i):
            """Return ' AND ' if i != 0, else ''"""
            yield ' AND ' if i else ''

        # kn stands for keyword number
        # It must be updated (+=1) ONLY if a keyword has led to add a condition
        # indeed. Hence it - alas - CANNOT be handled by enumerate(kwargs).
        kn = 0
        for kw in kwargs:
            if kw == "raw":
                result += next(hook(kn)) + kwargs[kw] + " "
                kn += 1
            elif kw.endswith('_notmod'):
                k = kw[:-7]
                result += next(hook(kn)) + k + " % " + str(kwargs[kw]) \
                    + " != 0 "
                kn += 1
            elif kw == "triangle_inequality":
                common_nb, t1, t2 = kwargs[kw]
                mini = str(abs(t1 - t2) + 1)  # we avoid "too flat" triangles
                maxi = str(t1 + t2 - 1)
                result += next(hook(kn)) + ' ( '\
                    '( nb1 = ' + str(common_nb) + ' '\
                    'AND ( nb2 >= ' + mini + ' AND nb2 <= ' + maxi + ' ) '\
                    ') OR '\
                    '( nb2 = ' + str(common_nb) + ' '\
                    'AND ( nb1 >= ' + mini + ' AND nb1 <= ' + maxi + ' ) '\
                    ')) '
                kn += 1
            elif (kw == "prevails" or kw.startswith("info_") or kw == "union"
                  or kw == 'table_name' or kw == 'no_order_by_random'):
                # __
                pass
            elif kw == "lock_equal_products":
                result += next(hook(kn)) + " lock_equal_products = 0 "
                kn += 1
            elif kw.endswith("_to_check"):
                k = kw[:-9]
                result += next(hook(kn)) + k + "_min" + " <= " \
                    + str(kwargs[kw]) + " "
                result += ' AND ' + k + "_max" + " >= " \
                    + str(kwargs[kw]) + " "
                kn += 1
            elif kw.endswith("_min"):
                k = kw[:-4]
                result += next(hook(kn)) + k + " >= " + str(kwargs[kw]) + " "
                kn += 1
            elif kw.endswith("_max"):
                k = kw[:-4]
                result += next(hook(kn)) + k + " <= " + str(kwargs[kw]) + " "
                kn += 1
            elif kw == "not_in":
                updated_notin_list = list(kwargs[kw])
                for c in self.valcols:
                    if c in kwargs and kwargs[c] in updated_notin_list:
                        updated_notin_list.remove(kwargs[c])
                # prevails is used to not prevent numbers to be drawn twice in
                # a row, like when drawing multiples of the same number, or
                # drawing complements to the same number (e.g. 100)
                # Take care it must contain a list of str (e.g. ['100'])
                if "prevails" in kwargs:
                    for n in kwargs["prevails"]:
                        if n in updated_notin_list:
                            updated_notin_list.remove(n)
                if len(updated_notin_list):
                    for i, c in enumerate(self.valcols):
                        result += next(hook(kn + i)) + c + " NOT IN ( " + ", "\
                            .join(str(x) if is_number(x)
                                  else "'{}'".format(x)
                                  for x in updated_notin_list) + " ) "
                        kn += 1
            elif kw.startswith("either_") and kw.endswith("_in"):
                k = kw.split(sep='_')[1:-1]
                result += next(hook(kn)) + " ( " + k[0] + " IN ( " + ", "\
                    .join(str(x) for x in kwargs[kw]) + " ) OR "\
                    + k[1] + " IN ( " + ", "\
                    .join(str(x) for x in kwargs[kw]) + " ) ) "
                kn += 1
            elif kw.endswith("_in"):
                k = kw[:-3]
                result += next(hook(kn)) + k + " IN ( " + ", "\
                    .join(str(x) for x in kwargs[kw]) + " ) "
                kn += 1
            elif kw == 'rectangle':
                if any([kw.startswith('nb2') for kw in kwargs]):
                    result += next(hook(kn)) + "nb1 != nb2 "
                    kn += 1
            elif kw == 'square':
                if any([kw.startswith('nb2') for kw in kwargs]):
                    result += next(hook(kn)) + " nb1 = nb2 "
                    kn += 1
            elif kw == 'diff7atleast':
                result += next(hook(kn)) + " nb2 - nb1 >= 7 "
                kn += 1
            elif kw.endswith('_noqr'):
                pass
            else:  # default interpretation is " AND key = value "
                key = kw
                rel_sign = " = "
                if kw.endswith('_lt'):
                    rel_sign = " < "
                    key = kw[:-3]
                # If following lines become useful, don't forget to update
                # other places (search for '_gt')
                # if kw.endswith('_gt'):
                #     rel_sign = " > "
                #     key = kw[:-3]
                if kw.endswith('_ge'):
                    rel_sign = " >= "
                    key = kw[:-3]
                elif kw.endswith('_neq'):
                    rel_sign = " != "
                    key = kw[:-4]
                simple_quote = ""
                try:  # automatic detection of integers
                    int(kwargs[kw])
                except ValueError as excinfo:
                    if ('invalid literal for int() with base 10'
                        in str(excinfo)):
                        simple_quote = "'"
                    else:
                        raise
                result += next(hook(kn)) + key + rel_sign + simple_quote \
                    + str(kwargs[kw]) + simple_quote + " "
                kn += 1
        return 'AND ( {} ) '.format(result) if result else ''

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
            order_by_random = " ORDER BY random() LIMIT 1;"
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
            self._twothirds_reset()
            qr = tuple(shared.db.execute(cmd))
            if not len(qr):
                log.debug('FULL RESET\n')
                kwargs = self._reset(**kwargs)
                cmd1 = self._cmd(**kwargs)
                qr = tuple(shared.db.execute(cmd1))
                if not len(qr):
                    if ' nb1 ' in cmd1 and ' nb2 ' in cmd1:
                        cmd2 = cmd1.replace(' nb1 ', 'TEMP') \
                            .replace(' nb2 ', ' nb1 ') \
                            .replace('TEMP', ' nb2 ')
                        cmd2 = cmd2.replace(' nb1_', 'TEMP') \
                            .replace(' nb2_', ' nb1_') \
                            .replace('TEMP', ' nb2_')
                        qr = tuple(shared.db.execute(cmd2))
                        if not len(qr):
                            logm = settings.mainlogger
                            logm.error('Query result is empty:\nQUERY1\n{}\n'
                                       'QUERY2\n{}\nQUERY3\n{}\n'
                                       .format(cmd, cmd1, cmd2))
        log.debug('Query result = {}\n'.format(qr))
        return qr

    ##
    #   @brief  Set the drawDate to datetime() in all entries where col_name
    #           has a value of col_match.
    def _timestamp(self, col_name, col_match, **kwargs):
        shared.db.execute(
            "UPDATE " + self.table_name
            + " SET drawDate = strftime('%Y-%m-%d %H:%M:%f')"
            + " WHERE " + col_name + " = '" + str(col_match) + "';")
        if 'union' in kwargs:
            shared.db.execute(
                "UPDATE " + kwargs['union']['table_name']
                + " SET drawDate = strftime('%Y-%m-%d %H:%M:%f')"
                + " WHERE " + col_name + " = '" + str(col_match) + "';")

    ##
    #   @brief  Will 'lock' some entries
    def _lock(self, t, **kwargs):
        if 'lock_equal_products' in kwargs:
            if t in kwargs['info_lock']:
                shared.db.execute(
                    "UPDATE " + self.table_name
                    + " SET lock_equal_products = 1"
                    + " WHERE nb1 = '" + str(t[0])
                    + "' and nb2 = '" + str(t[1]) + "';")
                for couple in kwargs['info_lock'][t]:
                    shared.db.execute(
                        "UPDATE " + self.table_name
                        + " SET lock_equal_products = 1"
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
        sql_query = self._cmd(**kwargs)
        query_result = self._query_result(sql_query, **kwargs)
        if not len(query_result):
            raise RuntimeError('No result from database query. Command was:\n'
                               + str(sql_query))
        t = query_result[0]
        self._timestamp(str(self.idcol), str(t[0]), **kwargs)
        self._lock(t[1:len(t)], **kwargs)
        if len(t) == 2:
            return t[1]
        else:
            return t[1:len(t)]


def db_table(tag):
    """Table's name possibly associated to tag."""
    if (tag.startswith('intpairs_') or tag.startswith('table_')
        or tag.startswith('multiplesof') or tag.startswith('complements_to_')):
        return 'int_pairs'
    elif tag.startswith('singleint_'):
        return 'single_ints'
    elif tag.startswith('singledeci1_'):
        return 'single_deci1'
    elif tag == 'unitspairs':
        return 'units_conversions'
    elif tag == 'decimalfractionssums':
        return 'decimals'
    elif tag in ['int_deci_clever_pairs', 'digits_places', 'fracdigits_places',
                 'decimals']:
        return tag
    return ''


##
#   @brief  Will tell if the tag belongs to int pairs, decimal numbers etc.
def classify_tag(tag):
    if (tag.startswith('intpairs_') or tag.startswith('table_')
        or tag.startswith('multiplesof') or tag.startswith('complements_to_')):
        # __
        return 'int_pairs'
    elif tag.startswith('singleint_'):
        return 'single_int'
    elif tag.startswith('singledeci1_'):
        return 'single_deci1'
    elif tag in ['int_deci_clever_pairs',
                 'int_irreducible_frac', 'nothing',
                 'decimal_and_10_100_1000_for_multi',
                 'decimal_and_10_100_1000_for_divi',
                 'decimal_and_one_digit_for_multi',
                 'decimal_and_one_digit_for_divi',
                 'unitspairs', 'digits_places', 'fracdigits_places',
                 'decimals', 'decimalfractionssums', 'extdecimals']:
        # __
        return tag
    raise ValueError(tag + " is not recognized as a valid 'tag' that can be "
                     "used in a mathmaker xml file.")


def preprocess_qkw(table_name, qkw=None):
    """Add relevant questions keywords to build the query."""
    with open(settings.db_index_path) as f:
        db_index = json.load(f)
    if table_name not in db_index:
        return {}
    d = {}
    if qkw is None:
        qkw = {}
    for kw in qkw:
        if any([kw.startswith(ref)
                for ref in db_index[table_name]]):
            d.update({kw: qkw[kw]})
    return d


##
#   @brief  Will turn the tag into the matching conditions for the db query.
#           Note that any value matching a 'nbN' key (like 'nb1': '11') will
#           be automatically removed from any "NOT IN(...)" condition in a
#           query. The "raw" keyword allows to give more complex queries but
#           as the 'nbN' keys are then "buried" inside the query string, it's
#           possible to add a "prevail": 'value' in the returned dictionary
#           to allow this very same behaviour (as directly adding a
#           'nbN': 'value' may change the query).
#   @return A dictionary
def preprocess_int_pairs_tag(tag, qkw=None):
    if qkw is None:
        qkw = {}
    d = {}
    if tag.startswith('complements_to_'):
        step = 1
        upper_bounds = tag[15:]
        if '...' in upper_bounds:
            mini, maxi = [int(n) for n in upper_bounds.split('...')]
            if mini % 10 == 0 and maxi % 10 == 0:
                step = 10
            if mini % 100 == 0 and maxi % 100 == 0:
                step = 100
            upper_bound = random.choice([n * step + mini
                                         for n in range(maxi // step
                                                        - mini // step + 1)])
        else:
            upper_bound = int(upper_bounds)
        if qkw.get('nb_variant', 'default').startswith('decimal'):
            upper_bound *= 10
            step = 10
        d = {'nb2': upper_bound, 'nb1_lt': upper_bound // 2 + 1,
             'prevails': [str(upper_bound)]}
        if step != 1:
            d.update({'nb1_notmod': step})
    # 'table_11' is a shortcut for a special range
    elif tag == 'table_11_ones':
        d = {'nb1_in': ['2', '3', '4', '5', '6', '7', '8', '9'],
             'nb2': '11'}
    elif tag == 'table_11_tens_easy':
        d = {'nb2_in': ['11', '12', '13', '14', '15', '16', '17', '18', '21',
                        '22', '23', '24', '25', '26', '27', '31', '32', '33',
                        '34', '35', '36', '41', '42', '43', '44', '45', '51',
                        '52', '53', '54', '61', '62', '63', '71', '72', '81'],
             'nb1': '11'}
    elif tag == 'table_11_tens_hard':
        d = {'nb2_in': ['19', '28', '29', '37', '37', '39', '46', '47', '48',
                        '49', '55', '56', '57', '58', '59', '64', '65', '66',
                        '67', '68', '69', '73', '74', '75', '76', '77', '78',
                        '79', '82', '83', '84', '85', '86', '87', '88', '89',
                        '91', '92', '93', '94', '95', '96', '97', '98', '99'],
             'nb1': '11'}
    elif tag == 'table_11_tens':
        d = {'nb2_in': [str(n + 11) for n in range(89)],
             'nb1': '11'}
    # 'table_N' is a shortcut for 'multiplesofN_2to9' if N <= 10
    # and for 'multiplesofN_2to6' if N >= 12 (11 is managed separately)
    elif tag.startswith('table_'):
        n = int(tag[6:])
        r = "_2to9" if n <= 10 else "_2to6"
        tag = 'multiplesof' + str(n) + r

    if tag.startswith('intpairs_'):
        if '×' not in tag:
            n1, n2 = tag[9:].split(sep='to')
            d = {'nb1_min': n1, 'nb1_max': n2,
                 'nb2_min': n1, 'nb2_max': n2}
        else:
            nb1_part, nb2_part = tag.replace('intpairs_', '').split(sep='×')
            min1, max1 = nb1_part.split(sep='to')
            min2, max2 = nb2_part.split(sep='to')
            d = {'nb1_min': min1, 'nb1_max': max1,
                 'nb2_min': min2, 'nb2_max': max2}
    elif tag.startswith('multiplesof'):
        N, r = tag[11:].split(sep='_')
        mini, maxi = r.split(sep='to')
        d = {'raw': '(nb1 = ' + N + ' and (nb2 >= ' + mini
                    + ' and nb2 <= ' + maxi + ')) or (nb2 = ' + N
                    + ' and (nb1 >= ' + mini + ' and nb1 <= ' + maxi + '))',
             'prevails': [N]}

    return d


def preprocess_single_nb_tag(tag):
    """From single..._mintomax, get and return min and max in a dictionary."""
    n1, n2 = tag.split(sep='_')[1].split(sep='to')
    return {'nb1_min': n1, 'nb1_max': n2}


def preprocess_units_pairs_tag(tag, last_draw=None, qkw=None):
    """
    Create the SQL query according to last_draw content and possible qkw.
    """
    d = {}
    if qkw is None:
        qkw = {}
    if last_draw is None:
        last_draw = {}
    if 'level' in qkw:
        d.update({'level': qkw['level']})
    else:
        d.update({'level': 1})
    if 'category' in qkw:
        d.update({'category': qkw['category']})
    elif len(last_draw) >= 5:
        d.update({'category_neq': last_draw[3]})
    if 'direction' in qkw:
        d.update({'direction': qkw['direction']})
    elif len(last_draw) >= 5:
        d.update({'direction_neq': last_draw[2]})
    return d


def preprocess_decimals_query(qkw=None):
    """
    Create the SQL query according to possible qkw.
    """
    d = {}
    if qkw is None:
        qkw = {}
    if 'fd' not in qkw:
        d.update(
            {'fd': Number(str(shared.fracdigits_places_source
                              .next())).fracdigits_nb()})
        if 'iz' in qkw and int(qkw['iz']) >= d['fd']:
            d['fd'] = int(qkw['iz']) + 1
        if 'iz_ge' in qkw and int(qkw['iz_ge']) >= d['fd']:
            d['fd'] = int(qkw['iz_ge']) + 1
        # if 'iz_gt' in qkw and qkw['iz_gt'] >= d['fd']:
        #     d['fd'] = qkw['iz_gt'] + 1
    else:
        d.update({'fd': qkw['fd']})
    return d


def preprocess_extdecimals_query(qkw=None):
    """
    Create the SQL query according to possible qkw.
    """
    if qkw is None:
        qkw = {}
    d = {}
    d.update({'position': qkw.get('position', None)})
    d.update({'width': qkw.get('width', 'random')})
    d.update({'generation_type': qkw.get('generation_type', 'default')})
    d.update({'pos_matches_invisible_zero':
              qkw.get('pos_matches_invisible_zero', False)})
    d.update({'unique_figures': qkw.get('unique_figures', True)})
    d.update({'grow_left': qkw.get('grow_left', False)})
    d.update({'numberof': qkw.get('numberof', False)})
    d.update({'digits_positions': qkw.get('digits_positions', None)})
    return d


def preprocess_decimalfractions_pairs_tag(qkw=None, **kwargs):
    """
    Create the SQL query according to possible qkw's overlap value.

    :param qkw: keywords provided by the question
    :type qkw: dict
    :rtype: dict
    """
    return {'overlap_level_ge': qkw.get('overlap', 0),
            'overlap_noqr': qkw.get('overlap', 0)}


def postprocess_decimalfractionssums_query(qr, qkw=None, **kwargs):
    """
    Create two decimal fractions from the drawn decimal number.

    :param qr: the result of the query (containing the decimal number)
    :type qr: tuple
    :rtype: tuple
    """
    variant = qkw.get('variant', 'random')
    if variant == 'random':
        variant = random.choice(['atomize', 'cut'])
    if variant == 'atomize':
        decimals = Number(str(qr)).atomized()
    else:
        decimals = Number(str(qr)).cut(overlap=kwargs['overlap_noqr'])
    if is_integer(decimals[0]) and (len(decimals) >= 3
                                    or random.choice([True, False])):
        first = decimals[0]
    else:
        first = Fraction(decimals[0])
    return (first, *[Fraction(decimals[i + 1])
                     for i in range(len(decimals) - 1)])


##
#   @brief  Generates a list of values to be used
#   @todo   Several cases should be factorized or maybe later moved to the db
def generate_values(source_id):
    if source_id == 'int_irreducible_frac':
        return [(k, Fraction((n, k))) for k in [i + 2 for i in range(18)]
                for n in coprime_generator(k)]

    elif source_id == 'alternate':
        l = [('left', ), ('right', )]
        random.shuffle(l)
        return l * 20

    elif source_id == 'trigo_functions':
        return ['cos', 'cos', 'sin', 'sin', 'tan', 'tan']

    elif source_id == 'trigo_vocabulary':
        return ['adjacent', 'adjacent', 'opposite', 'opposite']

    elif source_id == 'decimal_and_10_100_1000_for_multi':
        box_10_100_1000 = [10, 100, 1000]
        result = set()
        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]
            chosen_10_100_1000 = box_10_100_1000.pop()
            digits_positions = list(RANKS[2:])
            width = random.choices([1, 2, 3], weights=[0.14, 0.63, 0.33])[0]
            start_pos = random.choice([n
                                       for n in range(len(digits_positions))])
            result |= {(chosen_10_100_1000,
                        generate_decimal(width, digits_positions, start_pos))}
        return list(result)

    elif source_id == 'decimal_and_10_100_1000_for_divi':
        box_10_100_1000 = [10, 100, 1000]
        result = set()
        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]
            chosen_10_100_1000 = box_10_100_1000.pop()
            digits_positions = list(RANKS[2:])
            width = random.choices([1, 2, 3], weights=[0.14, 0.63, 0.33])[0]
            wt = {10: [0.2, 0.2, 0.2, 0.2, 0.2],
                  100: [0.25, 0.25, 0.25, 0.25, 0],
                  1000: [0.34, 0.33, 0.33, 0, 0]}
            start_pos = random.choices([n
                                        for n
                                        in range(len(digits_positions))],
                                       weights=wt[chosen_10_100_1000])[0]
            result |= {(chosen_10_100_1000,
                        generate_decimal(width, digits_positions, start_pos))}
        return list(result)

    elif source_id == 'decimal_and_one_digit_for_multi':
        box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
        result = set()
        for n in range(20):
            if not box:
                box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
            chosen = box.pop()
            digits_positions = list()
            if chosen == Decimal('0.1'):
                digits_positions = list(RANKS[:-1])
            elif chosen == Decimal('0.01'):
                digits_positions = list(RANKS[:-2])
            elif chosen == Decimal('0.001'):
                digits_positions = list(RANKS[:-3])
            width = random.choices([1, 2, 3, 4],
                                   weights=[0.14, 0.43, 0.33, 0.2])[0]
            start_pos = random.choice([n
                                       for n in range(len(digits_positions))])
            result |= {(chosen,
                        generate_decimal(width, digits_positions, start_pos))}
        return list(result)

    elif source_id == 'decimal_and_one_digit_for_divi':
        box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
        result = set()
        for n in range(20):
            if not box:
                box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
            chosen = box.pop()
            digits_positions = list()
            if chosen == Decimal('0.1') or chosen == Decimal('0.01'):
                digits_positions = list(RANKS)
            elif chosen == Decimal('0.001'):
                digits_positions = list(RANKS[1:])
            width = random.choices([1, 2, 3, 4],
                                   weights=[0.14, 0.43, 0.33, 0.2])[0]
            start_pos = random.choice([n
                                       for n in range(len(digits_positions))])
            result |= {(chosen,
                        generate_decimal(width, digits_positions, start_pos))}
        return list(result)

    elif source_id in ['nothing', 'bypass']:
        return []


def generate_random_decimal_nb(position=None, width='random',
                               generation_type=None,
                               pos_matches_invisible_zero=False,
                               unique_figures=True,
                               grow_left=False,
                               numberof=False,
                               digits_positions=None, **unused):
    if position is None:
        position = Decimal(str(shared.fracdigits_places_source.next()))
    if generation_type is None:
        if numberof:
            generation_type = 'default'
        else:
            generation_type = random.choice(['default', 'alternative'])
    chosen_deci = Decimal('0')
    figures = [str(i + 1) for i in range(9)]
    if not unique_figures:
        figures = figures * 3
    random.shuffle(figures)
    if digits_positions is None:
        digits_positions = copy.copy(DIGITS_POSITIONS)

    if (isinstance(width, str)
        and width.startswith('random') and width != 'random'):
        if len(width.split('_')) != 2:
            width = 'random'
            warnings.warn('Malformed random width. '
                          'A random value will be chosen instead.'
                          .format(width, len(digits_positions)))
        else:
            _, span = width.split('_')
            if not len(span.split('to')) == 2:
                width = 'random'
                warnings.warn('Malformed random width\'s span. '
                              'A random value will be chosen instead.'
                              .format(width, len(digits_positions)))
            else:
                mini, maxi = span.split('to')
                try:
                    mini, maxi = int(mini), int(maxi)
                except ValueError:
                    width = 'random'
                    warnings.warn('Malformed random width\'s span bounds '
                                  '(both should be int). '
                                  'A random value will be chosen instead.'
                                  .format(width, len(digits_positions)))
                else:
                    width = random.choice([i + 1
                                           for i
                                           in range(max(maxi - mini + 1, 1))])
    elif width != 'random':
        try:
            width = int(width)
            if not (1 <= width <= len(digits_positions)):
                width = 'random'
                warnings.warn('The chosen width ({}) is not greater than 1 '
                              'and lower than the length of digits positions'
                              ' ({}). '
                              'A random value will be chosen instead.'
                              .format(width, len(digits_positions)))
        except ValueError:
            raise ValueError('As width you can specify either \'random\', '
                             '\'random_xtoy\' or an int.')
    if width == 'random':
        if generation_type == 'default':
            width = random.choice([3, 4, 5, 6, 7])
        else:
            width = random.choices([2, 3, 4, 5],
                                   cum_weights=[0.1, 0.4, 0.75, 1])[0]
        if numberof:
            width = random.choices([2, 3, 4, 5],
                                   cum_weights=[0.15, 0.55, 0.85, 1])[0]

    # Two different ways to generate a number. Here is the "default" one:
    if generation_type == 'default':
        positions = []

        if not pos_matches_invisible_zero:
            if grow_left:
                positions = [digits_positions.index(position) - p
                             for p in range(width)]
            elif not numberof:
                # High positions are to the right of the numeral,
                # while low positions are to the left
                lr = digits_positions.index(position) - width + 1
                lowest_start_pos = lr if lr >= 0 else 0

                hr = digits_positions.index(position)
                highest_start_pos = hr if hr + width < len(digits_positions) \
                    else len(digits_positions) - 1 - width
                highest_start_pos = highest_start_pos \
                    if highest_start_pos >= lowest_start_pos \
                    else lowest_start_pos

                possible_start_positions = [lowest_start_pos + p
                                            for p in range(
                                                highest_start_pos
                                                - lowest_start_pos + 1)]

                start_pos = random.choice(possible_start_positions)

                positions = [start_pos + p for p in range(width)]

            else:
                # High positions are to the right of the numeral,
                # while low positions are to the left
                positions += [digits_positions.index(position)]
                # Probability to fill a higher position rather than a lower one
                phr = 0.5
                hr = lr = digits_positions.index(position)
                for i in range(width - 1):
                    if lr == 0:
                        phr = 1
                    elif hr == len(digits_positions) - 1:
                        phr = 0

                    if random.random() < phr:
                        hr += 1
                        positions += [hr]
                        phr *= 0.4
                    else:
                        lr -= 1
                        positions += [lr]
                        phr *= 2.5

        else:  # position matches invisible zero
            if position <= Decimal('0.1'):
                positions = [digits_positions.index(p)
                             for p in digits_positions
                             if p > position]
                width = min(width, len(positions))
                positions = positions[-width:]
            elif (position >= Decimal('10')
                  or (position == Decimal('1')
                      and random.choice([True, False]))):
                positions = [digits_positions.index(p)
                             for p in digits_positions
                             if p < position]
                width = min(width, len(positions))
                positions = positions[:width]
            else:  # units, second possibility
                positions = [digits_positions.index(p)
                             for p in digits_positions
                             if p != position]
                width = min(width, len(positions))
                maxi_start = len(positions) - width + 1
                slice_start = random.choice([i for i in range(maxi_start)])
                positions = positions[slice_start:slice_start + width]

        # Let's start the generation of the number:
        for p in positions:
            figure = figures.pop()
            chosen_deci += Decimal(figure) * digits_positions[p]

    # "Alternative" way of generating a number randomly:
    else:
        figure = '0' if pos_matches_invisible_zero \
            else figures.pop()

        chosen_deci += Decimal(figure) * position
        digits_positions.remove(position)

        if pos_matches_invisible_zero:
            if position <= Decimal('0.1'):
                next_pos = position * Decimal('10')
                figure = figures.pop()
                chosen_deci += Decimal(figure) * next_pos
                digits_positions = [p
                                    for p in digits_positions
                                    if p > next_pos]
            elif position >= Decimal('10'):
                next_pos = position * Decimal('0.1')
                figure = figures.pop()
                chosen_deci += Decimal(figure) * next_pos
                digits_positions = [p
                                    for p in digits_positions
                                    if p < next_pos]

        width = min(width, len(digits_positions))

        if position != Decimal('1') and not pos_matches_invisible_zero:
            figure = figures.pop()
            r = RANKS_CONFUSING[-(RANKS_CONFUSING.index(position) + 1)]
            chosen_deci += Decimal(figure) * r
            digits_positions.remove(r)
            width -= 1

        for i in range(width):
            figure = figures.pop()
            r = random.choice(digits_positions)
            digits_positions.remove(r)
            chosen_deci += Decimal(figure) * r

    return chosen_deci


class sub_source(object):
    ##
    #   @brief  Initializer
    def __init__(self, source_id, **kwargs):
        self.ondemand = kwargs.get('ondemand', False)
        if self.ondemand:
            self.values = []
            self.generator_fct = kwargs.get('generator_fct')
        else:
            self.values = generate_values(source_id)
        random.shuffle(self.values)
        self.current = 0
        self.max = len(self.values)

    ##
    #   @brief  Resets the source
    def _reset(self):
        random.shuffle(self.values)
        self.current = 0

    ##
    #   @brief  Synonym of self.next(), but makes the source an Iterator.
    def __next__(self):
        return self.next()

    ##
    #   @brief  Handles the choice of the next value to return
    def next(self, qkw=None, **kwargs):
        # qkw is only here for compatibility with source class
        # it must be "merged" with kwargs during preprocessing
        if self.ondemand:
            return self.generator_fct(**kwargs)
        else:
            if self.current == self.max:
                self._reset()
            self.current += 1
            return self.values[self.current - 1]


class mc_source(object):
    ##
    #   @brief  Handles the choice of the next value to return
    def next(self, source_id, qkw=None, **kwargs):
        if qkw is None:
            qkw = {}
        tag_classification = classify_tag(source_id)
        kwargs.update(preprocess_qkw(db_table(source_id), qkw=qkw))
        if tag_classification == 'int_pairs':
            kwargs.update(preprocess_int_pairs_tag(source_id, qkw=qkw))
            return shared.int_pairs_source.next(**kwargs)
        elif tag_classification.startswith('single'):
            kwargs.update(preprocess_single_nb_tag(source_id))
            return shared.single_ints_source.next(**kwargs)
        elif tag_classification == 'int_deci_clever_pairs':
            return shared.int_deci_clever_pairs_source.next(**kwargs)
        elif tag_classification == 'digits_places':
            return Decimal(str(shared.digits_places_source.next(**kwargs)))
        elif tag_classification == 'fracdigits_places':
            return Decimal(str(shared.fracdigits_places_source.next(**kwargs)))
        elif tag_classification == 'int_irreducible_frac':
            return shared.int_fracs_source.next(**kwargs)
        elif tag_classification == 'decimal_and_10_100_1000_for_multi':
            return shared.deci_10_100_1000_multi_source.next(**kwargs)
        elif tag_classification == 'decimal_and_10_100_1000_for_divi':
            return shared.deci_10_100_1000_divi_source.next(**kwargs)
        elif tag_classification == 'decimal_and_one_digit_for_multi':
            return shared.deci_one_digit_multi_source.next(**kwargs)
        elif tag_classification == 'decimal_and_one_digit_for_divi':
            return shared.deci_one_digit_divi_source.next(**kwargs)
        elif tag_classification == 'unitspairs':
            kwargs.update(preprocess_units_pairs_tag(source_id, qkw=qkw,
                                                     last_draw=kwargs.get(
                                                         'not_in', None)))
            kwargs.pop('not_in', None)
            return shared.unitspairs_source.next(**kwargs)
        elif tag_classification == 'decimals':
            kwargs.update(preprocess_decimals_query(qkw=qkw))
            return shared.decimals_source.next(**kwargs)
        elif tag_classification == 'extdecimals':
            kwargs.update(preprocess_extdecimals_query(qkw=qkw))
            return shared.extdecimals_source.next(**kwargs)
        elif tag_classification == 'decimalfractionssums':
            kwargs.update(preprocess_decimals_query(qkw=qkw))
            kwargs.update(preprocess_decimalfractions_pairs_tag(qkw=qkw,
                                                                **kwargs))
            return postprocess_decimalfractionssums_query(
                shared.decimals_source.next(**kwargs), qkw=qkw, **kwargs)
        elif tag_classification == 'nothing':
            return ()
