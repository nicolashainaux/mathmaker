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

import os

from mathmaker import settings
from mathmaker.lib.tools.auxiliary_functions import check_unique_letters_words
from mathmaker.lib.tools import po_file


def test_wnl():
    """Checks w*l words are correct."""
    for lang in next(os.walk(settings.localedir))[1]:
        settings.language = lang
        for n in [4, 5]:
            if os.path.isfile(settings.localedir + lang
                              + "/LC_MESSAGES/w{}l.po".format(str(n))):
                words = po_file.get_list_of('words', lang, n)
                assert check_unique_letters_words(words, n)
