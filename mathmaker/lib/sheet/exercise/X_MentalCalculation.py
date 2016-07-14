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
AVAILABLE_X_KIND_VALUES = {'tabular': 'default', 'slideshow': 'default'}

MAX_NB_OF_QUESTIONS = 40

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']
              }
             }

MIN_ROW_HEIGHT = 0.8

SWAPPABLE_QKINDS_QSUBKINDS = {("rectangle", "area"),
                              ("rectangle", "perimeter"),
                              ("square", "area"),
                              ("square", "perimeter")}

KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE = {
    ('divi', 'direct', 'area_width_length_rectangle'):
    ('rectangle', 'length_or_width', 'from_area')}

to_unpack = copy.deepcopy(question.SUBKINDS_TO_UNPACK)
Q_info = namedtuple('Q_info', 'type,kind,subkind,nb_source,options')


# --------------------------------------------------------------------------
##
#   @brief Will reorganize the raw questions lists into a dictionary
#   @param  q_list          The questions' list
#   @return (q_dict, q_nb)  The questions' dictionary + the total number of
#                           questions
def build_q_dict(q_list):
    # In q_list, each element is like this:
    # [{'kind':'multi', 'subkind':'direct', 'nb':'int'}, 'table_2_9', 4]
    # [q[0], q[1], q[2]]
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
    # { 'multi_direct':   [('table_2_9', 'multi', 'direct', {'nb':'int'}),
    #                       ('table_2_9', 'multi', 'direct', {'nb':'int'})],
    #   'multi_reversed': [('table_2_9', 'multi', 'reversed', {options})],
    #   'divi_direct':    [('table_2_9', 'divi', 'direct', {options})],
    #   'multi_hole':     [('table_2_9', 'multi', 'hole', {options})],
    #   'q_id':           [('table_15', 'kind', 'subkind', {options})],
    #   'q_id:            [('table_25', 'kind', 'subkind', {options})],
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


# --------------------------------------------------------------------------
##
#   @brief  Determine the
#   @param  q_i     The Q_info object
def get_nb_source_from_question_info(q_i):
    tag_to_unpack = nb_source = q_i.nb_source
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
    return nb_source


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_MentalCalculation
# @brief Creates a tabular with n questions and answers
class X_MentalCalculation(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Options detailed below:
    #          - start_number=<integer>
    #                         (should be >= 1)
    #          - number_of_questions=<integer>
    #            /!\ only useful if you use x_kind and not preformatted
    #                         (should be >= 1)
    #          - x_kind=<string>
    #                         ...
    #                         ...
    #          - preformatted=<string>
    #            /!\ preformatted is useless with short_test
    #            /!\ number_of_questions is useless with preformatted
    #            /!\ if you use it with the x_kind option, ensure there's a
    #                preformatted possibility with this option
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - short_test=bool
    #            /!\ the x_kind option above can't be used along this option
    #            use subtype if you need to make different short_test exercises
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - subtype=<string>
    #                         ...
    #                         ...
    #   @todo Complete the description of the possible options !
    #   @return One instance of exercise.X_MentalCalculation
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        from mathmaker.lib.tools.xml_sheet import (get_q_kinds_from,
                                                   get_xml_sheets_paths)
        XML_SHEETS = get_xml_sheets_paths()
        mc_mm_file = options.get('filename',
                                 XML_SHEETS['mental_calculation_default'])

        (x_kind, q_list) = get_q_kinds_from(
            mc_mm_file,
            sw_k_s=SWAPPABLE_QKINDS_QSUBKINDS,
            k_s_ctxt_tr=KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE)

        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------

        # should be default_question = question.Something
        default_question = question.Q_MentalCalculation

        # TEXTS OF THE EXERCISE
        self.text = {'exc': "", 'ans': ""}

        # From q_list, we build a dictionary and then a complete questions'
        # list:
        q_dict, self.q_nb = build_q_dict(q_list)
        for key in q_dict:
            random.shuffle(q_dict[key])
        mixed_q_list = build_mixed_q_list(q_dict)
        mixed_q_list = increase_alternation(mixed_q_list, 'type')
        mixed_q_list.reverse()
        mixed_q_list = increase_alternation(mixed_q_list, 'type')

        # mixed_q_list is organized like this:
        # [ ('type', 'kind', 'subkind', 'nb_source', 'options'),
        #   ('multi_direct', 'multi', 'direct', 'table_2_9', {'nb':}),
        #   ('multi_reversed', 'multi', 'reversed', 'table_2_9', {'nb':}),
        #   ('q_id', 'q_', 'id', 'table_15', {'nb':}),
        #   ('multi_hole', 'multi', 'hole', 'table_2_9', {'nb':}),
        #   ('multi_direct', 'multi', 'direct', 'table_2_9', {'nb':}),
        #   ('q_id, 'q_', 'id', 'table_25', {'nb':}),
        #   ('divi_direct', divi', 'direct', 'table_2_9', {'nb':}),
        #   etc.
        # ]

        # Now, we generate the numbers & questions, by type of question first
        self.questions_list = []
        last_draw = [0, 0]
        for q in mixed_q_list:
            nb_source = get_nb_source_from_question_info(q)
            nb_to_use = shared.mc_source\
                .next(nb_source,
                      not_in=last_draw,
                      **question.get_modifier(q.type, nb_source))
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

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = shared.machine
        result = ""

        if self.slideshow:
            result += M.write_frame("", frame='start_frame')
            for i in range(self.q_nb):
                result += M.write_frame(
                    self.questions_list[i].to_str('exc'),
                    timing=self.questions_list[i].transduration)

            result += M.write_frame("", frame='middle_frame')

            for i in range(self.q_nb):
                result += M.write_frame(_("Question:")
                                        + self.questions_list[i].to_str('exc')
                                        + _("Answer:")
                                        + self.questions_list[i].to_str('ans'),
                                        timing=0)

        # default tabular option:
        else:
            q = [self.questions_list[i].to_str('exc')
                 for i in range(self.q_nb)]
            a = [self.questions_list[i].to_str('ans')
                 for i in range(self.q_nb)]\
                if ex_or_answers == 'ans' \
                else [self.questions_list[i].to_str('hint')
                      for i in range(self.q_nb)]

            n = [M.write(str(i + 1) + ".", emphasize='bold')
                 for i in range(self.q_nb)]

            content = [elt for triplet in zip(n, q, a) for elt in triplet]

            result += M.write_layout((self.q_nb, 3),
                                     [0.5, 14.25, 3.75],
                                     content,
                                     borders='penultimate',
                                     justify=['left', 'left', 'center'],
                                     center_vertically=True,
                                     min_row_height=MIN_ROW_HEIGHT)

        return result

    # INSTRUCTIONS TO CREATE A NEW EXERCISE -----------------------------------
    # - Indicate its name in the header comment
    #   the one of documentation (@class)
    # - Write the @brief description
    # - Replace the Model class name by the chosen one
    # - In the constructor comment, replace Model with the chosen name
    #   at the @return line
    # - Write the class name of the default_question. You must mention it
    #   because it will be used in the OTHER EXERCISES section.
    # - The different sections to rewrite are:
    #   * TEXTS OF THE EXERCISE:
    #       default text for all exercises of this class
    #   * alternate texts section:
    #       if you want to specify a different text for any particular kind
    #       of exercise
    #   * PREFORMATTED EXERCISES
    #       that's where preformatted exercises are described (the ones that
    #       won't repeat n times the same kind of randomly question)
    #   * OTHER EXERCISES section is meant to all exercises that repeat
    #       the same (maybe randomly chosen among many) kind of question.
    #       shouldn't be rewritten
    # - Finally, if the write_* methods from the exercise.Structure don't
    #   match your needs, copy & modify or rewrite them
