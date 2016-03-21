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

def __retrieve_from_po_file(language, po_filename):
	output = []
	po = polib.pofile(settings.localedir \
					+ settings.language \
					+ "/LC_MESSAGES/" \
					+ po_filename \
					+ ".po")

	for entry in po:
		if len(entry.msgstr) == nb_of_letters:
			output.append(entry.msgstr)

	return output


def __get_list_of(what, language, arg):
	what_map = { "words" : "w" + str(nb_of_letters) + "l",
	 			 "names" : arg + "_names" }

	output = __retrieve_from_po_file(language, what_map[what])

	if len(output) < 20:
		output.append(__retrieve_from_po_file('en', what_map[what]))

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
	return infinite_generator(__get_list_of("words", language, 4))

def masculine_names():
	return infinite_generator(__get_list_of("names", language, "masculine"))

def feminine_names():
	return infinite_generator(__get_list_of("names", language, "feminine"))


def init():
    global four_letters_word_generator
	global masculine_names_generator
	global feminine_names_generator

    four_letters_word_generator = four_letters_word(settings.language)
	masculine_names_generator = masculine_names(settings.language)
	feminine_names_generator = feminine_names(settings.language)
