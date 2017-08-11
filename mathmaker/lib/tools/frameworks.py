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

# TODO: add yaml schema validation (per json?)
import os
import json
import copy
from glob import glob
from collections import OrderedDict
from operator import itemgetter
# # from abc import ABCMeta, abstractmethod
#
# import yaml
#
from mathmaker import settings
from mathmaker.lib.constants import DEFAULT_LAYOUT
from mathmaker.lib.tools import parse_layout_descriptor


def read_index():
    from mathmaker import settings
    with open(settings.index_path) as f:
        return json.load(f)


def build_index():
    from mathmaker import settings
    import yaml
    # Below snippet from https://stackoverflow.com/a/21048064/3926735
    # to load roadmap.yaml using OrderedDict instead of dict
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)
    index = dict()
    themes_dirs = [x
                   for x in os.listdir(settings.frameworksdir)
                   if os.path.isdir(settings.frameworksdir + x)]
    for theme in themes_dirs:
        folder_path = os.path.join(settings.frameworksdir, theme)
        folder_files = glob(folder_path + '/*.yaml')
        for folder_path in folder_files:
            subtheme = os.path.splitext(os.path.basename(folder_path))[0]
            with open(folder_path) as f:
                folder = OrderedDict(yaml.load(f))
            for sheet_name in folder:
                directive = '_'.join([subtheme, sheet_name])
                index[directive] = (theme, subtheme, sheet_name)
    with open(settings.index_path, 'w') as f:
        json.dump(index, f, indent=4)


def frameworks_info():
    """Returns a list of {'theme': ..., 'subtheme': ..., 'name': ...}"""
    infos = []
    index = read_index()
    for directive in index:
        infos.append({'theme': index[directive][0],
                      'subtheme': index[directive][1],
                      'name': directive})
    return infos


def _gather_old_style_sheets_info():
    """Returns a list of {'theme': ..., 'subtheme': ..., 'name': ...}"""
    from mathmaker.lib import old_style_sheet
    infos = []
    for s in old_style_sheet.AVAILABLE:
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
    from mathmaker import settings
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
    all_sheets_info += frameworks_info()

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


def load_sheet(theme, subtheme, sheet_name):
    """
    Retrieve sheet data from yaml file.

    :param theme: the theme where to find the sheet
    :type theme: str
    :param subtheme: the subtheme where to find the sheet
    :type subtheme: str
    :param sheet_name: the name of the sheet
    :type sheet_name: str
    :rtype: OrderedDict
    """
    from ruamel import yaml
    # from ruamel.yaml import YAML
    # yaml = YAML(typ='safe')

    theme_dir = os.path.join(settings.frameworksdir, theme)
    subtheme_file = os.path.join(settings.frameworksdir, theme,
                                 subtheme + '.yaml')
    if os.path.isdir(theme_dir):
        if os.path.isfile(subtheme_file):
            with open(subtheme_file) as file_path:
                file_data = yaml.round_trip_load(file_path)
                if sheet_name in file_data:
                    return file_data[sheet_name]
                else:
                    raise ValueError('No sheet of this name ({}) in the '
                                     'provided theme and subtheme ({}, {}).'
                                     .format(sheet_name, theme, subtheme))
        else:
            raise IOError('Could not find the provided subtheme ({}) in the '
                          'provided theme ({}).'.format(subtheme, theme))
    else:
        raise IOError('Could not find the provided theme ({}) among the '
                      'frameworks.'.format(theme))


def parse_attr_string(attr_string):
    """
    Turn an attribute string into a dictionary.


    For instance, this string:  'rowxcol=?×2,  print=3 3, spacing='
    will be turned into        {'rowxcol': '?×2',
                                'print': '3 3',
                                'spacing': ''}

    this one:
    'source=singleint_2to100;;intpairs_2to9, variant=2,3,6,7, required=true, '
    into:    {'source': 'singleint_2to100;;intpairs_2to9',
              'variant': '2,3,6,7',
              'required': 'true'}

    :param attr_string: the attributes formatted string
    :type attr_string: str
    :rtype: dict
    """
    attr_list = attr_string.strip(', ').split(sep=', ')
    return {k: v
            for couple in attr_list
            for (k, v) in [couple.strip().split(sep='=')]}


def split_attr_in_pages(key, attr_string):
    """
    Split attr_string and expand key for each new page found in attr_string.

    For instance, with
    key = 'wordings' and attr_string = 'rowxcol=?×2, print=3 3, spacing=',
    will return [{'wordings': 'rowxcol=?×2, print=3 3, spacing='}]

    while with
    key = 'answers'
    and attr_string = 'print=2, spacing=jump to next page, print=1'
    will return [{'answers': 'print=2, spacing=jump to next page'},
                 {'answers': 'print=1'}]

    In this second case, a dictionary wouldn't have been enough to keep the
    two different values of 'print' (the second one would have erased the
    first one) nor would it have kept the order.

    :param key: the key to expand
    :type key: str
    :param attr_string: the attributes formatted string
    :type attr_string: str
    :rtype: dict
    """
    pages = attr_string.strip(', ').split(sep='spacing=jump to next page')
    pages = [p.strip(', ') for p in pages]
    pages = [p + ', spacing=jump to next page' for p in pages[:-1]] \
        + [pages[-1]]
    return [{key: p} for p in pages]


def load_layout(data):
    """
    Create the layout dictionary from the raw data.

    :param data: the dictionary loaded from YAML file
    :type data: dict
    :rtype: dict
    """
    layout = copy.deepcopy(DEFAULT_LAYOUT)
    keep_default_w, keep_default_a = True, True
    parts = []
    for part in ['wordings', 'answers']:
        if part in data:
            parts += split_attr_in_pages(part, data[part])
    for chunk in parts:
        if 'wordings' in chunk:
            part = 'wordings'
        elif 'answers' in chunk:
            part = 'answers'
        attributes = parse_attr_string(chunk[part])
        s = None
        if 'spacing' in attributes:
            # if it is not, it's already set to 'undefined', by default
            s = attributes.get('spacing')
            if s != 'jump to next page':
                if part == 'wordings':
                    layout['spacing_w'] = s
                if part == 'answers':
                    layout['spacing_a'] = s
        # part is either wordings or answers
        rowxcol = attributes.get('rowxcol', 'none')
        distri = attributes.get('print', 'auto')
        if rowxcol == 'none':
            if distri == 'auto':
                distri = 'all'
            else:
                try:
                    distri = int(distri)
                except ValueError:
                    raise ValueError('XMLFileFormatError: a print '
                                     'attribute cannot be turned into int.')
            if not (s == 'jump to next page'
                    and 'rowxcol' not in attributes
                    and 'print' not in attributes):
                if part == 'wordings':
                    if keep_default_w:
                        layout['exc'] = [None, distri]
                        keep_default_w = False
                    else:
                        layout['exc'] += [None, distri]
                else:
                    if keep_default_a:
                        layout['ans'] = [None, distri]
                        keep_default_a = False
                    else:
                        layout['ans'] += [None, distri]
        else:
            nrow, ncol = parse_layout_descriptor(rowxcol, sep=['×', 'x'],
                                                 special_row_chars=['?'])
            colwidths = attributes.get('colwidths', 'auto')
            if colwidths == 'auto':
                colwidths = [int(18 // ncol) for _ in range(ncol)]
            else:
                colwidths = [int(n) for n in colwidths.split(sep=' ')]
                if not len(colwidths) == ncol:
                    raise ValueError(
                        'XMLFileFormatError: in a <layout>, the number of'
                        'columns '
                        'widths does not match the number of cols in '
                        'the rowxcol attribute.')
            if part == 'wordings':
                if keep_default_w:
                    layout['exc'] = [[nrow, ] + colwidths]
                    keep_default_w = False
                else:
                    layout['exc'].append([nrow, ] + colwidths)
            else:
                if keep_default_a:
                    layout['ans'] = [[nrow, ] + colwidths]
                    keep_default_a = False
                else:
                    layout['ans'].append([nrow, ] + colwidths)
            if distri == 'auto':
                distri = ' '.join(['1' for i in range(ncol * nrow)])
            distri = distri.replace(',', ' ').replace(';', ' ')
            distri = tuple(int(n) for n in distri.split())
            if part == 'wordings':
                layout['exc'].append(distri)
            else:
                layout['ans'].append(distri)
        if 'spacing' in attributes and s == 'jump to next page':
            if part == 'wordings':
                if keep_default_w:
                    layout['exc'] = ['jump', 'next_page']
                    keep_default_w = False
                else:
                    layout['exc'] += ['jump', 'next_page']
            if part == 'answers':
                if keep_default_a:
                    layout['ans'] = ['jump', 'next_page']
                    keep_default_a = False
                else:
                    layout['ans'] += ['jump', 'next_page']
    return layout
