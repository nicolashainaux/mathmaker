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

import shlex
import xml.etree.ElementTree as XML_PARSER
from decimal import Decimal
import copy
import random
from collections import deque, namedtuple

import sys

from lib import *
from lib.common import default
import sheet
from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
AVAILABLE_X_KIND_VALUES = \
    {'tabular' : 'default',
     'slideshow' : 'default'
    }

MAX_NB_OF_QUESTIONS = 40

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
X_LAYOUTS = {'default' :
              { 'exc' : [ None,                    'all'
                        ],
                'ans' : [ None,                    'all'
                        ]
              }
            }

MIN_ROW_HEIGHT = 0.5


# --------------------------------------------------------------------------
##
#   @brief Gets the questions' kinds from the given file.
def get_q_kinds_from_file(file_name):

    try:
        xml_config = XML_PARSER.parse(file_name).getroot()
    except FileNotFoundError:
        raise error.UnreachableData("the file named : " + str(file_name))

    questions = []

    # For instance we will get a list of this kind of elements:
    # [ {'kind': 'multi', 'subkind': 'direct', 'nb': 'int'}, 'table_2_9', 4]

    x_kind = 'tabular' # default

    for child in xml_config:
        if child.tag == 'exercise':
            if 'kind' in child.attrib:
                x_kind = child.attrib['kind']
            for subchild in child:
                if subchild.tag == 'question':
                    for elt in subchild:
                        questions += [[subchild.attrib,
                                       elt.attrib['source'], int(elt.text)]]
                elif subchild.tag == 'mix':
                    q_temp_list = []
                    n_temp_list = []
                    for elt in subchild:
                        if elt.tag == 'question':
                            q_temp_list += [elt.attrib]
                        elif elt.tag == 'nb':
                            # We don't check that 'source' is in elt.attrib,
                            # this should have been checked by the xml schema
                            if elt.attrib['source'] \
                                            in question.USER_Q_SUBKIND_VALUES:
                            #___
                                n_temp_list += [[elt.attrib['source'],
                                                 elt.attrib,
                                                 1] \
                                                for i in range(int(elt.text))]
                            else:
                                raise error.XMLFileFormatError(\
                                "Unknown source found in the xml file: " \
                                + elt.attrib['source'])
                        else:
                            raise error.XMLFileFormatError(\
                            "Unknown element found in the xml file: " + elt.tag)

                    if len(q_temp_list) != len(n_temp_list):
                        raise error.XMLFileFormatError(\
                        "Incorrect mix section: the number of sources "\
                        + "of numbers (" + str(len(n_temp_list)) + ") "\
                        + "does not match the number of questions (" \
                        + str(len(q_temp_list)) + ").")

                    # So far, we only check if all of the numbers' sources
                    # may be attributed to any of the questions, in order
                    # to just distribute them all randomly.
                    for n in n_temp_list:
                        for q in q_temp_list:
                            if not n[0] \
            in question.AVAILABLE_Q_KIND_VALUES[q['kind'] + "_" + q['subkind']]:
                            #___
                                raise error.XMLFileFormatError(\
                                "This source: " + str(n[0]) + " cannot be " \
                                + "attributed to this question: " \
                                + str(q['kind'] + "_" + q['subkind']))

                    random.shuffle(q_temp_list)
                    random.shuffle(n_temp_list)

                    for (q,n) in zip(q_temp_list, n_temp_list):
                        q.update(n[1])
                        questions += [[q, n[0], 1]]

    return (x_kind, questions)

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
    #   @param embedded_machine The machine that will be used to write output.
    #   @param **options Options detailed below :
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
    #          - short_test=<string>
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
    def __init__(self, embedded_machine, x_kind='default_nothing', **options):
        self.derived = True
        mc_mm_file = options['filename'] if 'filename' in options \
                                         else sheet.catalog.XML_SHEETS[\
                                                  'mental_calculation_default']

        (x_kind, q_list) = get_q_kinds_from_file(mc_mm_file)

        X_Structure.__init__(self, embedded_machine,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------

        # should be default_question = question.Something
        default_question = question.Q_MentalCalculation

        # TEXTS OF THE EXERCISE
        self.text = {'exc' : "",
                     'ans' : ""
                    }

        # From q_list, we build a dictionary:
        q_dict = {}

        nb_box = { key : question.generate_numbers(key) \
                   for key in question.nb_sources()}
        nb_used = { key : set() \
                    for key in question.nb_sources()}
        last_nb = { key : set() \
                    for key in question.nb_sources()}

        to_unpack = copy.deepcopy(question.SUBKINDS_TO_UNPACK)
        already_unpacked = set()

        self.q_nb = 0

        # In q_list, each element is like this:
        # [{'kind':'multi', 'subkind':'direct', 'nb':'int'}, 'table_2_9', 4]
        # [q[0],                                             q[1],        q[2]]
        for q in q_list:
            self.q_nb += q[2]

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
                        already_unpacked -= copy.deepcopy(\
                                            question.SUBKINDS_TO_UNPACK[subk])
                        to_unpack[subk] = copy.deepcopy(\
                                            question.SUBKINDS_TO_UNPACK[subk])
                        subk_left = to_unpack[subk] - already_unpacked
                    s = list(subk_left)
                    random.shuffle(s)
                    subk = s.pop()
                    already_unpacked |= {subk}

                q_id += subk
                q_options = copy.deepcopy(q[0])
                if not q_id in q_dict:
                    q_dict[q_id] = []
                q_dict[q_id] += [(q[1], q_options['kind'], subk, q_options)]
                del q_options['kind']
                del q_options['subkind']

        # Now, q_dict is organized like this:
        # { 'multi_direct' :   [('table_2_9', 'multi', 'direct', {'nb':'int'}),
        #                       ('table_2_9', 'multi', 'direct', {'nb':'int'})],
        #   'multi_reversed' : [('table_2_9', 'multi', 'reversed', {options})],
        #   'divi_direct' :    [('table_2_9', 'divi', 'direct', {options})],
        #   'multi_hole' :     [('table_2_9', 'multi', 'hole', {options})],
        #   'q_id' :           [('table_15', 'kind', 'subkind', {options})],
        #   'q_id :            [('table_25', 'kind', 'subkind', {options})],
        #   'etc.'
        # }

        # We shuffle the lists a little bit:
        for key in q_dict:
            random.shuffle(q_dict[key])

        # Now we mix the questions types (by id):
        mixed_q_list = []
        #q_id_box = copy.deepcopy(list(q_dict.keys()))
        #q_ids_aside = deque()

        q_info = namedtuple('q_info', 'type,kind,subkind,nb_source,options')

        """for n in range(self.q_nb):
            q_nb_in_q_id_box = sum([len(q_dict[q_id]) for q_id in q_dict])

            w_table = [Decimal(Decimal(len(q_dict[q_id])) \
                               / Decimal(q_nb_in_q_id_box)) \
                       for q_id in q_id_box]

            #dbg
            zipped = zip(q_id_box, w_table)
            sys.stderr.write("\n------------------------------------------")
            for q,w in zipped:
                sys.stderr.write("\n" + str(q) + ": " + str(w))

            q_id = randomly.pop(q_id_box,
                                weighted_table=w_table)

            info = q_dict[q_id].pop(0)

            mixed_q_list += [q_info(q_id, info[1], info[2], info[0], info[3])]

            if len(q_dict[q_id]):
                q_ids_aside.appendleft(q_id)
                if len(q_ids_aside) >= 4 or len(q_id_box) <= 1:
                    q_id_box += [q_ids_aside.pop()]
            else:
                del q_dict[q_id]

            if len(q_id_box) <= 1 and len(q_ids_aside) > 0:
                q_id_box += [q_ids_aside.pop()]"""

        q_id_box = [key for key in q_dict.keys() \
                        for i in range(len(q_dict[key]))]

        random.shuffle(q_id_box)

        for q_id in q_id_box:
            info = q_dict[q_id].pop(0)
            nb_source = info[0]
            translations_to_check = []
            if 'variant' in info[3]:
                translations_to_check += [q_id + "_" + info[3]['variant']]
            if 'context' in info[3]:
                translations_to_check += [q_id + "_" + info[3]['context']]
            for t in translations_to_check:
                if t in question.SOURCES_TO_TRANSLATE \
                    and nb_source in question.SOURCES_TO_TRANSLATE[t]:
                #___
                    nb_source = question.SOURCES_TO_TRANSLATE[t][nb_source]
                    break

            mixed_q_list += [q_info(q_id, info[1], info[2], nb_source, info[3])]

        # Now, mixed_q_list is organized like this:
        # [ ('type',           'kind',      'subkind',  'nb_source', 'options'),
        #   ('multi_direct',   'multi',     'direct',   'table_2_9', {'nb':}),
        #   ('multi_reversed', 'multi',     'reversed', 'table_2_9', {'nb':}),
        #   ('q_id',           'q_',        'id',       'table_15',  {'nb':}),
        #   ('multi_hole',     'multi',     'hole',     'table_2_9', {'nb':}),
        #   ('multi_direct',   'multi',     'direct',   'table_2_9', {'nb':}),
        #   ('q_id,            'q_',        'id',       'table_25',  {'nb':}),
        #   ('divi_direct',    divi',       'direct',   'table_2_9', {'nb':}),
        #   etc.
        # ]

        # Now, we generate the numbers & questions, by type of question first
        self.questions_list = []

        for q in mixed_q_list:
            nb_source = q.nb_source
            if nb_source in question.SOURCES_TO_UNPACK:
                s = ''
                stu = copy.copy(question.SOURCES_TO_UNPACK)
                if nb_source == 'decimal_and_10_100_1000' \
                    or nb_source == 'decimal_and_one_digit':
                    s = stu[nb_source][q.type]
                else:
                    s = stu[nb_source][q.subkind]
                s = list(s)
                random.shuffle(s)
                nb_source = s.pop()

            if len(nb_box[nb_source]) == 0:
                nb_box[nb_source] = question.generate_numbers(nb_source)

            if nb_source == 'rank_word':
                if 'rank_matches_invisible_zero' in q.options \
                    and q.options['rank_matches_invisible_zero'] != ""\
                    and q.options['rank_matches_invisible_zero'] != "False":
                #___
                    if (Decimal("1"),) in nb_box[nb_source]:
                        if len(nb_box[nb_source]) == 1:
                            nb_box[nb_source] = \
                                        question.generate_numbers(nb_source)

                        last_nb[nb_source] |= {Decimal("1")}

            (kept_aside,
             nb_box[nb_source]) = utils.put_aside(last_nb[nb_source],
                                                  nb_box[nb_source]) \
                if not nb_source in question.PART_OF_ANOTHER_SOURCE \
                else (set(), nb_box[nb_source])

            nb_to_use = None
            if nb_source in question.PART_OF_ANOTHER_SOURCE:
                second_source = question.PART_OF_ANOTHER_SOURCE[nb_source]
                remaining = set(nb_box[nb_source] & nb_box[second_source])
                reversed_elements = {(j, i) for (i, j) in nb_box[second_source]}
                extra_elements = set(nb_box[nb_source] & reversed_elements)
                remaining |= extra_elements
                if not len(remaining):
                    nb_box[nb_source] = question.generate_numbers(nb_source)
                    remaining = set(nb_box[nb_source])
                remaining_shuffled = list(remaining)
                random.shuffle(remaining_shuffled)
                nb_to_use = remaining_shuffled.pop()
                nb_box[nb_source].remove(nb_to_use)
                nb_box[second_source].discard(nb_to_use)

            else:
                #if len(nb_box[nb_source]) == 0:
                #    nb_box[nb_source] = question.generate_numbers(nb_source)
                nb_box_shuffled = list(nb_box[nb_source])
                random.shuffle(nb_box_shuffled)
                nb_to_use = nb_box_shuffled.pop()
                nb_box[nb_source].remove(nb_to_use)

            if nb_source == 'decimal_and_10_100_1000_for_divi' \
                or nb_source == 'decimal_and_10_100_1000_for_multi':
            #___
                q.options['10_100_1000'] = True

            nb_box[nb_source] |= kept_aside
            self.questions_list += [default_question(embedded_machine,
                                                     q.type,
                                                     q.options,
                                                     numbers_to_use=nb_to_use
                                                     )]

            last_nb[nb_source] = set()
            if nb_source == 'table_2_9':
                last_nb[nb_source] |= {nb_to_use[0], nb_to_use[1]}
            elif nb_source == 'int_irreducible_frac' \
                 or nb_source == 'rank_word'\
                 or nb_source == 'decimal_and_10_100_1000_for_divi'\
                 or nb_source == 'decimal_and_10_100_1000_for_multi':
                last_nb[nb_source] |= {nb_to_use[0]}
            else:
                last_nb[nb_source] |= {nb_to_use[1]}


        # END OF THE ZONE TO REWRITE ------------------------------------------





    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = self.machine
        result = ""

        if self.slideshow:
            result += M.write_frame("", frame='start_frame')
            for i in range(self.q_nb):
                result += M.write_frame(self.questions_list[i].to_str('exc'),
                                    timing=self.questions_list[i].transduration)

            result += M.write_frame("", frame='middle_frame')

            for i in range(self.q_nb):
                result += M.write_frame(_("Question:") \
                                        + self.questions_list[i].to_str('exc')\
                                        + _("Answer:") \
                                        + self.questions_list[i].to_str('ans'),
                                        timing=0)

        # default tabular option:
        else:
            q = [self.questions_list[i].to_str('exc') for i in range(self.q_nb)]
            a = [self.questions_list[i].to_str('ans') for i in range(self.q_nb)]\
                if ex_or_answers == 'ans' else [" " for i in range(self.q_nb)]

            content = [elt for pair in zip(q, a) for elt in pair]

            result += M.write_layout((self.q_nb, 2),
                                     [14, 4],
                                     content,
                                     borders='all',
                                     center='yes',
                                     center_vertically='yes',
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
    # - The different sections to rewrite are :
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
