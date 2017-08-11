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
"""Various auxiliary functions."""

import os
import json
import copy
import warnings
import random
import re
import subprocess
from glob import glob
from decimal import Decimal, ROUND_DOWN
from tempfile import TemporaryFile
from operator import itemgetter
from collections import OrderedDict
import polib

from mathmaker.lib.constants import DEFAULT_LAYOUT


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


def retrieve_fonts(fonts_list_file='mathmaker/data/fonts_list.txt',
                   datadir='mathmaker/data',
                   force=False) -> tuple:
    """
    Store in a file the list of the fonts available for lualatex.
    """
    if force:
        return []
    with TemporaryFile() as tmp_file:
        p = subprocess.Popen('luaotfload-tool --list "*"',
                             shell=True,
                             stdout=tmp_file)
        p.wait()
        tmp_file.seek(0)
        with open(fonts_list_file, mode='wt') as f:
            for line in tmp_file.readlines():
                if not line.startswith(b'luaotfload') and line[:-1]:
                    f.write(line.decode('utf-8').lower())
    return [(datadir, [fonts_list_file])]


def _retrieve_po_file_content(language, po_filename):
    from mathmaker import settings
    po = polib.pofile(settings.localedir
                      + settings.language
                      + "/LC_MESSAGES/"
                      + po_filename
                      + ".po")
    return [entry.msgstr for entry in po if entry.msgstr != ""]


def po_file_get_list_of(what, language, arg):
    what_map = {"words": "w" + str(arg) + "l",
                "names": str(arg) + "_names"}
    output = _retrieve_po_file_content(language, what_map[what])
    if len(output) < 20:
        output.append(_retrieve_po_file_content('en', what_map[what]))
    return output


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


def _gather_yaml_sheets_info():
    """Returns a list of {'theme': ..., 'subtheme': ..., 'name': ...}"""
    infos = []
    index = read_index()
    for directive in index:
        infos.append({'theme': index[directive][0],
                      'subtheme': index[directive][1],
                      'name': directive})
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
    all_sheets_info += _gather_yaml_sheets_info()

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


def is_number(n):
    """Check if n is a number."""
    return type(n) in [float, int, Decimal]


def is_integer(n):
    """Check if number n is an integer."""
    if type(n) is int:
        return True
    elif type(n) is float:
        return n.is_integer()
    elif type(n) is Decimal:
        return n % 1 == 0
    else:
        raise TypeError('Expected a number, either float, int or Decimal,'
                        'got {} instead.'.format(str(type(n))))


def is_natural(n):
    """Check if number n is a natural number."""
    return is_integer(n) and n >= 0


class ext_dict(dict):
    """A dict with more methods."""

    def recursive_update(self, d2):
        """
        Update self with d2 key/values, recursively update nested dicts.

        :Example:

        >>> d = ext_dict({'a': 1, 'b': {'a': 7, 'c': 10}})
        >>> d.recursive_update({'a': 24, 'd': 13, 'b': {'c': 100}})
        >>> print(d == {'a': 24, 'd': 13, 'b': {'a': 7, 'c': 100}})
        True
        """
        nested1 = {key: ext_dict(val)
                   for key, val in iter(self.items())
                   if isinstance(val, dict)}
        other1 = {key: val
                  for key, val in iter(self.items())
                  if not isinstance(val, dict)}
        nested2 = {key: val
                   for key, val in iter(d2.items())
                   if isinstance(val, dict)}
        other2 = {key: val
                  for key, val in iter(d2.items())
                  if not isinstance(val, dict)}
        other1.update(other2)
        for key in nested1:
            if key in nested2:
                nested1[key].recursive_update(nested2[key])
        other1.update(nested1)
        self.update(other1)

    def flat(self, sep='.'):
        """
        Return a recursively flattened dict.

        If the dictionary contains nested dictionaries, this function
        will return a one-level ("flat") dictionary.

        :Example:

        >>> d = ext_dict({'a': {'a1': 3, 'a2': {'z': 5}}, 'b': 'data'})
        >>> d.flat() == {'a.a1': 3, 'a.a2.z': 5, 'b': 'data'}
        True
        """
        output = {}
        for key in self:
            if isinstance(self[key], dict):
                ud = ext_dict(self[key]).flat()
                for k in ud:
                    output.update({str(key) + sep + str(k): ud[k]})
            else:
                output.update({key: self[key]})
        return output


def rotate(l, n):
    """Rotate list l of n places, to the right if n > 0; else to the left."""
    return l[-n:] + l[:-n]


def check_unique_letters_words(words_list, n):
    """
    Check if each word of the list contains exactly n letters, all unique.
    """
    for w in words_list:
        if len(w) != n:
            raise ValueError('Expected words of length {}, but {} contains '
                             '{} letters.'.format(str(n), w, str(len(w))))
        if len(w) != len(set(w)):
            raise ValueError('{} contains duplicate letters, but it '
                             'shouldn\'t.'
                             .format(w))
    return True


def parse_layout_descriptor(d, sep=None, special_row_chars=None,
                            min_row=0, min_col=0):
    """
    Parse a "layout" string, e.g. '3×4'. Return number of rows, number of cols.

    :param d: the "layout" string
    :type d: str
    :param sep: the separator's list. Default to '×'
    :type sep: None or str or a list of str
    :param special_row_chars: a list of special characters allowed instead of
                              natural numbers. Defaults to []
    :type special_row_chars: None or list
    :param min_row: a minimal value that the number of rows must respect. It is
                    not checked is nrow is a special char
    :type min_row: positive int
    :param min_col: a minimal value that the number of columns must respect
    :type min_col: positive int
    :rtype: tuple
    """
    if not type(d) is str:
        raise TypeError('The layout descriptor must be str')
    if sep is None:
        sep = '×'
    if type(sep) is str:
        sep = [sep]
    if type(sep) is list:
        if any([type(s) is not str for s in sep]):
            raise TypeError('All items of the sep list must be str')
    else:
        raise TypeError('sep must be a str or a list')
    if special_row_chars is None:
        special_row_chars = []
    if type(special_row_chars) is list:
        if any([type(c) is not str for c in special_row_chars]):
            raise TypeError('All items of the special_row_chars list must be '
                            'str')
    else:
        raise TypeError('special_row_char must be a list')
    if type(min_row) is not int or type(min_col) is not int:
        raise TypeError('min_row and min_col must both be int')
    if min_row < 0 or min_col < 0:
        raise TypeError('min_row and min_col must both be positive')
    for s in sep:
        if s in d:
            nrow_ncol = d.split(sep=s)
            nrow_ncol = [x for x in nrow_ncol if x != '']
            if not len(nrow_ncol) == 2:
                raise ValueError('The layout format must be a string like '
                                 '\'row×col\', where × is your delimiter. '
                                 'Cannot find a row and a col in \''
                                 + d + '\' with '
                                 + s + ' as delimiter ')
            break
    else:  # no break
        raise ValueError('Cannot find a row and a col in \'' + d + '\' with '
                         'any of the str from this list as delimiter: '
                         + str(sep))
    nrow, ncol = nrow_ncol
    if nrow not in special_row_chars:
        try:
            nrow = int(nrow)
        except ValueError:
            raise ValueError('Number of rows: \'{}\' cannot be turned into int'
                             .format(nrow))
    try:
        ncol = int(ncol)
    except ValueError:
        raise ValueError('Number of cols: \'{}\' cannot be turned into int'
                         .format(ncol))
    if type(nrow) is int:
        if nrow < min_row:
            raise ValueError('nrow must be greater than ' + str(min_row))
    if ncol < min_col:
        raise ValueError('ncol must be greater than ' + str(min_col))
    return nrow, ncol


def generate_header_comment(document_format, comment_symbol="% "):
    """Return the header comment for output text files."""
    from mathmaker import (__software_name__, __release__,
                           __licence_info__, __contact__)
    from mathmaker import __licence__, __url_info__, __url__, __copyright__
    hc = comment_symbol \
        + _("{document_format} document generated by {software_ref}")\
        .format(document_format=document_format,
                software_ref=__software_name__ + " " + __release__) + "\n"
    hc += comment_symbol + _(__licence_info__)\
        .format(software_ref=__software_name__,
                software_license=__licence__) + "\n"
    hc += comment_symbol + _(__url_info__)\
        .format(software_website=__url__) + "\n"
    hc += comment_symbol + "{copyright} {contact}\n\n"\
        .format(copyright=__copyright__, contact=__contact__)
    return hc


def fix_math_style2_fontsize(text, mathsize='\Large',
                             normalsize='\\normalsize'):
    """
    Wrap any $ LaTex math expression $ in another fontsize.

    :param mathsize: the size the math expressions will be (same as LaTeX
                     fontsizes, including \ at start)
    :type mathsize: str

    :param normalsize: the size the rest of the text will be (same as LaTeX
                       fontsizes, including \ at start)
    :type normalsize: str
    :rtype: str
    """
    p = re.compile(r'(\$[^\$]+\$)')
    remember = []
    for match in p.split(text):
        if (match != '' and not match.startswith('$')
            and not match.endswith('$') and match not in remember):
            text = text.replace(match, normalsize + '{' + match + '}')
            remember.append(match)
    text = p.sub(mathsize + r'{\1}', text)
    return text


def correct_normalize_results(d):
    """Transform the xE+n results in decimal form (ex. 1E+1 -> 10)"""
    if not isinstance(d, Decimal):
        raise TypeError('Expected a Decimal, got a '
                        + str(type(d)) + 'instead')
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def round_deci(d, precision, **options):
    """Correctly round a Decimal"""
    if not isinstance(d, Decimal):
        raise TypeError('Expected a Decimal, got a '
                        + str(type(d)) + 'instead')

    return correct_normalize_results(d.quantize(precision, **options))


def digits_nb(n):
    """
    Return the number of significant digits of an int or decimal.Decimal.

    :param n: the number to test
    :type n: int or decimal.Decimal
    :rtype: int
    """
    if is_integer(abs(n)):
        return 0
    n = Decimal(abs(n))
    n = n.quantize(Decimal(1)) if n == n.to_integral() else n.normalize()
    temp = len(str((n - round_deci(n, Decimal(1), rounding=ROUND_DOWN)))) - 2
    return temp if temp >= 0 else 0


def is_power_of_10(n):
    """
    Check if n is a power of ten.

    :param n: the number to test
    :type n: int or decimal.Decimal
    :rtype: boolean
    """
    if not is_number(n) or type(n) is float:
        raise TypeError('Argument n must be either int or decimal.Decimal.')
    n = Decimal(abs(n))
    if Decimal(10) <= n:
        return is_power_of_10(n / 10)
    if Decimal(1) < n < Decimal(10):
        return False
    elif n == Decimal(1):
        return True
    elif Decimal('0.1') < n < Decimal(1):
        return False
    elif 0 < n <= Decimal('0.1'):
        return is_power_of_10(n * 10)
    elif n == 0:
        return False


def move_digits_to(N, from_nb=None):
    """
    Turn N into decimal instead of all decimals found in the from_nb list.

    Each decimal found in the numbers' list will be recursively replaced by
    10 times itself (until it is no decimal anymore) while in the same time
    N will be divided by 10.

    This is useful for the case division by a decimal is unwanted.

    :param N: the number who will be divided by 10 instead of the others
    :type N: any number (int, Decimal, float though they're not advised)
    :param from_nb: an iterable containing the numbers that must be integers
    :type from_nb: a list (of numbers)
    :rtype: a list (of numbers)
    """
    if type(from_nb) is not list:
        raise TypeError('A list of numbers must be given as argument '
                        '\'numbers\'.')
    if not is_number(N):
        raise TypeError('The first argument must be a number.')
    N = Decimal(str(N))
    if all([is_integer(n) for n in from_nb]):
        return [N, ] + [n for n in from_nb]
    numbers_copy = copy.deepcopy(from_nb)
    for i, n in enumerate(from_nb):
        if not is_number(n):
            raise TypeError('Each variable of the list must be a number.')
        if not is_integer(n):
            numbers_copy[i] = n * 10
            return move_digits_to(N / 10, from_nb=numbers_copy)
    return [N, ] + [n for n in from_nb]


def remove_digits_from(number, to=None):
    """
    Turn a number of the to list into a decimal, instead of number.

    In some cases this is not possible (for instance when all numbers of the
    to list are multiples of 10), then a ValueError is raised.

    :param number: the number that must be turned into integer
    :type number: decimal.Decimal
    :param to: the list of numbers where to find an integer that must be
               turned into a decimal
    :type to: list
    :rtype: a list (of numbers)
    """
    if type(number) is not Decimal:
        raise TypeError('The first argument must be a Decimal number.')
    if is_integer(number):
        raise TypeError('The first argument must be a decimal number.')
    if type(to) is not list:
        raise TypeError('Argument to: must be a list.')
    n = Decimal(digits_nb(number))
    try:
        i = to.index(next(x for x in to
                          if not is_integer(x / 10 ** n)))
    except StopIteration:
        raise ValueError('None of the numbers of to can be turned into '
                         'decimal.')
    to[i] = to[i] / 10 ** n
    return [number * 10 ** n, ] + [x for x in to]


def fix_digits(n1, *n2):
    """Ensure digits from n1 are removed. Change n2 if necessary."""
    n2 = list(n2)
    try:
        n1, *n2 = remove_digits_from(n1, to=n2)
    except ValueError:
        j = random.choice([j for j in range(len(n2))])
        n2[j] += random.choice([i for i in range(-4, 5) if i != 0])
        n1, *n2 = remove_digits_from(n1, to=n2)
    return (n1, *n2)


def split_nb(n, operation='sum', dig=0):
    """
    Split n as a sum, like a + b = n; or a difference, like a - b = n

    By default, a and b have as many digits as n does. The 'dig' keyword tells
    how many extra digits must have a and b (compared to n).
    For instance, if n=Decimal('2.5'), operation='sum', dig=1, then
    n will be split into 2-digits numbers, like 2.14 + 2.36.

    :param n: the number to split
    :type n: a number (preferably an int or a Decimal, but can be a float too)
    :param operation: must be 'sum', 'difference', '+' or '-'
    :type operation: str
    :param dig: extra depth level to use
    :type dig: int
    :rtype: tuple (of numbers)
    """
    if operation not in ['sum', 'difference', '+', '-']:
        raise ValueError('Argument "operation" should be either \'sum\' or '
                         '\'difference\'.')
    n_depth = digits_nb(n)
    depth = dig + digits_nb(n)
    if operation in ['sum', '+']:
        if is_power_of_10(n) and abs(n) <= 1 and dig == 0:
            # This case is impossible: write 1 as a sum of two natural
            # numbers bigger than 1, or 0.1 as a sum of two positive decimals
            # having 1 digit either, etc. so we arbitrarily replace n by
            # a random number between 2 and 9
            warnings.warn('mathmaker is asked something impossible (split {}'
                          'as a sum of two numbers having as many digits)'
                          .format(n))
            n = random.choice([i + 2 for i in range(7)])
            n = n * (10 ** (Decimal(- n_depth)))
        amplitude = n
    elif operation in ['difference', '-']:
        amplitude = max(10 ** (n_depth), n)
    start, end = 0, int((amplitude) * 10 ** depth - 1)
    if start > end:
        start, end = end + 1, -1
    # default: all numbers, including integers
    seq = [(Decimal(i) + 1) / Decimal(10) ** Decimal(depth)
           for i in range(start, end)]
    # then if decimals are wanted, we remove the results that do not match
    # the wanted "depth" (if depth == 2, we remove 0.4 for instance)
    if depth >= 1:
            seq = [n for n in seq
                   if not is_integer(n * (10 ** (depth - 1)))]
    if operation in ['sum', '+']:
        a = random.choice(seq)
        b = n - a
    elif operation in ['difference', '-']:
        b = random.choice(seq)
        a = n + b
    return (a, b)
