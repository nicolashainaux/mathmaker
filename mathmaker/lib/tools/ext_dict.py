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
"""Extend dict."""


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
