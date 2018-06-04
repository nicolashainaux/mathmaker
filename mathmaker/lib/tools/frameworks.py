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

# TODO: add yaml schema validation (per json?)
import os
import re
import json
import copy
import random
import warnings
from glob import glob
from pathlib import Path
from collections import OrderedDict
from operator import itemgetter

from mathmaker import settings
from mathmaker.lib.constants import DEFAULT_LAYOUT, EQUAL_PRODUCTS
from mathmaker.lib.constants import BOOLEAN
from mathmaker.lib.tools import parse_layout_descriptor

# Characters allowed inside questions, numbers' sources and attributes
# (including =)
_CHARS = r'a-zA-Z0-9_×±;:%\. =|'
_QA_ICHARS = _CHARS + r'{}'
# Separator between attributes (and question's id)
_ATTR_SEP = r','
# All characters forming a complete question or a complete numbers' source.
_QCHARS = _QA_ICHARS + _ATTR_SEP
# Separator between question and number source
_MAIN_SEP = r'\->'
# Characters of a complete line, without number in parentheses:
# "question -> number source"
_LINE = _QCHARS + _MAIN_SEP
_INT = r'\d+'
_FETCH_NB = r'\((' + _INT + r')\)'
# _DECI = r'[\d\.]+'

SIMPLE_QUESTION = re.compile(r'([' + _LINE + r']+\(' + _INT + r'\))')
Q_BLOCKS = re.compile(r'\[(' + _INT + r')\]\[([' + _LINE + r'\n\(\)]+)\]'
                      r'|([' + _LINE + r']+\(' + _INT + r'\))')
MIX_QUESTION = re.compile(
    r'([' + _QA_ICHARS + r']+[,]?)(([' + _QA_ICHARS + r']+'
    r'=[' + _QA_ICHARS + r']+[,]?)*)')
NB_SOURCE = re.compile(r'([' + _QCHARS + r'\-]+)' + _FETCH_NB)
FETCH_NB = re.compile(_FETCH_NB + r'$')
SUB_NB = re.compile(r'([' + _LINE + r']+)' + _FETCH_NB + r'$')
CURLY_BRACES_CONTENT = re.compile(r'{([' + _CHARS + r']+)}')

TESTFILE_TEMPLATE = """# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2018 Nicolas Hainaux <nh.techn@gmail.com>

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


from mathmaker.lib import shared
from mathmaker.lib.document.frames import Sheet


def test_{sheet_name}():
    \"""Check this sheet is generated without any error.\"""
    shared.machine.write_out(str(Sheet('{theme}',
                                       '{subtheme}',
                                       '{sheet_name}')),
                             pdf_output=True)
"""

MENTAL_CALCULATION_TESTFILE_TEMPLATE_ADDENDUM = """

def test_{sheet_name}_embedding_js():
    \"""Check this sheet is generated without any error.\"""
    shared.machine.write_out(str(Sheet('{theme}',
                                       '{subtheme}',
                                       '{sheet_name}',
                                       enable_js_form=True)),
                             pdf_output=True)
"""


def read_index():
    """Read the index of all (YAML) sheets available."""
    from mathmaker import settings
    with open(settings.index_path) as f:
        return json.load(f)


def build_index():
    """Create the index of all (YAML) sheets available."""
    from mathmaker import settings
    from ruamel import yaml
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
                loaded_data = yaml.safe_load(f)
                if loaded_data is not None:
                    folder = OrderedDict(loaded_data)
                for sheet_name in folder:
                    directive = '_'.join([subtheme, sheet_name])
                    index[directive] = (theme, subtheme, sheet_name)
                    # Automatic add possibly missing sheet integration test
                    sheet_test_dir = Path(os.path.join(settings.testsdir,
                                                       'integration',
                                                       theme,
                                                       subtheme))
                    file_name = subtheme + '_' + sheet_name
                    sheet_file = Path(os.path.join(sheet_test_dir,
                                                   'test_{}.py'
                                                   .format(file_name)))
                    if not sheet_file.is_file():
                        sheet_test_dir.mkdir(parents=True, exist_ok=True)
                        template = TESTFILE_TEMPLATE
                        if (theme == 'mental_calculation'
                            and not sheet_name.startswith('W')):
                            template += \
                                MENTAL_CALCULATION_TESTFILE_TEMPLATE_ADDENDUM
                        with open(sheet_file, 'w') as f:
                            f.write(template.format(theme=theme,
                                                    subtheme=subtheme,
                                                    sheet_name=sheet_name))

    with open(settings.index_path, 'w') as f:
        json.dump(index, f, indent=4)
        f.write('\n')


def _frameworks_info():
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
    all_sheets_info += _frameworks_info()

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


def parse_qid(qid):
    """
    Return question's kind and subkind from question's attribute "id".
    """
    if qid.count(' ') != 1:
        raise ValueError('YAML file format error: got "{}", but a question id '
                         'must consist of two parts separated by one space '
                         'character. There cannot be several space '
                         'characters in the id, neither.'.format(qid))
    return qid.split()


class _AttrStr(str):
    """
    Attributes formatted string: a series of attributes represented as a str.

    Each attribute attr and its value val are represented by 'attr=val'.
    All pairs (attr, val) are joined with ', '.
    For instance: 'attr1=val1, attribute 2=value 2, attr3=val3'
    """

    def parse(self):
        """
        Turn an attribute string into a dictionary.

        For instance, this string:  'rowxcol=?×2,  print=3 3, spacing='
        will be turned into        {'rowxcol': '?×2',
                                    'print': '3 3',
                                    'spacing': ''}

        this one:
        'source=singleint_2to100;;intpairs_2to9, variant=2,3,6,7,
         required=true, '
        into:    {'source': 'singleint_2to100;;intpairs_2to9',
                  'variant': '2,3,6,7',
                  'required': 'true'}

        :rtype: dict
        """
        attr_list = self.strip(', ').split(sep=', ')
        if not all(('=' in couple or couple == '') for couple in attr_list):
            warnings.warn('Ignoring malformed attributes\' string '
                          '(missing =, or empty space between two commas) '
                          'in \'{}\'.'.format(self))
        return {k: v
                for couple in attr_list if '=' in couple
                for (k, v) in [couple.strip().split(sep='=')]}

    def split_clever(self, key):
        """
        Split self in pieces to gather (rowxcol, colwidths, print) series.

        Also split on each newpage occurence.

        For instance, with
        key = 'wordings' and self = 'rowxcol=?×2, print=3 3, spacing=',
        will return [{'wordings': 'rowxcol=?×2, print=3 3, spacing='}]

        while with
        key = 'answers'
        and self = 'print=2, newpage=true, print=1'
        will return [{'answers': 'print=2, newpage=true'},
                     {'answers': 'print=1'}]

        In this second case, a dictionary wouldn't have been enough to keep the
        two different values of 'print' (the second one would have erased the
        first one) nor would it have kept the order.

        If self is: 'print=2, rowxcol=?×2, print=3 3'
        will return: [{'answers': 'print=2'},
                      {'answers': 'rowxcol=?×2, print=3 3'}]

        :param key: the key to expand
        :type key: str
        :rtype: list
        """
        if self == '':
            return [{}]
        order = {'rowxcol': 0, 'colwidths': 1, 'print': 2, 'newpage': -1000}
        chunks = self.strip(', ').split(sep=', ')
        result = []
        bit = {}
        last_place = -1
        for c in chunks:
            k, v = c.strip(', ').split(sep='=')
            if k in order and order[k] < last_place:
                if k == 'newpage':
                    if key not in bit:
                        raise ValueError('YAML File Format Error: '
                                         'a layout cannot start with a '
                                         'newpage (at least, not yet).')
                    result.append({key: ', '.join([bit[key], c])})
                    bit = {}
                else:
                    result.append(bit)
                    bit = {key: c}
                last_place = -1
            elif k in order and order[k] == last_place:
                raise ValueError('YAML File Format Error: same keyword cannot '
                                 'show up several times in a row.')
            else:
                # either k is not in order, like 'spacing', or k is in order
                # and order[k] > last_place
                if key in bit:
                    bit = {key: ', '.join([bit[key], c])}
                else:
                    bit = {key: c}
                if k in order:
                    last_place = order[k]
        if bit != {}:
            result.append(bit)
        return result

    def fetch(self, attr):
        """
        Return the value of first attr in self.

        For instance, if a = 'pick' and s = 'attr1=value 1, pick=7, attr3=valZ'
        then we'll get: '7'

        :param attr: the attribute to find
        :type attr: str
        :rtype: str
        """
        chunks = self.split(sep=', ')
        for c in chunks:
            a, v = c.split(sep='=')
            if a.strip() == attr:
                return v.strip(', ')
        raise KeyError('Cannot find the attribute \'{}\' in string \'{}\'.'
                       .format(attr, self))

    def remove(self, attr):
        """
        Return self, without attribute attr in it.

        For instance, if attr = 'pick'
        and self = 'attr1=value 1, pick=7, attr3=valZ'
        then we'll get: 'attr1=value 1, attr3=valZ'

        :param attr: the attribute to remove
        :type attr: str
        :rtype: str
        """
        return _AttrStr(', '.join([c
                                   for c in self.split(sep=', ')
                                   if not c.startswith(attr + '=')]))


def read_layout(data):
    """
    Create the layout dictionary from the raw data.

    :param data: the dictionary loaded from YAML file (might be list of dict)
    :type data: dict or list
    :rtype: dict
    """
    layout = copy.deepcopy(DEFAULT_LAYOUT)
    keep_default_w, keep_default_a = True, True
    if not isinstance(data, list):
        data = [data]
    parts = []
    for data_elt in data:
        for part in ['wordings', 'answers']:
            if part in data_elt and _AttrStr(data_elt[part]) != '':
                parts += _AttrStr(data_elt[part]).split_clever(part)
    for data_elt in data:
        for elt in data_elt:
            if elt not in ['wordings', 'answers']:
                layout.update({elt: data_elt[elt]})
    for chunk in parts:
        if 'wordings' in chunk:
            part = 'wordings'
        elif 'answers' in chunk:
            part = 'answers'
        attributes = _AttrStr(chunk[part]).parse()
        jump = BOOLEAN[attributes.get('newpage', 'false')]()
        s = None
        if 'spacing' in attributes:
            # if it is not, it's already set to 'undefined', by default
            s = attributes.get('spacing')
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
            if not (jump
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
                        'YAML File Format Error: in a layout, the number of'
                        'columns widths does not match the number of cols in '
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
            distri = distri.replace('.', ' ').replace('/', ' ')
            distri = tuple(int(n) for n in distri.split())
            if part == 'wordings':
                layout['exc'].append(distri)
            else:
                layout['ans'].append(distri)
        if jump:
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


def build_exercises_list(data):
    """
    Return the list of exercises from a sheet.

    :param data: the sheet's data, as read from YAML file
    :type data: dict
    :rtype: list
    """
    return [data[x]
            for x in data
            if (type(x) is str and x.startswith('exercise'))]


def _match_qid_sourcenb(q_id: str, source_nb: str, variant: str):
    """
    Tell if the given question's id and source number do match.

    This is used in mix sections only, yet.

    :param q_id: the question's id (kind_subkind)
    :param source_nb: the source of the numbers
    :param variant: the variant of the numbers' source / question, if available
    """
    # TODO:   The 'integer_3_10_decimal_3_10' may be later turned into
    #         'intpairs_3to10' with variant='decimal1', so this condition can
    #         certainly be removed.
    source_nb = source_nb[0]
    if q_id in ['multi_direct', 'area_rectangle', 'multi_hole',
                'rectangle_length_or_width_from_area', 'divi_direct',
                'vocabulary_multi', 'vocabulary_divi']:
        # __
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'decimal_and_10_100_1000',
                    source_nb == 'decimal_and_one_digit',
                    source_nb == 'bypass'])
    elif q_id in ['addi_direct', 'subtr_direct', 'perimeter_rectangle',
                  'rectangle_length_or_width_from_perimeter',
                  'vocabulary_addi', 'vocabulary_subtr']:
        # __
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb.startswith('complements_to_'),
                    source_nb == 'decimal_and_10_100_1000',
                    source_nb == 'integer_3_10_decimal_3_10',
                    source_nb == 'decimals_0_20_1',
                    source_nb == 'bypass'])
    elif q_id.startswith('place_'):
        return any([source_nb == 'digits_places',
                    source_nb == 'fracdigits_places',
                    source_nb == 'bypass'])
    elif q_id in ['perimeter_square', 'area_square']:
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'bypass'])
    elif q_id in ['vocabulary_half', 'vocabulary_double']:
        return any([source_nb.startswith('multiplesof2'),
                    source_nb == 'table_2',
                    source_nb == 'bypass'])
    elif q_id in ['vocabulary_third', 'vocabulary_triple']:
        return any([source_nb.startswith('multiplesof3'),
                    source_nb == 'table_3',
                    source_nb == 'bypass'])
    elif q_id in ['vocabulary_quarter', 'vocabulary_quadruple']:
        return any([source_nb.startswith('multiplesof4'),
                    source_nb == 'table_4',
                    source_nb == 'bypass'])
    elif q_id in ['multi_reversed', 'fraction_of_rectangle']:
        return any([source_nb.startswith('intpairs_'),
                    source_nb == 'table_2',
                    source_nb == 'table_3',
                    source_nb == 'table_4',
                    source_nb == 'bypass'])
    elif q_id == 'order_of_operations':
        # We only check there are two sources
        return len(source_nb.split(sep=';;')) == 2
    elif q_id == 'fraction_of_a_rectangle':
        return any([(source_nb.startswith('intpairs_') and ';;' in source_nb),
                    source_nb.startswith('properfraction'),
                    source_nb == 'bypass'])
    elif q_id == 'fraction_of_a_linesegment':
        return any([source_nb.startswith('properfraction'),
                    source_nb.startswith('simple_fractions'),
                    source_nb.startswith('intpairs'),
                    (len(source_nb.split(sep=';;')) == 2
                     and source_nb.split(sep=';;')[0].startswith('singleint')
                     and source_nb.split(sep=';;')[1].startswith('singleint')),
                    source_nb == 'bypass'])
    else:
        warnings.warn('Could not check if the question\'s type and numbers\'s '
                      'source do match or not: {} and {}'
                      .format(q_id, source_nb))
        return True


# --------------------------------------------------------------------------
##
#   @brief Returns a dictionary to give some special informations needed for
#          certain questions.
def get_q_modifier(q_type, nb_source):
    d = {}
    if (q_type in ['multi_reversed', 'fraction_of_a_rectangle']
        and nb_source.startswith('intpairs')):
        d.update({'lock_equal_products': True,
                  'info_lock': EQUAL_PRODUCTS})
    elif (q_type == 'mini_pb_proportionality'
          and nb_source.startswith('deciinttriplesforprop')):
        d.update({'lock_equal_coeffs': True})
    elif q_type == 'subtr_direct' and nb_source.startswith('intpairs_10'):
        d.update({'diff7atleast': True})
    elif any(['rectangle' in q_type and q_type != 'fraction_of_a_rectangle',
              q_type.startswith('addi_'), q_type.endswith('_addi'),
              q_type.startswith('subtr_'), q_type.endswith('_subtr')]):
        # __
        d.update({'rectangle': True})
    elif 'square' in q_type:
        d.update({'square': True})
    elif (q_type == 'digitplaces_numberof'
          and nb_source.startswith('extdecimals')):
        d.update({'numberof': True})
    return d


def _expand_alternatives(s):
    """
    Return all alternatives, like 'a_{b|c}' will return ['a_b', 'a_c'].

    :param s: the string to parse
    :type s: str
    :rtype: list
    """
    alternatives = []
    if '{' in s and '|' in s and '}' in s:
        content = CURLY_BRACES_CONTENT.findall(s)[0]
        p = '{' + content.replace('|', r'\|') + '}'
        for alt in content.split('|'):
            alternatives += _expand_alternatives(re.sub(p, alt, s))
    else:
        alternatives.append(s)
    return alternatives


def _dissolve_block(block):
    """
    Turn a choice block into simple question attributes' strings.

    For instance, will turn ('2', 'q1 (2)\n q2 (1)\n q3 (1)') into a list of
    two questions taken from q1, q2 and q3.

    :param block: the number of questions to create and the questions' list to
                  pick from
    :type block: tuple (of str)
    :rtype: list
    """
    nb_of_q = int(block[0])
    raw_q_list = SIMPLE_QUESTION.findall(block[1])
    q_list = []
    for i in range(len(raw_q_list)):
        raw_q_list[i] = random.choice(_expand_alternatives(raw_q_list[i]))
    for q in raw_q_list:
        repeat_it = int(FETCH_NB.findall(q)[0])
        new_q = SUB_NB.sub(r'\1(1)', q)
        for i in range(repeat_it):
            q_list.append(new_q)
    try:
        return random.sample(q_list, nb_of_q)
    except ValueError:
        raise ValueError('YAML File Format error: there are more questions '
                         'to create ({}) than available ({}).'
                         .format(nb_of_q, len(q_list)))


def _read_simple_question(s):
    """
    Build the questions' attributes from the raw string read from YAML file.

    For instance, from:
    expand double -> intpairs_2to9;;intpairs_2to9 (5)
    we'll build:
    [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 5]]

    From:
    expand double -> intpairs_2to9;;intpairs_2to9 (3)
    expand double -> intpairs_10to20;;intpairs_2to9 (7)
    as well as from:
    expand double -> intpairs_2to9;;intpairs_2to9 (3)
                  -> intpairs_10to20;;intpairs_2to9 (7)
    we'll build:
    [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 3],
     [{'id': 'expand double'}, ['intpairs_10to20', 'intpairs_2to9'], 7]]

    and from:
    expand double -> intpairs_2to9;;intpairs_2to9 (3)
                  -> intpairs_10to20;;intpairs_2to9 (7)
    expand simple -> intpairs_2to9;;intpairs_2to9 (10)
    we'll build:
    [[{'id': 'expand double'}, ['intpairs_2to9', 'intpairs_2to9'], 3],
     [{'id': 'expand double'}, ['intpairs_10to20', 'intpairs_2to9'], 7],
     [{'id': 'expand simple'}, ['intpairs_2to9', 'intpairs_2to9'], 10]]

    :param s: the raw string read from YAML file.
    :type s: str
    :rtype: list
    """
    result = []
    parsed = Q_BLOCKS.findall(s)
    pairs = []
    for p in parsed:
        if p[0] == '':
            pairs.append(random.choice(_expand_alternatives(p[2])))
        else:  # block
            pairs += _dissolve_block(p[:2])
    if not len(pairs):
        raise ValueError('YAML file format error: the simple questions or \n'
                         'blocks: {}\nare not built correctly.'.format(s))
    pairs = [p.split('->') for p in pairs]
    last_id = last_attr = None
    for p in pairs:
        q_attr = _AttrStr('id=' + p[0]).parse()
        if q_attr['id'] == '':
            if last_id is None:
                raise ValueError('YAML file format error: missing question\'s '
                                 'name.')
            else:
                q_attr['id'] = last_id
                q_attr.update(last_attr)
        else:
            last_id = q_attr['id']
            last_attr = q_attr
        q_attr = {k: q_attr[k].strip() for k in q_attr}
        try:
            parts = NB_SOURCE.match(p[1]).group
        except AttributeError:
            raise ValueError('YAML file format error: incorrect numbers\' '
                             'source:\n{}'.format(p[1]))
        n_attr = _AttrStr('source=' + parts(1)).parse()
        sources = n_attr.pop('source').strip().split(sep=';;')
        q_attr.update(n_attr)
        n_text = parts(2)
        result += [[q_attr, sources, int(n_text)]]
    return result


def _read_mix_question(s):
    """
    Build mix question from the raw string from YAML file.

    For instance, from:
    q id1, attr1=val1, attr2=value 2, q id2, attr1=val1, attr3=val3, pick=3,
    q id3
    we'll build:
    [{'id': 'q id1', 'attr1': 'val1', 'attr2': 'value 2'},
     {'id': 'q id2', 'attr1': 'val1', 'attr3': 'val3'},
     {'id': 'q id2', 'attr1': 'val1', 'attr3': 'val3'},
     {'id': 'q id2', 'attr1': 'val1', 'attr3': 'val3'},
     {'id': 'q id3'}]

    :param s: the raw string read from YAML file.
    :type s: str
    :rtype: list (of dict)
    """
    questions = MIX_QUESTION.findall(s)
    result = []
    for q in questions:
        repeat_it = 1
        q_attributes = _AttrStr(q[1])
        if 'pick' in q_attributes:
            repeat_it = int(q_attributes.fetch('pick'))
            q_attributes = q_attributes.remove('pick')
        for i in range(repeat_it):
            result.append(
                _AttrStr('id=' + q[0].strip() + ' ' + q_attributes.strip())
                .parse())
    return result


def _read_mix_nb(s):
    """
    Build mix numbers' sources from the raw string from YAML file.

    For instance, from:
    'singleint_2to100;;intpairs_2to9, variant=2,3,6,7, required=true (1)'
    we'll build:
    [[['singleint_2to100;;intpairs_2to9'],
      {'source': 'singleint_2to100;;intpairs_2to9',
       'variant': '2,3,6,7',
       'required': 'true'},
      1]]

    From:
    'singleint_2to100;;intpairs_2to9, variant=2,3,6,7, required=true (3)'
    we'll build:
    [[['singleint_2to100;;intpairs_2to9'],
      {'source': 'singleint_2to100;;intpairs_2to9',
       'variant': '2,3,6,7',
       'required': 'true'},
      1],
     [['singleint_2to100;;intpairs_2to9'],
       {'source': 'singleint_2to100;;intpairs_2to9',
        'variant': '2,3,6,7',
        'required': 'true'},
       1],
     [['singleint_2to100;;intpairs_2to9'],
       {'source': 'singleint_2to100;;intpairs_2to9',
        'variant': '2,3,6,7',
        'required': 'true'},
       1]]

    and from:
    'singleint_2to100;;intpairs_2to9, variant=2,3,6,7, required=true (1)
     singleint_3to12;;intpairs_2to9, variant=8-23,100-187, (2)'
    we'll build:
    [[['singleint_2to100;;intpairs_2to9'],
      {'source': 'singleint_2to100;;intpairs_2to9',
       'variant': '2,3,6,7',
       'required': 'true'},
      1],
     [['singleint_2to100;;intpairs_2to9'],
      {'source': 'singleint_3to12;;intpairs_2to9',
       'variant': '8-23,100-187'},
      1],
     [['singleint_2to100;;intpairs_2to9'],
      {'source': 'singleint_3to12;;intpairs_2to9',
       'variant': '8-23,100-187'},
      1]]

    :param s: the raw string read from YAML file.
    :type s: str
    :rtype: list
    """
    result = []
    for nb in NB_SOURCE.findall(s):
        # nb should be, for instance: ('intpairs_2to9, variant=90', '1')
        parsed = _AttrStr('source=' + nb[0].strip()).parse()
        for i in range(int(nb[1])):
            result += [[[parsed['source']],
                        parsed,
                        1]]
    return result


def _read_mix(data):
    """
    Build questions and numbers' sources from the raw strings from YAML file.

    For instance, from:
    {'mix': {'question': 'q id, subvariant=someth',
             'nb': 'singleint_5to20;;intpairs_2to9, variant=0, (1)'}
    }
    we'll build:
    ([{'id': 'q id', 'subvariant': 'someth'}],
     [['singleint_5to20;;intpairs_2to9'],
      {'source': 'singleint_5to20;;intpairs_2to9',
       'variant': '0'},
      1])

    and from:
    {'mix': {'question': 'q id, subvariant=someth, pick=2',
             'nb': 'singleint_5to20;;intpairs_2to9, variant=0, (3)'}
    }
    we'll build:
    ([{'id': 'q id', 'subvariant': 'someth'},
      {'id': 'q id', 'subvariant': 'someth'}],
     [[['singleint_5to20;;intpairs_2to9'],
       {'source': 'singleint_5to20;;intpairs_2to9',
        'variant': '0'},
       1],
       ['singleint_5to20;;intpairs_2to9'],
         {'source': 'singleint_5to20;;intpairs_2to9',
          'variant': '0'},
         1]],
      )

    So far it's not possible to mix questions requiring several sources with
    other questions yet multiple sources questions can be mixed together
    if they are the same type.

    :param data: the raw string read from YAML file.
    :type data: dict
    :rtype: list
    """
    q_temp_list = []
    n_temp_list = []
    if not isinstance(data, list):
        data = [data]
    for entry in data:
        for key in entry:
            if key.startswith('question'):
                q_temp_list += _read_mix_question(entry[key])
            elif key.startswith('nb'):
                n_temp_list += _read_mix_nb(entry[key])
            else:
                raise ValueError('YAML file format error: invalid entry under '
                                 'a mix section: {}.'.format(key))

    # Check and then Mix the questions and numbers retrieved
    if len(q_temp_list) > len(n_temp_list):
        raise ValueError(
            'YAML file format error: incorrect mix section: the number '
            'of sources of numbers (' + str(len(n_temp_list)) + ') '
            'must be at least equal to the number of questions '
            '(' + str(len(q_temp_list)) + ').')

    # TODO: A YAML validation will necessary to ensure all data are correct.

    # So far, we only check if all of the numbers' sources
    # may be attributed to any of the questions, in order
    # to just distribute them all randomly.
    for n in n_temp_list:
        for q in q_temp_list:
            v = n[1].get('variant', q.get('variant', ''))
            if (not _match_qid_sourcenb(q['id'].replace(' ', '_'),
                                        n[0], v)):
                # __
                raise ValueError(
                    'YAML File Format Error: this source: '
                    + str(n[0]) + ' cannot '
                    'be attributed to this question:'
                    ' ' + str(q['id'].replace(' ', '_')))

    random.shuffle(q_temp_list)
    if any(BOOLEAN[n[1].get('required', 'false')]()
           for n in n_temp_list):
        required_n_temp_list = [n for n in n_temp_list
                                if BOOLEAN[n[1].get('required', 'false')]()]
        rest_n_temp_list = [n for n in n_temp_list
                            if not BOOLEAN[n[1].get('required', 'false')]()]
        random.shuffle(required_n_temp_list)
        random.shuffle(rest_n_temp_list)
        n_temp_list = required_n_temp_list + rest_n_temp_list
    else:
        random.shuffle(n_temp_list)

    mix_questions = []
    for (q, n) in zip(q_temp_list, n_temp_list):
        merged_q = copy.deepcopy(q)
        merged_q.update(n[1])
        mix_questions += [[merged_q, n[0], 1]]

    random.shuffle(mix_questions)

    return mix_questions


def build_questions_list(data):
    """
    Return the list of questions from an exercise.

    :param data: the exercise's data, as read from YAML file (extract from
                 the complete sheet's data)
    :type data: dict
    :rtype: list
    """
    questions = []
    # For instance we will get a list of this kind of elements:
    # [{'id': 'multi direct', 'nb': 'int'}, 'table_2_9', 4]
    # [{'id': 'expand_and_reduce double_expansion'},
    #  'table_2_9',
    #  4]
    for entry in data:
        if entry.startswith('question'):
            questions += _read_simple_question(data[entry])
        elif entry.startswith('mix'):
            questions += _read_mix(data[entry])
    return questions


def _get_attributes(data, tag):
    """
    Return the list of "attributes" matching tag. Not recursive.

    :param data: the data read from YAML file
    :type data: dict
    :rtype: list
    """
    result = []
    for key in data:
        if key.startswith(tag):
            attr = {}
            for a in data[key]:
                attr.update(a)
            result.append(attr)
    return result


def get_attributes(filename, tag):
    """
    Gathers the "attributes" of all *filename*'s keys matching *tag*.

    :param filename: The YAML file name.
    :type filename: str
    :param tag: The tag we're looking for.
    :type tag: str
    :rtype: list
    """
    from ruamel import yaml
    with open(filename) as f:
        return _get_attributes(yaml.safe_load(f), tag)
