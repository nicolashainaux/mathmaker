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
"""Various auxiliary functions."""

import os
import sys
import logging
import errno
import re


def load_config(file_tag, settingsdir):
    """
    Will load the values from the yaml config file, named file_tag.yaml.

    The default configuration values are loaded from
    mathmaker/settings/default/*.yaml, then load_config
    will update with values found successively in
    /etc/mathmaker/*.yaml, then in ~/.config/mathmaker/*.yaml,
    finally in mathmaker/settings/dev/*.yaml.
    """
    from ruamel import yaml
    # As one wants to log anything as soon as possible, but at least the
    # default values from ``logging.yaml`` must be read before anything
    # can be logged, the logger is only set and used if the filename is
    # not 'logging.yaml'.
    if file_tag != 'logging':
        mainlogger = logging.getLogger('__main__')
    configuration = ext_dict()
    try:
        with open(os.path.join(settingsdir, 'default/', file_tag + '.yaml'))\
                as file_path:
            # __
            if file_tag != 'logging':
                mainlogger.info('Loading ' + file_tag + '.yaml from '
                                + file_path.name)
            configuration = ext_dict(yaml.safe_load(file_path))
    except IOError:
        if file_tag != 'logging':
            mainlogger.error('FileNotFoundError: No default config file for '
                             + file_tag)
        raise FileNotFoundError(errno.ENOENT,
                                os.strerror(errno.ENOENT),
                                file_tag + '.yaml')
    if file_tag == 'logging' and sys.platform.startswith('freebsd'):
        try:
            with open(os.path.join(settingsdir, 'default/',
                                   file_tag + '_freebsd.yaml')) as file_path:
                # __
                configuration.recursive_update(yaml.safe_load(file_path))
        except IOError:
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    file_tag + '_freebsd.yaml')
    if file_tag == 'user_config' and sys.platform.startswith('win'):
        try:
            with open(os.path.join(settingsdir, 'default/',
                                   file_tag + '_windows.yaml')) as file_path:
                # __
                configuration.recursive_update(yaml.safe_load(file_path))
        except IOError:
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    file_tag + '_windows.yaml')
    for d in ['/etc/mathmaker',
              os.path.join(os.path.expanduser('~'), '.config', 'mathmaker'),
              settingsdir + 'dev']:
        try:
            with open(os.path.join(d, file_tag + '.yaml')) as file_path:
                if file_tag != 'logging':
                    mainlogger.info('Updating config values for ' + file_tag
                                    + ' from ' + file_path.name)
                configuration.recursive_update(yaml.safe_load(file_path))
        except IOError:
            pass
        if file_tag == 'logging' and sys.platform.startswith('freebsd'):
            try:
                with open(os.path.join(d,
                                       file_tag
                                       + '_freebsd.yaml')) as file_path:
                    # __
                    configuration.recursive_update(yaml.safe_load(file_path))
            except IOError:
                pass
        if file_tag == 'user_config' and sys.platform.startswith('win'):
            try:
                with open(os.path.join(d,
                                       file_tag
                                       + '_windows.yaml')) as file_path:
                    # __
                    configuration.recursive_update(yaml.safe_load(file_path))
            except IOError:
                pass
    return configuration


def _retrieve_po_file_content(language, po_filename):
    from mathmaker import settings
    import polib
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


def generate_preamble_comment(document_format, comment_symbol="% "):
    """Return the preamble comment for output text files."""
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
    hc += comment_symbol + "{copyright} {contact}\n"\
        .format(copyright=__copyright__, contact=__contact__)
    return hc


def fix_math_style2_fontsize(text):
    """
    Turn all \\frac to \\dfrac.

    :rtype: str
    """
    r = re.compile(r'(\\frac{)')
    return r.sub(r'\\dfrac{', text)
