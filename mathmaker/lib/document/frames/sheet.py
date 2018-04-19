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

import copy
import random
import warnings

from mathmakerlib.LaTeX import KNOWN_AMSSYMB_SYMBOLS, KNOWN_TEXTCOMP_SYMBOLS
from mathmakerlib.LaTeX import KNOWN_AMSMATH_SYMBOLS

from mathmaker.lib import shared
from mathmaker.lib.constants import SLIDE_CONTENT_SEP
from mathmaker.lib.tools import rotate
from mathmaker.lib.tools.frameworks import load_sheet, read_layout
from mathmaker.lib.tools.frameworks import build_exercises_list
from mathmaker.lib.document.frames import Exercise

DEFAULT_SHEET_LAYOUT = {'type': 'default', 'unit': 'cm',
                        'font_size_offset': '0',
                        'wordings': '', 'answers': ''}


class Sheet(object):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.Generic
    def __init__(self, theme, subtheme, sheet_name, **options):
        from mathmaker.lib.tools.xml import get_sheet_config
        from mathmaker.lib.tools.xml import get_exercises_list
        # from mathmaker.lib.tools.frameworks import load_sheet
        filename = options.get('filename', None)
        self.preset = 'default'
        # default presets
        presets = {'default':
                   {'write_ex_titles': True,
                    'header': '',
                    'title': '',
                    'subtitle': '',
                    'text': '',
                    'answers_title': _('Answers')},
                   'mental calculation':
                   {'write_ex_titles': False,
                    'header': '',
                    'title': '',
                    'subtitle': '',
                    'text': '',
                    'answers_title': _('Answers')},
                   'mental calculation slideshow':
                   {'write_ex_titles': False,
                    'header': '',
                    'title': _('Ready,{sep}Steady,{sep}Go!')
                    .format(sep=SLIDE_CONTENT_SEP),
                    'subtitle': '',
                    'text': '',
                    'answers_title': _('Answers!')}}

        if filename is None:
            data = load_sheet(theme, subtheme, sheet_name)
            self.preset = data.get('preset', 'default')
            shared.enable_js_form = (options.get('enable_js_form', False)
                                     and self.preset == 'mental calculation')
            header = data.get('header', presets[self.preset]['header'])
            title = data.get('title', presets[self.preset]['title'])
            subtitle = data.get('subtitle', presets[self.preset]['subtitle'])
            text = data.get('text', presets[self.preset]['text'])
            answers_title = data.get('answers_title',
                                     presets[self.preset]['answers_title'])
            layout_data = copy.deepcopy(DEFAULT_SHEET_LAYOUT)
            if self.preset == 'mental calculation':
                layout_data['font_size_offset'] = '-1'
            loaded_layout_data = data.get('layout', layout_data)
            if self.preset == 'mental calculation slideshow':
                layout_data['type'] = 'slideshow'
            if not isinstance(loaded_layout_data, list):
                loaded_layout_data = [loaded_layout_data]
            for d in loaded_layout_data:
                layout_data.update(d)
            self.layout_type = layout_data['type']
            if (self.preset == 'mental calculation slideshow'
                and self.layout_type != 'slideshow'):
                self.layout_type = 'slideshow'
                warnings.warn('For mental calculation slideshows, the '
                              'layout type cannot be redefined to another '
                              'value than \'slideshow\'.')
            self.sheet_layout_unit = layout_data['unit']
            font_size_offset = layout_data['font_size_offset']
            sheet_layout = read_layout(layout_data)
            try:
                font_size_offset = int(font_size_offset)
            except ValueError:
                raise ValueError('YAML file format error: expected an integer'
                                 'as font_size_offset value, got {} instead.'
                                 .format(str(type(font_size_offset))))
        else:
            (header,
             title,
             subtitle,
             text,
             answers_title,
             self.layout_type,
             font_size_offset,
             self.sheet_layout_unit,
             sheet_layout,
             self.preset) = get_sheet_config(filename)

        self.write_ex_titles = presets[self.preset].get('write_ex_titles')
        self.exercises_list = list()
        shared.machine.set_font_size_offset(font_size_offset)

        self.write_texts_twice = False

        if 'write_texts_twice' in options and options['write_texts_twice']:
            self.write_texts_twice = True

        # Some tests on sheet_layout before using it ;
        # but it's a bit complicated to write a complete set of tests on it ;
        # e.g. if the user doesn't use the same number of exercises in the
        # 'exc' key as in 'ans' key (which would be stupid) this
        # won't be checked here and so it won't work.
        if type(sheet_layout) != dict:
            raise TypeError('Got: ' + str(type(type(sheet_layout)))
                            + ' instead of a dict')

        # if len(sheet_layout) != 4:
        #     raise ValueError('SHEET_LAYOUT should have four keys but '
        #                      'it has ' + str(len(sheet_layout)) + ' keys')

        for k in ['exc', 'ans']:
            if k not in sheet_layout:
                raise ValueError('SHEET_LAYOUT should have a key '
                                 + k + ' but it has no such key')

            if type(sheet_layout[k]) != list:
                raise ValueError('SHEET_LAYOUT[' + k + '] should be'
                                 + ' a list, but it is '
                                 + str(type(sheet_layout[k])))

            if len(sheet_layout[k]) % 2:
                raise ValueError('SHEET_LAYOUT[' + k + '] should have'
                                 + ' an even number of elements but it has '
                                 + str(len(sheet_layout[k]))
                                 + ' elements')

            for i in range(int(len(sheet_layout[k]) // 2)):
                if (not (sheet_layout[k][2 * i] is None
                    or type(sheet_layout[k][2 * i]) == list
                    or sheet_layout[k][2 * i] == 'jump')):
                    # __
                    raise ValueError('SHEET_LAYOUT[' + k + ']['
                                     + str(2 * i) + '] should be '
                                     'either a list '
                                     'or None or "jump", but it is a '
                                     + str(type(sheet_layout[k][2 * i])))
                elif sheet_layout[k][2 * i] is None:
                    if (not (type(sheet_layout[k][2 * i + 1]) == int
                        or sheet_layout[k][2 * i + 1]
                        in ['all', 'all_left', 'jump'])):
                        # __
                        raise ValueError(
                            'SHEET_LAYOUT[' + k + ']['
                            + str(2 * i + 1) + '] should be an '
                            + 'int since it follows the None'
                            + 'keyword, but it is '
                            + str(type(sheet_layout[k][2 * i + 1])))

                elif sheet_layout[k][2 * i] == 'jump':
                    if not sheet_layout[k][2 * i + 1] == 'next_page':
                        raise ValueError(
                            'SHEET_LAYOUT[' + k + ']['
                            + str(2 * i + 1) + '] should be: '
                            + 'next_page since it follows '
                            + 'the jump keyword, but it is '
                            + str(type(sheet_layout[k][2 * i + 1])))

                elif type(sheet_layout[k][2 * i]) == list:
                    if not type(sheet_layout[k][2 * i + 1]) == tuple:
                        raise ValueError(
                            'SHEET_LAYOUT[' + k + ']['
                            + str(2 * i + 1) + '] should be a tuple, '
                            'but it is '
                            + str(type(sheet_layout[k][2 * i + 1])))

                    if (not len(sheet_layout[k][2 * i + 1])
                        == (len(sheet_layout[k][2 * i]) - 1)
                        * sheet_layout[k][2 * i][0]):
                        # __
                        raise ValueError(
                            'SHEET_LAYOUT[' + k + ']['
                            + str(2 * i + 1) + '] should have '
                            + ' as many elements as the '
                            + 'number of cols described in '
                            + 'SHEET_LAYOUT[' + k + ']['
                            + str(2 * i) + '], but found '
                            + str(len(sheet_layout[k][2 * i + 1]))
                            + ' instead of '
                            + str(len(sheet_layout[k][2 * i]) - 1))
                else:
                    raise ValueError(
                        'SHEET_LAYOUT[' + k + ']['
                        + str(2 * i) + '] is not of any '
                        + ' of the expected types or '
                        + 'values, it is instead: '
                        + str(len(sheet_layout[k][2 * i])))

        self.sheet_layout = sheet_layout

        self.header = _(header) if header != "" else ""
        self.title = _(title) if title != "" else ""
        self.subtitle = _(subtitle) if subtitle != "" else ""
        self.text = _(text) if text != "" else ""
        self.answers_title = _(answers_title) if answers_title != "" else ""

        self.shift = options.get('shift', False)

        if filename is None:
            for e_data in build_exercises_list(data):
                if self.preset != 'default' and 'preset' not in e_data:
                    if self.preset == 'mental calculation slideshow':
                        e_preset = 'mental calculation'
                    else:
                        e_preset = self.preset
                    e_data.update({'preset': e_preset})
                    if self.preset == 'mental calculation slideshow':
                        e_data.update({'layout_variant': 'slideshow'})
                exc = Exercise(data=e_data)
                self.exercises_list.append(exc)
                if self.shift:
                    excbis = copy.deepcopy(exc)
                    offset = random.choice([i - 9
                                            for i in range(19)
                                            if abs(i - 9) >= 5])
                    excbis.questions_list = rotate(excbis.questions_list,
                                                   offset)
                    self.exercises_list.append(excbis)
        else:
            for ex in get_exercises_list(filename):
                ex_kwargs = ex[2]
                if self.preset != 'default':
                    ex_kwargs.update({'preset': self.preset})
                self.exercises_list.append(Exercise(q_list=ex[0],
                                                    x_layout=ex[1][1],
                                                    x_config=ex[1][0],
                                                    **ex_kwargs))

    #   @brief Writes the whole sheet's content to the output.
    def __str__(self):
        result = ''
        if self.layout_type in ['default', 'equations', 'slideshow']:
            result += shared.machine.write_document_begins(
                variant=self.layout_type)
            result += self.sheet_header_to_str()
            result += self.sheet_title_to_str(variant=self.layout_type)
            result += self.sheet_text_to_str()
            result += self.texts_to_str('exc', 0)
            if self.layout_type != 'slideshow':
                result += shared.machine.write_jump_to_next_page()
            result += self.answers_title_to_str(
                variant=self.layout_type)
            result += self.texts_to_str('ans', 0)
            result += shared.machine.write_document_ends()
            pkg = []
            if any([s in result for s in KNOWN_AMSSYMB_SYMBOLS]):
                pkg.append('amssymb')
            if any([s in result for s in KNOWN_AMSMATH_SYMBOLS]):
                pkg.append('amsmath')
            if any([s in result for s in KNOWN_TEXTCOMP_SYMBOLS]):
                pkg.append('textcomp')
            result = shared.machine.write_preamble(variant=self.layout_type,
                                                   required_pkg=pkg)\
                + result

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Return as str exercises' or answers'texts
    def texts_to_str(self, ex_or_answers, n_of_first_ex):
        M = shared.machine

        result = ''

        if self.layout_type == 'slideshow':
            result += self.exercises_list[0].to_str(ex_or_answers)
            return result

        result += M.reset_exercises_counter()
        result += M.write_set_font_size_to('large')
        layout = self.sheet_layout[ex_or_answers]

        ex_n = n_of_first_ex

        for k in range(int(len(layout) // 2)):
            if layout[2 * k] is None:
                how_many = layout[2 * k + 1]

                if layout[2 * k + 1] in ['all_left', 'all']:
                    how_many = len(self.exercises_list) - ex_n
                    if (self.layout_type in ['short_test', 'mini_test']
                        and ex_n < len(self.exercises_list) // 2):
                        # __
                        how_many = len(self.exercises_list) // 2 - ex_n
                    # elif self.layout_type == 'mini_test':
                    #    if ex_n < len(self.exercises_list) / 4:
                    #        how_many = len(self.exercises_list) / 4 - ex_n
                    #    elif ex_n < len(self.exercises_list) / 2:
                    #        how_many = len(self.exercises_list) / 2 - ex_n
                    #    elif ex_n < 3*len(self.exercises_list) / 4:
                    #        how_many = 3*len(self.exercises_list) / 4 - ex_n

                for i in range(how_many):
                    if self.shift and i != 0:
                        result += shared.machine.write_jump_to_next_page()
                        if ex_or_answers == 'exc':
                            result += self.sheet_title_to_str(
                                variant=self.layout_type)
                        else:
                            result += self.answers_title_to_str()
                            result += \
                                shared.machine.write_set_font_size_to(
                                    'large')
                    if self.write_ex_titles:
                        result += M.write_exercise_number()
                    result += self.exercises_list[ex_n].to_str(ex_or_answers)
                    if (self.layout_type == 'default'
                        and ex_or_answers == 'ans'):
                        if i < how_many - 1:
                            result += M.addvspace(height='29.0pt')
                    else:
                        vspace = '' if len(result) <= 25 else result[-25:]
                        newpage = '' if len(result) <= 9 else result[-9:]
                        result += M.write_new_line(check=result[-2:],
                                                   check2=vspace,
                                                   check3=newpage)
                    # if not (ex_or_answers == 'ans' \
                    #    and self.layout_type == 'equations'):
                    # __
                    #    result += M.write_new_line()
                    ex_n += 1

            elif layout[2 * k] == 'jump' and layout[2 * k + 1] == 'next_page':
                result += M.write_jump_to_next_page()

            else:
                nb_of_lines = layout[2 * k][0]
                nb_of_cols = len(layout[2 * k]) - 1
                col_widths = layout[2 * k][1:]
                content = []
                for i in range(nb_of_lines):
                    for j in range(nb_of_cols):
                        nb_of_ex_in_this_cell = \
                            layout[2 * k + 1][i * nb_of_cols + j]
                        cell_content = ""
                        for n in range(nb_of_ex_in_this_cell):
                            if self.write_ex_titles:
                                cell_content += M.write_exercise_number()
                            cell_content += \
                                self.exercises_list[ex_n].to_str(ex_or_answers)
                            ex_n += 1
                        content += [cell_content]

                result += M.write_layout((nb_of_lines, nb_of_cols),
                                         col_widths,
                                         content,
                                         unit=self.sheet_layout_unit)
                if ex_n < len(self.exercises_list):
                    result += M.write_new_line()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output the header of the sheet to be generated
    #   This header is written in a large size. A new line follow it.
    #   It's useful to write headers for test sheets, for example.
    def sheet_header_to_str(self):
        result = ""
        if self.header != "":
            result += shared.machine.write_set_font_size_to('large')
            result += self.header
            result += shared.machine.write_new_line()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output the title of the sheet to be generated
    def sheet_title_to_str(self, variant='default'):
        result = ''
        if variant == 'slideshow' and self.title != '':
            result += shared.machine.write_frame(self.title,
                                                 uncovered=True,
                                                 duration=0.75)
        else:
            result += shared.machine.write_set_font_size_to('large')
            if shared.enable_js_form:
                result += r'\begin{Form}' + '\n'
            result += shared.machine.write(self.title, emphasize='bold')
            if shared.enable_js_form:
                result += r"""\hfill
\TextField[name=mark,width=3cm,height=0.2cm,value=Score :,
           format={var f = this.getField('mark');
                   f.strokeColor = ['T'];
                   f.fillColor = ['T'];
                   f.textFont = 'Ubuntu'},
           width=10em]{}"""
            if self.subtitle != '':
                result += shared.machine.write_new_line()
                result += shared.machine.write_set_font_size_to('normal')
                result += shared.machine.write(self.subtitle, emphasize='bold')
            result += shared.machine.write_new_line_twice()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output the sheet's text
    def sheet_text_to_str(self):
        result = ""
        if self.text != "":
            result += shared.machine.write(self.text)
            result += shared.machine.write_new_line_twice()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output title of the answers' sheet to be generated
    def answers_title_to_str(self, variant='default'):
        result = ''
        if variant == 'slideshow' and self.answers_title != '':
            result += shared.machine.write_frame(self.answers_title)
        else:
            result += shared.machine.write_set_font_size_to('Large')
            result += shared.machine.write(self.answers_title,
                                           emphasize='bold')
            result += shared.machine.write_new_line_twice()

        return result
