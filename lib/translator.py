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

from lib.common import cfg
from lib.common import latex
from lib import is_
from . import error


markup_choice = cfg.get_value_from_file('MARKUP', 'USE')

if markup_choice == 'latex':
    from lib.common.latex import MARKUP



# --------------------------------------------------------------------------
##
#   @brief Writes a table filled with the given [strings]
#   @param size : (nb of lines, nb of columns)
#   @param chosen_markup
#   @param content : [strings]
#   @options col_fmt : [int|<'l'|'c'|'r'>]
#   @options : borders='all'
#   @options : unit='inch' etc. (check the possibilities...)
#   @return
def create_table(size, content, **options):
    if markup_choice == 'latex':
        n_col = size[1]
        n_lin = size[0]
        result = ""

        length_unit = 'cm'
        if 'unit' in options:
            length_unit = options['unit']

        tabular_format = ""
        v_border = ""
        h_border = ""
        center = ""
        new_line_sep = "\\\\" + "\n"

        if 'center' in options:
            center = ">{\centering}"
            new_line_sep = "\\tabularnewline" + "\n"

        if 'borders' in options and options['borders'] == 'all':
            v_border = "|"
            h_border = "\\hline \n"

        col_fmt = ['c' for i in range(n_col)]

        #DBG
        #error.write_warning("type(options['col_fmt']) = " + type(options['col_fmt']))

        if 'col_fmt' in options and type(options['col_fmt']) == list \
            and len(options['col_fmt']) == n_col:
        #___
            for i in range(len(col_fmt)):
                col_fmt[i] = options['col_fmt'][i]

        for i in range(len(col_fmt)):
            t = col_fmt[i]
            if is_.a_number(col_fmt[i]):
                t = "p{" + str(col_fmt[i]) + " " + str(length_unit) + "}"

            tabular_format += v_border \
                              + center \
                              + t

        tabular_format += v_border

        result += "\\begin{tabular}{"+ tabular_format + "}" + "\n"
        result += h_border

        for i in range(n_lin):
            for j in range(n_col):
                result += str(content[i*n_col + j])
                if j != n_col - 1:
                    result += "&" + "\n"
            if i != n_lin - 1:
                result += new_line_sep + h_border

        result += new_line_sep + h_border
        result += "\end{tabular}" + "\n"

        return result

    else:
        raise error.NotImplementedYet("create_table using this markup : " \
                                        + markup_choice + " ")








