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
from random import shuffle

from . import settings
#import lib.common.surnames

NB = {3 : "THREE", 4 : "FOUR", 5 : "FIVE", 6 : "SIX"}

def __retrieve_from_po_file(language, nb_of_letters):
	output = []
	po = polib.pofile(settings.localedir \
					+ settings.language \
					+ "/LC_MESSAGES/" \
					+ "w" + str(nb_of_letters) + "l" \
					+ ".po")

	for entry in po:
		if len(entry.msgstr) == nb_of_letters:
			output.append(entry.msgstr)

	return output


def __get_list_of_words(language, nb_of_letters):
	output = __retrieve_from_po_file(language, nb_of_letters)

	if len(output) < 20:
		output.append(__retrieve_from_po_file('en', nb_of_letters))

	return output


def infinite_generator(memory):
	shuffle(memory)
	collector = []

	while(True):
		collector.append(memory[0])
		output = memory.pop(0)

		if not memory:
			(memory, collector) = (collector, memory)
			shuffle(memory)

		yield output


def four_letters_word(language):
	return infinite_generator(__get_list_of_words(language, 4))


#def surnames():
#	return infinite_generator(lib.common.surnames.LIST)


def init():
    global four_letters_word_generator
#	global surnames_generator

    four_letters_word_generator = four_letters_word(settings.language)
#	surnames_generator = surnames()
