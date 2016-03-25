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
import sys
import polib
import random
from random import shuffle

from . import settings
#import lib.common.surnames

NB = {3 : "THREE", 4 : "FOUR", 5 : "FIVE", 6 : "SIX"}

def __retrieve_from_po_file(language, po_filename):
	po = polib.pofile(settings.localedir \
					+ settings.language \
					+ "/LC_MESSAGES/" \
					+ po_filename \
					+ ".po")

	return [ entry.msgstr for entry in po if entry.msgstr != "" ]


def __get_list_of(what, language, arg):
	what_map = { "words" : "w" + str(arg) + "l",
	 			 "names" : str(arg) + "_names" }

	output = __retrieve_from_po_file(language, what_map[what])

	if len(output) < 20:
		output.append(__retrieve_from_po_file('en', what_map[what]))

	return output

class infinite_iterator(object):

	def __init__(self, sources):
		self.collector = []

		for s in sources:
			shuffle(s)
			self.collector.append([])

		self.sources = sources

	def __iter__(self):
		return self

	def __next__(self, **options):
		sce_nb = 0

		if 'choice' in options:
			sce_nb = options['choice']
		else:
			choices = [ n for n in range(len(self.sources)) ]
			sce_nb = random.choice(choices)

		source = self.sources[sce_nb]
		collector = self.collector[sce_nb]

		collector.append(source[0])
		output = source.pop(0)

		if not source:
			(source, collector) = (collector, source)
			shuffle(source)

		return output


def four_letters_words(language):
	return infinite_iterator([__get_list_of("words", language, 4)])

def names(language):
	return infinite_iterator([__get_list_of("names", language, "masculine"),
							  __get_list_of("names", language, "feminine")])

def init():
	global four_letters_words_source
	global names_source

	four_letters_words_source = four_letters_words(settings.language)
	names_source = names(settings.language)
