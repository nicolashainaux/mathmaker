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

import sys

from lib.sources_tools import bidict, infinite_source
from . import mini_problems_wordings_additions
from . import mini_problems_wordings_substractions
from . import mini_problems_wordings_multiplications
from . import mini_problems_wordings_divisions

initialized = False

def init(**kwargs):
    global mini_problems_wordings_source
    global initialized
    global WORDINGS_MAP

    initialized = True

    if 'sce_nb' in kwargs:
        if kwargs['sce_nb'] == 0:
            mini_problems_wordings_additions.init()
        elif kwargs['sce_nb'] == 1:
            mini_problems_wordings_substractions.init()
        elif kwargs['sce_nb'] == 2:
            mini_problems_wordings_multiplications.init()
        elif kwargs['sce_nb'] == 3:
            mini_problems_wordings_divisions.init()
    else:
        mini_problems_wordings_additions.init()
        mini_problems_wordings_substractions.init()
        mini_problems_wordings_multiplications.init()
        mini_problems_wordings_divisions.init()

    WORDING = { "multi_direct": mini_problems_wordings_multiplications.CONTENT,
                "divi_direct": mini_problems_wordings_divisions.CONTENT,
                "addi_direct": mini_problems_wordings_additions.CONTENT,
                "substr_direct": mini_problems_wordings_substractions.CONTENT
              }

    tables_and_integers_couples = \
    ['table_2_9', 'table_2', 'table_3', 'table_4', 'table_4_9', 'table_2_11_50',
    'table_3_11_50', 'table_4_11_50', 'table_2_9_for_rectangles', 'table_11',
    'table_11_for_rectangles', 'table_15', 'table_25', 'integers_10_100',
    'integers_10_100_for_rectangles', 'integers_5_20',
    'integers_5_20_for_rectangles', 'integers_10_100_for_sums_diffs']

    WORDINGS_MAP = bidict({
    WORDING["multi_direct"]["Marbles"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Golden goose"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Gardener's vegetables"]: \
                                                    tables_and_integers_couples,
    WORDING["multi_direct"]["Candies"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Pencils boxes"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Pens purchase"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Pocket money"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Sheep"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Truffles packets"]: tables_and_integers_couples,
    WORDING["multi_direct"]["Flour packets"]: tables_and_integers_couples,

    WORDING["divi_direct"]["Marbles"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Golden goose"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Gardener's vegetables"]: \
                                                    tables_and_integers_couples,
    WORDING["divi_direct"]["Candies"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Pencils boxes"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Pens purchase"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Pocket money"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Sheep"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Truffles packets"]: tables_and_integers_couples,
    WORDING["divi_direct"]["Flour packets"]: tables_and_integers_couples,

    WORDING["addi_direct"]["Marbles"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Golden goose"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Gardener's vegetables"]: \
                                                    tables_and_integers_couples,
    WORDING["addi_direct"]["Candies"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Ages"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Can"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Book"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Bike ride"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Painted walls"]: tables_and_integers_couples,
    WORDING["addi_direct"]["Sheep"]: tables_and_integers_couples,

    WORDING["substr_direct"]["Marbles"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Golden goose"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Gardener's vegetables"]: \
                                                    tables_and_integers_couples,
    WORDING["substr_direct"]["Candies"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Ages"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Can"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Book"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Bike ride"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Painted walls"]: tables_and_integers_couples,
    WORDING["substr_direct"]["Sheep"]: tables_and_integers_couples,

    })

    if not 'sce_nb' in kwargs:
        mini_problems_wordings_source = infinite_source([\
                                        list(WORDING["addi_direct"].values()),
                                        list(WORDING["substr_direct"].values()),
                                        list(WORDING["multi_direct"].values()),
                                        list(WORDING["divi_direct"].values())
                                        ],
                                        refresh=sub_object)

class sub_object(object):
    def __init__(self):
        pass

    def refresh(sce_nb):
        init(sce_nb=sce_nb)
        if sce_nb == 0:
            return list(mini_problems_wordings_additions.CONTENT.values())
        elif sce_nb == 1:
            return list(mini_problems_wordings_substractions.CONTENT.values())
        elif sce_nb == 2:
            return list(mini_problems_wordings_multiplications.CONTENT.values())
        elif sce_nb == 3:
            return list(mini_problems_wordings_divisions.CONTENT.values())

