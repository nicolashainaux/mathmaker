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

import os
from operator import itemgetter

from mathmaker.lib import sheet
from mathmaker import settings


def _gather_old_style_sheets_info():
    """Returns a list of {'theme': ..., 'subtheme': ..., 'name': ...}"""
    infos = []
    for s in sheet.AVAILABLE:
        # s in actually the complete name
        theme, subtheme = '', ''
        if s.startswith('algebra'):
            theme = 'algebra'
        elif s.startswith('equation'):
            theme = 'algebra'
            subtheme = 'equations'
        elif s.startswith('fraction'):
            theme = 'numeric calculation'
            subtheme = 'fractions'
        elif 'pythagorean' in s:
            theme = 'geometry'
            subtheme = 'right triangle'
        infos.append({'theme': theme, 'subtheme': subtheme, 'name': s})
    return infos


def _gather_xml_sheets_info():
    """Returns a list of {'theme': ..., 'subtheme': ..., 'name': ...}"""
    infos = []
    for d in os.listdir(settings.frameworksdir):
        theme_dir = settings.frameworksdir + d
        if os.path.isdir(theme_dir):
            for subdir in os.listdir(theme_dir):
                subtheme_dir = theme_dir + '/' + subdir
                if os.path.isdir(subtheme_dir):
                    for filename in os.listdir(subtheme_dir):
                        abspath_f = subtheme_dir + '/' + '/' + filename
                        if os.path.isfile(abspath_f):
                            name, extension = os.path.splitext(filename)
                            if extension == '.xml':
                                infos.append({'theme': d, 'subtheme': subdir,
                                              'name': name})
    return infos


def _hfill(word, total_length, charfill=' '):
    """
    Add spaces after word to get to the given total length.
    """
    return word + charfill * (total_length - len(word))


def list_all_sheets():
    """
    Creates the list of all available mathmaker's sheets.

    The list is displayed as a tabular.

    :return: The list as str
    """
    all_sheets_info = _gather_old_style_sheets_info()
    all_sheets_info += _gather_xml_sheets_info()

    len_t, len_s, len_n = 0, 0, 0
    for s in all_sheets_info:
        len_t = max({len_t, len(s['theme'])})
        len_s = max({len_s, len(s['subtheme'])})
        len_n = max({len_n, len(s['name'])})

    ruler_t = '-' * len_t + '--|'
    ruler_s = '-' * len_s + '--|'
    ruler_n = '-' * len_n + '--'

    header = _hfill('Theme', len(ruler_t) - 1) + '|' \
        + _hfill(' Subtheme', len(ruler_s) - 1) + '|' \
        + _hfill(' Directive name', len(ruler_n) - 1) + '\n' \
        + ruler_t + ruler_s + ruler_n + '\n'

    sheets_list = ''
    for s in sorted(all_sheets_info,
                    key=itemgetter('theme', 'subtheme', 'name')):
        # __
        sheets_list += _hfill(s['theme'], len(ruler_t) - 1) + '|' \
            + _hfill(' ' + s['subtheme'], len(ruler_s) - 1) + '|' \
            + _hfill(' ' + s['name'], len(ruler_n) - 1) \
            + '\n'

    return header + sheets_list
