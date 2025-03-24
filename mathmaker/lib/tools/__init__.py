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
import json
import logging
import errno
import re

from mathmakerlib.calculus import Number, Fraction


def load_config(file_tag, settingsdir, fmt='.yaml'):
    """
    Will load the values from the yaml config file, named file_tag.yaml.
    It's possible to read from json files too, instead.

    The default configuration values are loaded from
    mathmaker/settings/default/*.yaml, then load_config
    will update with values found successively in
    /etc/mathmaker/*.yaml, then in ~/.config/mathmaker/*.yaml,
    finally in mathmaker/settings/dev/*.yaml.
    """
    if fmt == '.yaml':
        from ruamel.yaml import YAML
        loader = YAML(typ='safe', pure=True)
    elif fmt == '.json':
        loader = json
    # As one wants to log anything as soon as possible, but at least the
    # default values from ``logging.yaml`` must be read before anything
    # can be logged, the logger is only set and used if the filename is
    # not 'logging.yaml'.
    if file_tag != 'logging':
        mainlogger = logging.getLogger('__main__')
    configuration = ext_dict()
    try:
        with open(os.path.join(settingsdir, 'default/', file_tag + fmt))\
                as file_path:
            # __
            if file_tag != 'logging':
                mainlogger.info('Loading ' + file_tag + f'{fmt} from '
                                + file_path.name)
            configuration = ext_dict(loader.load(file_path))
    except IOError:
        if file_tag != 'logging':
            mainlogger.error('FileNotFoundError: No default config file for '
                             + file_tag)
        raise FileNotFoundError(errno.ENOENT,
                                os.strerror(errno.ENOENT),
                                file_tag + fmt)
    if file_tag == 'logging' and sys.platform.startswith('freebsd'):
        try:
            with open(os.path.join(settingsdir, 'default/',
                                   file_tag + f'_freebsd{fmt}')) as file_path:
                # __
                configuration.recursive_update(loader.load(file_path))
        except IOError:
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    file_tag + f'_freebsd{fmt}')
    if file_tag == 'user_config' and sys.platform.startswith('win'):
        try:
            with open(os.path.join(settingsdir, 'default/',
                                   file_tag + f'_windows{fmt}')) as file_path:
                # __
                configuration.recursive_update(loader.load(file_path))
        except IOError:
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    file_tag + f'_windows{fmt}')
    for d in ['/etc/mathmaker',
              os.path.join(os.path.expanduser('~'), '.config', 'mathmaker'),
              settingsdir + 'dev']:
        try:
            with open(os.path.join(d, file_tag + fmt)) as file_path:
                if file_tag != 'logging':
                    mainlogger.info('Updating config values for ' + file_tag
                                    + ' from ' + file_path.name)
                configuration.recursive_update(loader.load(file_path))
        except IOError:
            pass
        if file_tag == 'logging' and sys.platform.startswith('freebsd'):
            try:
                with open(os.path.join(d,
                                       file_tag
                                       + f'_freebsd{fmt}')) as file_path:
                    # __
                    configuration.recursive_update(loader.load(file_path))
            except IOError:
                pass
        if file_tag == 'user_config' and sys.platform.startswith('win'):
            try:
                with open(os.path.join(d,
                                       file_tag
                                       + f'_windows{fmt}')) as file_path:
                    # __
                    configuration.recursive_update(loader.load(file_path))
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


def deci_and_frac_repr(n, output='default'):
    """
    Standard decimal (if any) and reduced fraction representations of number n

    A decimal representation is taken into account only if it has at most two
    fractional digits.

    'default' output is a str (e.g. "dfrac{3}{4} (or 0.75)")
    'js' output is a list of these representations
    (e.g. ['3/4', '0.75', 'any_fraction == 3/4'])
    """
    fraction_among_answers = False
    if isinstance(n, Fraction):
        fraction_among_answers = True
        f = Fraction(n.sign, n.numerator, n.denominator)
        deciv = n.evaluate().standardized()
        if deciv.fracdigits_nb() <= 2:
            representations = [f, deciv]
        else:
            representations = [f]
    else:
        n = Number(n).standardized()
        f = Fraction(from_decimal=n).reduced()
        representations = [n]
        if f.numerator < 100 and f.denominator < 100 and f.denominator != 1:
            fraction_among_answers = True
            representations.append(f)
    if output == 'js':
        results = [i.uiprinted for i in representations]
        if fraction_among_answers:
            results.append(f'any_fraction == {f.uiprinted}')
        return results
    else:  # 'default'
        r = [f"${i.printed}$" if isinstance(i, Fraction) else i.printed
             for i in representations]
        if len(representations) == 1:
            return r[0]
        else:
            return _('{n1} (or {n2})').format(n1=r[0], n2=r[1])


def closest_nn_outside_data(line, i):
    """The closest natural number to the ith item of line."""
    n = p = line[i]
    assert p >= 0
    while n in line and p in line:
        n += 1
        if p > 1:
            p -= 1
    if n not in line:
        return n
    else:
        return p


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


def rotate(L, n):
    """Rotate list L of n places, to the right if n > 0; else to the left."""
    return L[-n:] + L[:-n]


def divisors(n):
    output = []
    for i in range(1, int(n ** Number(0.5)) + 1):
        if n % i == 0:
            output.append(i)
            output.append(n // i)
    return sorted(output)


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
