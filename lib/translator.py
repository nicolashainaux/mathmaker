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

from lib.common import latex
from lib import is_
from . import error
from lib.common.settings import config

if config.MARKUP == 'latex':
    from lib.common.latex import MARKUP



# --------------------------------------------------------------------------
##
#   @brief Writes a table filled with the given [strings]
#   @param size: (nb of lines, nb of columns)
#   @param chosen_markup
#   @param content: [strings]
#   @options col_fmt: [int|<'l'|'c'|'r'>]
#   @options: borders='all'|'v_internal'
#   @options: unit='inch' etc. (check the possibilities...)
#   @return
def create_table(size, content, **options):
    if config.MARKUP == 'latex':
        n_col = size[1]
        n_lin = size[0]
        result = ""

        length_unit = 'cm'
        if 'unit' in options:
            length_unit = options['unit']

        tabular_format = ""
        v_border = ""
        h_border = ""
        justify = ["" for _ in range(n_col)]
        new_line_sep = "\\\\" + "\n"
        min_row_height = ""

        # The last column is not centered vertically (LaTeX bug?)
        # As a workaround it's possible to add an extra empty column...
        extra_last_column = ""
        extra_col_sep = ""

        if 'justify' in options and type(options['justify']) == list:
            if not len(options['justify']) == n_col:
                raise ValueError("The number of elements of this list should "\
                                 "be equal to the number of columns of the "\
                                 "tabular.")
            new_line_sep = "\\tabularnewline" + "\n"
            extra_last_column = "@{}m{0pt}@{}"
            extra_col_sep = " & "
            justify = []
            for i in range(n_col):
                if options['justify'][i] == 'center':
                    justify.append(">{\centering}")
                elif options['justify'][i] == 'left':
                    justify.append(">{}")
                else:
                    raise ValueError("Expecting 'left' or 'center' as values "\
                                     "of this list.")

        elif 'center' in options:
            new_line_sep = "\\tabularnewline" + "\n"
            extra_last_column = "@{}m{0pt}@{}"
            extra_col_sep = " & "
            justify = [">{\centering}" for _ in range(n_col)]

        if 'min_row_height' in options:
            min_row_height = " [" \
                           + str(options['min_row_height']) + length_unit \
                           + "] "

        cell_fmt = "p{"

        if 'center_vertically' in options:
            cell_fmt = "m{"

        if 'borders' in options and options['borders'] in ['all',
                                                           'v_internal',
                                                           'penultimate']:
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
                t = cell_fmt + str(col_fmt[i]) + " " + str(length_unit) + "}"

            vb = v_border
            if 'borders' in options and options['borders'] == "penultimate":
                if i == n_col - 1:
                    vb = "|"
                else:
                    vb = ""

            tabular_format += vb + justify[i] + t

        if 'borders' in options and options['borders'] == "penultimate":
            v_border = ""

        tabular_format += extra_last_column + v_border

        if 'borders' in options and options['borders'] in ['v_internal']:
            tabular_format = tabular_format[1:-1]

        result += "\\begin{tabular}{"+ tabular_format + "}" + "\n"
        result += h_border

        for i in range(int(n_lin)):
            for j in range(n_col):
                result += str(content[i*n_col + j])
                if j != n_col - 1:
                    result += "&" + "\n"
            if i != n_lin - 1:
                result += extra_col_sep + new_line_sep + min_row_height \
                       + h_border

        result += extra_col_sep + new_line_sep + min_row_height + h_border
        result += "\end{tabular}" + "\n"

        return result.replace(" $~", "$~").replace("~$~", "$~")

    else:
        raise error.NotImplementedYet("create_table using this markup: " \
                                        + config.MARKUP + " ")
