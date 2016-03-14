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

import polib
import sys
from random import shuffle

from . import settings

NB = {3 : "THREE", 4 : "FOUR", 5 : "FIVE", 6 : "SIX"}

def __get_list_of_words(language, nb_of_letters):
	output = []
	po = polib.pofile(settings.localedir \
					+ settings.language \
					+ "/LC_MESSAGES/" \
					+ "mathmaker"\
					+ ".po")

	for entry in po:
		if entry.msgid[:-3] == NB[nb_of_letters] + "_LETTERS_WORD_" \
			and entry.msgstr != "":
		#___
			output.append(entry.msgstr)

	return output

def four_letters_word(language):
	memory = __get_list_of_words(language, 4)
	shuffle(memory)
	collector = []
	
	while(True):
		collector.append(memory[0])
		output = memory.pop(0)

		if not memory:
			(memory, collector) = (collector, memory)
			shuffle(memory)

		yield output

def init():
    global four_letters_word_generator
    four_letters_word_generator = four_letters_word(settings.language)
