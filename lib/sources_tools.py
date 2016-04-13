# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import random

class infinite_source(object):

    def __init__(self, sources, **kwargs):
        self.collector = []
        for s in sources:
            self.collector.append([])
        self.sources = sources
        if 'refresh' in kwargs:
            if hasattr(kwargs['refresh'], 'refresh'):
                if hasattr(kwargs['refresh'].refresh, '__call__'):
                    self.refresh = kwargs['refresh']
                else:
                    raise error.WrongArgument("kwargs['refresh'].refresh is " \
                    + "not callable.", "kwargs['refresh'] having a callable " \
                    + "refresh attribute.")
            else:
                raise error.WrongArgument("kwargs['refresh'] is an object" \
                + "without refresh attribute.", "an object having a " \
                + "refresh attribute.")

    def __next__(self):
        return self.next()

    def next(self, **kwargs):
        sce_nb = random.choice([ n for n in range(len(self.sources)) ])
        if 'choice' in kwargs:
            sce_nb = kwargs['choice']
        i = random.choice([ n for n in range(len(self.sources[sce_nb])) ])
        self.collector[sce_nb].append(self.sources[sce_nb][i])
        output = self.sources[sce_nb].pop(i)
        if not self.sources[sce_nb]:
            if hasattr(self, 'refresh'):
                self.sources[sce_nb] = self.refresh.refresh(sce_nb)
                self.collector[sce_nb] = []
            else:
                (self.sources[sce_nb], self.collector[sce_nb]) = \
                            (self.collector[sce_nb], self.sources[sce_nb])
        return output


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class bidict
# @brief A bidirectional dictionary inspired from
#        http://stackoverflow.com/questions/3318625/efficient-bidirectional
#        -hash-table-in-python
#        Must be built with lists of values, like:
#        d = bidict({'a': [1, 2, 3, 4], 'b': [4, 5, 7, 8], 'c': [2, 4, 7],
#                    'd': [1, 6, 8]})
#        then d.inverse contains:
#        {1: ['a', 'd'], 2: ['a', 'c'], 3: ['a'], 4: ['a', 'c', 'b'],
#         5: ['b'], 6: ['d'], 7: ['c', 'b'], 8: ['d', 'b']}
class bidict(dict):
	def __init__(self, *args, **kwargs):
		super(bidict, self).__init__(*args, **kwargs)
		self.inverse = {}
		for key, value in self.items():
			for v in value:
				self.inverse.setdefault(v, []).append(key)

    # In case adding a new value is someday useful, here is the code
	#def __setitem__(self, key, value):
	#	self.setdefault(key,[]).append(value)
	#	self.inverse.setdefault(value,[]).append(key)

    # But I didn't hack the code to delete a key
	#def __delitem__(self, key):
	#	self.inverse.setdefault(self[key],[]).remove(key)
	#	if self[key] in self.inverse and not self.inverse[self[key]]:
	#		del self.inverse[self[key]]
	#	super(bidict, self).__delitem__(key)