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


class Generator(object, metaclass=ABCMeta):

    def check_args(self, codename=None, variant=None, labels=None, name=None):
        if type(codename) is not str:
            raise TypeError('codename must be a str, found {} instead.'
                            .format(type(codename)))
        if not hasattr(self, '_' + codename):
            raise ValueError('Cannot generate \'{}\'.'.format(codename))
        if not isinstance(labels, list):
            raise TypeError('labels must be a list, found {} instead.'
                            .format(type(labels)))
        if not all([isinstance(t, tuple) and len(t) == 2
                    and isinstance(t[0], int)
                    for t in labels]):
            raise TypeError('All elements of the labels list must be tuples '
                            'of two elements, first being an int.')
        if codename.endswith('r'):
            codename = codename[:-1]
        codename_nb = [int(_) for _ in codename.split('_')[1:]]
        labels_nb = [t[0] for t in labels]
        if sorted(codename_nb) != sorted(labels_nb):
            raise ValueError('The given labels list does not match the '
                             'codename: labels\' numbers {} != {}'
                             .format(labels_nb, codename_nb))

    @abstractmethod
    def generate(self, codename=None, variant=None, labels=None, name=None,
                 **kwargs):
        """Return the generated object."""