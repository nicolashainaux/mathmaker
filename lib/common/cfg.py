# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from . import software
from lib import error

# CFG FILE DATA
FILE_NAME = software.ROOT_PATH \
            + software.NAME + '.' \
            + software.CFG_FILE_SUFFIX
COMMENT_TOKEN = '#'
CATEGORY_TOKEN = '['


# --------------------------------------------------------------------------
##
#   @brief Gets the value of the given option.
#   For instance, cfg.get_value_from_file(latex.FORMAT, "ENCODING") gets the
#   encoding value for LaTeX
#   @param  category Options' category (LOCALES, LATEX...)
#   @param  nom Exact name of the option
def get_value_from_file(category, option_name):
    category_was_found = False
    category_was_found_at_least_once = False

    try:
        f = open(FILE_NAME, mode = 'r')
    except NameError:
        raise error.UnreachableData("the file named : " + str(FILE_NAME))

    for line in f:
        # jump over the comment lines of the file
        if not line[0] == COMMENT_TOKEN:
            # check first if a category was found :
            if line[0] == CATEGORY_TOKEN:
                if line[1:len(line)-2] == category:
                    category_was_found = True
                    category_was_found_at_least_once = True
                else:
                    category_was_found = False

            # at this point, no comment nor category token has been found
            # on the current line. if a category was previously found, let's
            # check if the option we're looking for is on the current line
            elif category_was_found:
                if line[0:len(option_name)] == option_name:
                    return line[len(option_name)+1:len(line)-1]

    if category_was_found_at_least_once:
        raise error.UnreachableData("the option " + option_name               \
                                    + " in the category " + category          \
                                    + " of the cfg file.")

    else:
        raise error.UnreachableData("the category " + category                \
                                    + " of the cfg file.")





