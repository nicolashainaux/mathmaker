# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
from lib import *
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

SEPARATOR_TOKEN = ":"


# --------------------------------------------------------------------------
##
#   @brief Gets the questions' kinds from the given file.
def get_q_kinds_from_file(file_name):
    try:
        f = open(file_name, mode = 'r')
    except NameError:
        raise error.UnreachableData("the file named : " + str(file_name))

    result = []
    # At the end, result should contain a list of questions' kinds.
    # Each line of the file matches one question's kind and will be turned into:
    # [ <q_kind>, <q_subkind>, nb_of_q]
    # with <q_kind> as a set (see Q_MentalCalculation.AVAILABLE_Q_KIND_VALUES)
    # <q_subkind> as a str (see Q_MentalCalculation.AVAILABLE_Q_KIND_VALUES)
    # and nb_of_q as an int
    # For instance, the line:
    # multiplication direct : table_2-9 : 4
    # will be transformed into:
    # [frozenset(('multiplication', 'direct')), 'table_2-9', 4]

    x_kind = 'tabular'

    for line in f:
        if line == 'slideshow\n':
            x_kind = 'slideshow'
        elif line == 'tabular\n':
            pass
        elif line[0] == '#':
            pass
        else:
            # this will get the <q_kind> set:
            qk = frozenset(shlex.split(line[0:line.find(':')]))
            # this will get the <q_subkind> str:
            qs = line[line.find(':')+1:line.rfind(':')].strip()
            # this will get the number at the end
            qn = int(line[line.rfind(':')+1:len(line)])

            result += [[qk, qs, qn]]

    return (x_kind, result)

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
    #   @return One instance of exercise.Model
    def __init__(self, embedded_machine, x_kind='default_nothing', **options):
        self.derived = True
        mc_mm_file = options['filename'] if 'filename' in options \
                                         else default.MC_MM_FILE

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

        # Creation of the list of questions organized by type of nb :
        q_dict = {}

        # In q_list, each element is like this:
        # [frozenset(('multiplication', 'direct')), 'table_2-9', 4]
        # [q[0],                                    q[1],        q[2]]
        for q in q_list:
            if not q[1] in q_dict:
                q_dict[q[1]] = []

            for n in range[q[2]]:
                q_dict[q[1]].append(q[0])

        # Now, generate the prioritary numbers (not implemented yet)

        # Then, generate all other numbers
        for q_type in list(q_dict.keys()):



        # OTHER EXERCISES



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
                                     [12, 4],
                                     content,
                                     borders='all',
                                     center='yes',
                                     center_vertically='yes')

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
