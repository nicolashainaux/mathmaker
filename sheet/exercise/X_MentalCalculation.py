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
    # [{'multiplication', 'direct'}, 'table_2-9', 4]

    for line in f:
        # this will get the <q_kind> set:
        qk = set(shlex.split(line[0:line.find(':')]))
        # this will get the <q_subkind> str:
        qs = line[line.find(':')+1:line.rfind(':')].strip()
        # this will get the number at the end
        qn = int(line[line.rfind(':')+1:len(line)])

        result += [[qk, qs, qn]]

    return result

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

        # HERE: get the list of questions' kinds with get_q_kinds_from_file()
        # check if the sum of qn is not more than an arbitrary max limit
        # defined at the beginning of the file (40)
        # then write the correct loop to append the questions to
        # self.questions_list, each question should be added qn times,
        # the order of questions should be randomized and the 'table_2-9'|
        # 'table_11'|'table_15'etc.'s "gauge" should be managed here too
        # also, self.q_nb should be set here

        for i in range(self.q_nb):
            self.questions_list.append(                                   \
                         default_question(self.machine,
                                    q_kind=self.x_subkind,
                                    expression_number=i+self.start_number,
                                    **options)
                                          )





        # OTHER EXERCISES



        # END OF THE ZONE TO REWRITE ------------------------------------------





    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = self.machine
        result = ""

        if self.slideshow:


        # default tabular option:
        else:
            q = [self.questions_list[i].to_str('exc') for i in range(self.q_nb)]
            a = [self.questions_list[i].to_str('ans') for i in range(self.q_nb)]\
                if ex_or_answers == 'ans' else [" " for i in range(self.q_nb)]

            content = [item for pair in zip(q, a) for item in pair]

            result += M.write_layout((self.nb_q, 2),
                                     [14, 5],
                                     content,
                                     borders='all')

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
