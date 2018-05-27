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

from abc import ABCMeta, abstractmethod

from mathmakerlib import required
from mathmakerlib.calculus import is_integer

from mathmaker.lib import shared

MIN_ROW_HEIGHT = 0.8  # this is for mental calculation exercises


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Structure
# @brief Mother class of all exercises objects. Not instanciable.
# This class suggests two default methods which are also in the exercise.Model
# class: write_text and write_answer. In a new exercise, they can either be
# kept untouched (then it would be wise to delete them from the new exercise)
# or rewritten.
class X_Structure(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                 X_LAYOUT_UNIT, number_of_questions=6, **options):
        self.questions_list = list()

        # OPTIONS -------------------------------------------------------------
        # It is necessary to define an options field to pass the
        # possibly modified value to the child class
        self.options = options

        x_subkind = 'default'
        if 'x_subkind' in options:
            x_subkind = options['x_subkind']
            # let's remove this option from the options
            # since we re-use it recursively
            temp_options = dict()
            for key in options:
                if key != 'x_subkind':
                    temp_options[key] = options[key]
            self.options = temp_options

        self.x_kind = x_kind
        self.x_subkind = x_subkind

        # Start number
        self.start_number = 0
        if 'start_number' in options:
            if not is_integer(options['start_number']):
                raise TypeError('Got: ' + str(type(options['start_number']))
                                + ' instead of an integer')
            if not (options['start_number'] >= 1):
                raise ValueError(str(options['start_number'])
                                 + 'should be >= 1')

            self.start_number = options['start_number']

        # Number of questions
        if (not isinstance(number_of_questions, int)
            and number_of_questions >= 1):
            # __
            raise ValueError('The number_of_questions keyword argument should '
                             'be an int and greater than 6.')
        self.q_nb = number_of_questions

        self.layout = options.get('layout', 'default')
        self.x_layout_unit = X_LAYOUT_UNIT

        if 'user_defined' in X_LAYOUTS:
            self.x_layout = X_LAYOUTS['user_defined']
        elif (self.x_kind, self.x_subkind) in X_LAYOUTS:
            self.x_layout = X_LAYOUTS[(self.x_kind, self.x_subkind)]
        else:
            self.x_layout = X_LAYOUTS[self.layout]

        self.x_id = options.get('id', 'generic')
        x_spacing = options.get('spacing', '')
        if x_spacing == 'newline':
            self.x_spacing = {'exc': shared.machine.write_new_line(),
                              'ans': shared.machine.write_new_line()}
        elif x_spacing == 'newline_twice':
            self.x_spacing = {'exc': shared.machine.write_new_line()
                              + shared.machine.write_new_line(),
                              'ans': shared.machine.write_new_line()
                              + shared.machine.write_new_line()}
        elif x_spacing == '':
            # do not remove otherwise you'll get empty addvspace instead
            self.x_spacing = {'exc': '', 'ans': ''}
        elif x_spacing == 'jump to next page':
            self.x_spacing = \
                {'exc': shared.machine.write_jump_to_next_page(),
                 'ans': shared.machine.write_jump_to_next_page()}
        else:
            self.x_spacing = \
                {'exc': shared.machine.addvspace(height=x_spacing),
                 'ans': shared.machine.addvspace(height=x_spacing)}

        # The slideshow option (for MentalCalculation sheets)
        self.slideshow = options.get('slideshow', False)

        # END OF OPTIONS ------------------------------------------------------

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = shared.machine
        result = ""

        layout = self.x_layout[ex_or_answers]

        if self.text[ex_or_answers] != "":
            result += self.text[ex_or_answers]
            result += M.addvspace(height='10.0pt')

        q_n = 0

        for k in range(int(len(layout) // 2)):
            if layout[2 * k] is None:
                how_many = layout[2 * k + 1]
                if layout[2 * k + 1] in ['all_left', 'all']:
                    how_many = len(self.questions_list) - q_n
                for i in range(how_many):
                    result += self.questions_list[q_n]\
                        .to_str(ex_or_answers)
                    if ex_or_answers == 'ans' and i < how_many - 1:
                        result += M.addvspace(height='20.0pt')
                    q_n += 1

            elif (layout[2 * k] == 'jump'
                  and layout[2 * k + 1] == 'next_page'):
                result += M.write_jump_to_next_page()

            else:
                nb_of_cols = len(layout[2 * k]) - 1
                col_widths = layout[2 * k][1:]
                nb_of_lines = layout[2 * k][0]
                undefined_nb_of_lines = False
                if nb_of_lines == '?':
                    undefined_nb_of_lines = True
                    if layout[2 * k + 1] == 'all':
                        nb_of_q_per_row = nb_of_cols
                    else:
                        nb_of_q_per_row = sum(layout[2 * k + 1][j]
                                              for j in range(nb_of_cols))
                    nb_of_lines = \
                        len(self.questions_list) // nb_of_q_per_row \
                        + (0
                           if not len(self.questions_list)
                           % nb_of_q_per_row
                           else 1)
                content = []
                for i in range(int(nb_of_lines)):
                    for j in range(nb_of_cols):
                        if layout[2 * k + 1] == 'all':
                            nb_of_q_in_this_cell = 1
                        else:
                            K = 0 if undefined_nb_of_lines else i
                            nb_of_q_in_this_cell = \
                                layout[2 * k + 1][K * nb_of_cols + j]
                        cell_content = ""
                        for n in range(nb_of_q_in_this_cell):
                            empty_cell = False
                            if q_n >= len(self.questions_list):
                                cell_content += " "
                                empty_cell = True
                            else:
                                cell_content += \
                                    self.questions_list[q_n].\
                                    to_str(ex_or_answers)
                            if ex_or_answers == 'ans' and not empty_cell:
                                vspace = '' \
                                    if len(cell_content) <= 25 \
                                    else cell_content[-25:]
                                newpage = '' \
                                    if len(cell_content) <= 9 \
                                    else cell_content[-9:]
                                cell_content += M.write_new_line(
                                    check=cell_content[-2:],
                                    check2=vspace,
                                    check3=newpage)
                            q_n += 1
                        content += [cell_content]

                options = {'unit': self.x_layout_unit}
                result += M.write_layout((nb_of_lines, nb_of_cols),
                                         col_widths,
                                         content,
                                         **options)
                if (self.x_kind,
                    self.x_subkind) == ('bypass', 'any_simple_expandable'):
                    result += '\n' + r'\FloatBarrier' + '\n'
                    required.package['placeins'] = True

        return result + self.x_spacing[ex_or_answers]
