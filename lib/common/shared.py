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
import random
from random import shuffle

from . import settings
from lib.sources_tools import get_list_of, infinite_source

def four_letters_words(language):
	return infinite_source([get_list_of("words", language, 4)])

def names(language):
	return infinite_source([get_list_of("names", language, "masculine"),
							get_list_of("names", language, "feminine")])

def init():
	global four_letters_words_source
	global names_source

	four_letters_words_source = four_letters_words(settings.language)
	names_source = names(settings.language)
