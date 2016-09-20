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

import copy
import random
from collections import namedtuple

from mathmaker.lib import shared
from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'': ['default'],
     'std': ['default'],
     'tabular': ['default'],  # reserved to mental calculation
     'slideshow': ['default'],  # reserved to mental calculation
     'bypass': ['']
     }

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']
              }
             }

to_unpack = copy.deepcopy(question.SUBKINDS_TO_UNPACK)
Q_info = namedtuple('Q_info', 'type,kind,subkind,nb_source,options')

MIN_ROW_HEIGHT = 0.8

SWAPPABLE_QKINDS_QSUBKINDS = {("rectangle", "area"),
                              ("rectangle", "perimeter"),
                              ("square", "area"),
                              ("square", "perimeter")}

KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE = {
    ('divi', 'direct', 'area_width_length_rectangle'):
    ('rectangle', 'length_or_width', 'from_area')}


# --------------------------------------------------------------------------
##
#   @brief Will reorganize the raw questions lists into a dictionary
#   @param  q_list          The questions' list
#   @return (q_dict, q_nb)  The questions' dictionary + the total number of
#                           questions
def build_q_dict(q_list):
    # In q_list, each element is like this:
    # [{'kind':'multi', 'subkind':'direct', 'nb':'int'}, ['table_2_9'], 4]
    # [q[0],                                             q[1],          q[2]]
    q_dict = {}
    already_unpacked = set()
    q_nb = 0
    for q in q_list:
        q_nb += q[2]

        for n in range(q[2]):
            q_id = q[0]['kind']
            q_id += "_"

            # Here we 'unpack' some special subkinds.
            subk = q[0]['subkind']
            if subk in question.UNPACKABLE_SUBKINDS:
                already_unpacked |= {subk}
            elif subk in to_unpack:
                subk_left = to_unpack[subk] - already_unpacked
                if not subk_left:
                    already_unpacked -= copy.deepcopy(
                        question.SUBKINDS_TO_UNPACK[subk])
                    to_unpack[subk] = copy.deepcopy(
                        question.SUBKINDS_TO_UNPACK[subk])
                    subk_left = to_unpack[subk] - already_unpacked
                s = list(subk_left)
                random.shuffle(s)
                subk = s.pop()
                already_unpacked |= {subk}

            q_id += subk
            q_options = copy.deepcopy(q[0])
            q_dict.setdefault(q_id, [])
            q_dict[q_id] += [(q[1], q_options['kind'], subk, q_options)]
            del q_options['kind']
            del q_options['subkind']

    return q_dict, q_nb


# --------------------------------------------------------------------------
##
#   @brief Will create a complete and mixed questions' list from q_dict
#   @param  q_dict  The questions' dictionary
#   @return q_list  The new mixed questions' list
def build_mixed_q_list(q_dict):
    # q_dict is organized like this:
    # { 'multi_direct':   [(['table_2_9'], 'multi', 'direct', {'nb':'int'}),
    #                      (['table_2_9'], 'multi', 'direct', {'nb':'int'})],
    #   'multi_reversed': [(['table_2_9'], 'multi', 'reversed', {options})],
    #   'divi_direct':    [(['table_2_9'], 'divi', 'direct', {options})],
    #   'multi_hole':     [(['table_2_9'], 'multi', 'hole', {options})],
    #   'q_id':           [(['table_15'], 'kind', 'subkind', {options})],
    #   'q_id:            [(['table_25'], 'kind', 'subkind', {options})],
    #   'etc.'
    # }
    mixed_q_list = []
    q_id_box = [key for key in q_dict.keys()
                for i in range(len(q_dict[key]))]
    random.shuffle(q_id_box)
    for q_id in q_id_box:
        info = q_dict[q_id].pop(0)
        mixed_q_list += [Q_info(q_id, info[1], info[2], info[0], info[3])]
    return mixed_q_list


# --------------------------------------------------------------------------
##
#   @brief  Determine the
#   @param  q_i     The Q_info object
def get_nb_sources_from_question_info(q_i):
    nb_sources = []
    extra_infos = {'merge_sources': False}
    questions_sources = q_i.nb_source
    if len(q_i.nb_source) == 1 and q_i.nb_source[0].startswith('inttriplets_'):
        questions_sources = ['intpairs_' + q_i.nb_source[0][12:],
                             'intpairs_' + q_i.nb_source[0][12:]]
        extra_infos.update({'merge_sources': True})
    for nb_sce in questions_sources:
        tag_to_unpack = nb_source = nb_sce
        if nb_source in question.SOURCES_TO_UNPACK:
            s = ''
            stu = copy.copy(question.SOURCES_TO_UNPACK)
            if nb_source in ['decimal_and_10_100_1000',
                             'decimal_and_one_digit']:
                # __
                s = stu[nb_source][q_i.type]
            else:
                s = stu[nb_source][q_i.subkind]
            s = list(s)
            random.shuffle(s)
            nb_source = s.pop()
            if (tag_to_unpack == 'auto_vocabulary'
                and q_i.subkind in ['addi', 'subtr']
                and nb_source == 'intpairs_2to200'):
                # __
                q_i.options.update({'variant': 'decimal2'})
        nb_sources += [nb_source]
    return nb_sources, extra_infos


# --------------------------------------------------------------------------
##
#   @brief Increases the disorder of the questions' list
#   @param  l           The list
#   @param  sort_key    The list's objects' attribute that will be used to
#                       determine whether the order should be changed or not
def increase_alternation(l, sort_key):
    if len(l) >= 3:
        for i in range(len(l) - 2):
            if getattr(l[i], sort_key) == getattr(l[i + 1], sort_key):
                if getattr(l[i + 2], sort_key) != getattr(l[i], sort_key):
                    l[i + 1], l[i + 2] = l[i + 2], l[i + 1]

    return l


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Generic
# @brief A default 'void' exercise (will get its questions from...)
class X_Generic(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #          - x_kind=<string>
    #                         see AVAILABLE_X_KIND_VALUES to check the
    #                         possible values to use and their matching
    #                         x_subkind options
    #   @return One instance of exercise.Generic
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        from mathmaker.lib.tools.xml_sheet import get_q_kinds_from
        source_file = options.get('filename')
        (x_kind, q_list) = get_q_kinds_from(
            source_file,
            sw_k_s=SWAPPABLE_QKINDS_QSUBKINDS,
            k_s_ctxt_tr=KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE)

        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        default_question = question.Q_Generic

        # TEXTS OF THE EXERCISE
        self.text = {'exc': options.get('text_exc', ''),
                     'ans': options.get('text_ans', '')}

        if self.text['exc'] != '':
            self.text['exc'] = _(self.text['exc'])

        if self.text['ans'] != '':
            self.text['ans'] = _(self.text['ans'])

        # From q_list, we build a dictionary and then a complete questions'
        # list:
        q_dict, self.q_nb = build_q_dict(q_list)
        # in case of mental calculation exercises we shuffle the questions
        if self.x_kind in ['tabular', 'slideshow']:
            for key in q_dict:
                random.shuffle(q_dict[key])
        mixed_q_list = build_mixed_q_list(q_dict)
        # in case of mental calculation exercises we shuffle the questions
        if self.x_kind in ['tabular', 'slideshow']:
            mixed_q_list = increase_alternation(mixed_q_list, 'type')
            mixed_q_list.reverse()
            mixed_q_list = increase_alternation(mixed_q_list, 'type')

        # mixed_q_list is organized like this:
        # [('type', 'kind', 'subkind', 'nb_source', 'options'),
        #  ('q_id', 'q', 'id', 'table_15', {'nb':}),
        #  ('multi_direct', 'multi', 'direct', ['table_2_9'], {'nb':}),
        #  etc.
        # ]

        # Now, we generate the numbers & questions, by type of question first
        self.questions_list = []
        last_draw = [0, 0]
        for q in mixed_q_list:
            nb_sources, extra_infos = get_nb_sources_from_question_info(q)
            nb_to_use = tuple()
            for i, nb_source in enumerate(nb_sources):
                if i == 1 and extra_infos['merge_sources']:
                    nb_to_use += shared.mc_source\
                        .next(nb_source,
                              either_nb1_nb2_in=last_draw,
                              **question.get_modifier(q.type, nb_source))
                else:
                    drawn = shared.mc_source.next(nb_source,
                                                  not_in=last_draw,
                                                  **question
                                                  .get_modifier(
                                                      q.type,
                                                      nb_source))
                    if isinstance(drawn, int):
                        nb_to_use += (drawn, )
                    else:
                        nb_to_use += drawn
                last_draw = [str(n) for n in set(nb_to_use)
                             if (isinstance(n, int) or isinstance(n, str))]
                if nb_source in ['decimal_and_10_100_1000_for_divi',
                                 'decimal_and_10_100_1000_for_multi']:
                    # __
                    q.options['10_100_1000'] = True
            self.questions_list += [default_question(q.type,
                                                     q.options,
                                                     numbers_to_use=nb_to_use
                                                     )]

        shared.number_of_the_question = 0
