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
import sys
import time
import subprocess
from tempfile import NamedTemporaryFile

from mathmaker import settings
from mathmaker.lib import is_, error
from mathmaker.lib.common import latex
from mathmaker.lib.common.cst import TEXT_SCALES, TEXT_RANKS
from mathmaker.lib.tools import header_comment
from mathmaker.lib.core.base import Printable, Drawable

from . import Structure


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class LaTeX
# @brief This machine knows how to write LaTeX commands & math expressions
# @todo When creating another machine, some things might have to change here
class LaTeX(Structure.Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   The created machine is set to the beginning of an expression,
    #   its language is the default one (from cfg file or in case of any
    #   problem, from text.DEFAULT_LANGUAGE)
    #   its encoding is set to the default one (from cfg file or in case of any
    #   problem, from latex.DEFAULT_ENCODING)
    #   @param expression_begins True if machine's at an expression's beginning
    #   @param **options Any options
    #   @return One instance of machine.LaTeX
    def __init__(self, language, create_pic_files=True, **options):
        self.text_sizes = latex.TEXT_SIZES
        self.font_size_offset = 0
        self.create_pic_files = create_pic_files
        self.language_code = language
        self.language = latex.LANGUAGE_PACKAGE_NAME[language]
        self.markup = latex.MARKUP
        self.out = sys.stdout
        self.redirect_output_to_str = True

    # --------------------------------------------------------------------------
    ##
    #   @brief Write the complete LaTeX header of the sheet to the output.
    def write_document_header(self):
        result = header_comment.generate(latex.FORMAT_NAME_PRINT)
        result += "\documentclass[a4paper,fleqn,12pt]{article}" + "\n"
        result += r"\usepackage{fontspec}" + "\n"
        if settings.font is not None:
            result += r"\setmainfont{" + settings.font + "}" + "\n"
            result += r"\newfontfamily\configfont{" + settings.font + "}\n"
        result += r"\usepackage{polyglossia}" + "\n"
        result += "\setmainlanguage{" + self.language + "}" + "\n"
        if self.language_code in latex.LANGUAGE_OPTIONS:
            lod = latex.LANGUAGE_OPTIONS[self.language_code]
            lang_options = ",".join([str(o) + "=" + str(lod[o])
                                     for o in lod])
            result += "".join(["\setkeys{", self.language, "}"
                               "{", lang_options, "}\n"])
        result += "% " + _("To display units correctly") + "\n"
        result += r"\usepackage[detect-all]{siunitx}" + "\n"
        sisetup_dict = {}
        if settings.language == "fr_FR":
            sisetup_dict.update({'locale': 'FR'})
        if settings.font is not None:
            sisetup_dict.update({'text-rm': r'\configfont'})
        if len(sisetup_dict):
            sisetup_str = ", ".join([k + " = " + sisetup_dict[k]
                                     for k in sisetup_dict])
            result += "\AtBeginDocument{\n"
            result += "\sisetup{" + sisetup_str + "}\n"
            result += "}\n"
        result += "% " + _("To strike out numbers ") + "\n"
        result += r"\usepackage{cancel}" + "\n"
        result += "% " + _("To use the margin definition command") + "\n"
        result += r"\usepackage{geometry}" + "\n"
        result += "% " + _("To use the commands from {pkg_name} ")\
            .format(pkg_name="theorem") + "\n"
        result += r"%\usepackage{theorem}" + "\n"
        result += "% " + _("To use multicol environment") + "\n"
        result += r"\usepackage{multicol}" + "\n"
        result += "% " + _("To use extra commands to handle tabulars") + "\n"
        result += r"\usepackage{array}" + "\n"
        result += "% " + _("For pretty underlining") + "\n"
        result += r"\usepackage{ulem}" + "\n"
        result += "% " + _("To include .eps pictures (loads graphicx)") + "\n"
        # result += r"\usepackage{graphbox}" + "\n"
        result += r"\usepackage{graphicx}" + "\n"
        result += "% " + _("To use some symbols like currency units") + "\n"
        result += r"\usepackage{textcomp}" + "\n"
        result += r"\usepackage{eurosym}" + "\n"
        result += "% " + _("To use other mathematical symbols") + "\n"
        result += r"\usepackage{amssymb}" + "\n"
        result += r"\usepackage{amsmath}" + "\n"
        result += "% " + _("To draw") + "\n"
        result += r"\usepackage{tikz}" + "\n"
        result += "% " + _("Page layout ") + "\n"
        result += "\geometry{hmargin=0.75cm, vmargin=0.75cm}" + "\n"
        result += "\setlength{\parindent}{0cm}" + "\n"
        result += r"\setlength{\arrayrulewidth}{0.02pt}" + "\n"
        result += "\pagestyle{empty}" + "\n"
        result += " " + "\n"
        result += r"\usepackage{epstopdf}" + "\n"
        result += "%%% " + _("If you wish to include a picture, \
please use this command:") + "\n"
        result += "%%% \includegraphics[height=6cm]{"
        result += _("file_name")
        result += ".eps} \n"
        result += " " + "\n"
        result += "% " + _("Exercises counter") + "\n"
        result += "\\newcounter{n}" + "\n"
        result += "% " + _("Definition of the {cmd_name} command, \
which will insert the word {word} in bold, with its number and \
automatically increments the counter").format(cmd_name="exercise",
                                              word=_("Exercise")) + "\n"
        result += "\\newcommand{\exercise}{\\noindent \hspace{-.25cm}" \
            + " \stepcounter{n} " + self.translate_font_size('large') \
            + " \\textbf{" \
            + _("Exercise") \
            + " \\arabic{n}} " \
            + "\\newline " + self.translate_font_size('large') + " }" + " \n"
        result += "% " + _('Definition of the command resetting the '
                           'exercises counter (which is useful when begining '
                           'to write the answers sheet)') + '\n'
        result += "\\newcommand{\\razcompteur}{\setcounter{n}{0}}" + "\n"
        result += " " + "\n"
        result += r"\usetikzlibrary{calc}" + "\n"
        result += r"\epstopdfsetup{outdir=./}" + "\n"
        if settings.round_letters_in_math_expr:
            result += r"\usepackage{lxfonts}" + "\n"

        if settings.language == "fr_FR":
            result += r"\renewcommand{\parallel}{\mathbin{/\negthickspace/}}" \
                + "\n"

        if self.redirect_output_to_str:
            return result

        else:
            self.out.write(result)

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output the command to begin the document
    def write_document_begins(self):
        output_str = "\\begin{document}\n"
        if settings.font is not None:
            output_str += "\\fontspec{" + settings.font + "}\n"
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes to the output the end of document command
    def write_document_ends(self):
        output_str = "\end{document} " + "\n"
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes to the output the command displaying an exercise's title
    def write_exercise_number(self):
        output_str = "\exercise" + "\n"
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes to the output the jump to next page command
    def write_jump_to_next_page(self):
        output_str = "\\newpage" + "\n"
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes to the output the exercises counter reinitialize command
    def reset_exercises_counter(self):
        output_str = "\\razcompteur " + "\n"
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    def addvspace(self, height='30.0pt', **options):
        """
        Add a vertical space.
        """
        output_str = "\n\n\\addvspace{{{height}}}\n\n".format(height=height)
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes to the output the new line command
    def write_new_line(self, **options):
        output_str = "\\newline " + "\n"
        if 'check' in options:
            if options['check'] == '\]':
                output_str = ""
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes to the output two commands writing two new lines
    def write_new_line_twice(self, **options):
        output_str = "\\newline " + "\n" + " \\newline " + "\n"
        if 'check' in options:
            if options['check'] == '\]':
                output_str = ""
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Prints the given string as a mathematical expression
    def write_math_style2(self, given_string, **kwargs):
        spacing = " "
        if 'extra_spacing' in kwargs and not kwargs['extra_spacing']:
            spacing = ""
        output_str = self.markup['opening_math_style2'] + spacing \
            + given_string \
            + spacing + self.markup['closing_math_style2']
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Prints the given string as a mathematical expression
    def write_math_style1(self, given_string):
        output_str = self.markup['opening_math_style1'] + " " \
            + given_string \
            + " " + self.markup['closing_math_style1']

        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    def write_out(self, latex_document: str, pdf_output=False):
        """
        Writes the given document to the output.

        If pdf_output is set to True then the document will be compiled into
        a pdf and the pdf content will be written to output.

        :param latex_document: contains the entire LaTeX document
        :param pdf_output: if True, output will be written in pdf format
        """
        document = latex_document
        if pdf_output:
            with NamedTemporaryFile(mode='r+t') as tmp_file:
                tmp_file_name = os.path.basename(tmp_file.name)
                tmp_log_name = settings.outputdir + tmp_file_name + '.log'
                pdf_file_name = settings.outputdir + tmp_file_name + '.pdf'
                tmp_file.write(latex_document)
                tmp_file.seek(0)
                p = subprocess.Popen(['lualatex',
                                      '-interaction',
                                      'nonstopmode',
                                      tmp_file.name],
                                     cwd=settings.outputdir,
                                     stdout=sys.stderr)
                returncode = p.wait()
                if returncode:
                    saved_log_name = 'lualatex_' \
                        + time.strftime("%Y%m%d-%H%M%S") + '.log'
                    with open(tmp_log_name, mode='rt') as tmplog,\
                        open(saved_log_name, mode='wt') as savedlog:  # noqa
                        # __
                        savedlog.write(tmplog.read())
                        raise RuntimeError('lualatex had a problem while '
                                           'compiling. See ' + saved_log_name)
                with open(pdf_file_name, mode='rb') as pdf_file:
                    document = pdf_file.read()
                self.out = sys.stdout.buffer
                os.remove(pdf_file_name)
        self.out.write(document)

    ##
    #   @brief Writes to the output the given string
    #   @option emphasize='bold'|'italics'|'underlined'
    def write(self, given_string, **options):
        output_str = ""

        if 'emphasize' in options:
            if options['emphasize'] == 'bold':
                output_str = "\\textbf{" + given_string + "}" + "\n"
            elif options['emphasize'] == 'italics':
                output_str = "\\textit{" + given_string + "}" + "\n"
            elif options['emphasize'] == 'underlined':
                output_str = r"\uline{" + given_string + "}" + "\n"
            else:
                output_str = given_string
        else:
            output_str = given_string

        if 'multicolumns' in options:
            keyword = 'multicols'
            if options.get('unbalanced', False):
                keyword = 'multicols*'
            if (type(options['multicolumns']) == int
                and options['multicolumns'] >= 1):
                # __
                output_str = '\\begin{' + keyword + '}{' \
                             + str(options['multicolumns']) + "} " + "\n" \
                             + output_str \
                             + '\end{' + keyword + '}\n'
            else:
                raise ValueError('This: {} should be an int >=1\n'
                                 .format(str(options['multicolumns'])))

        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief turn the size keyword in LaTeX matching keyword
    #   @warning if you chose a too low or too high value as font_size_offset,
    #   @warning then all the text will be either tiny or Huge.
    def translate_font_size(self, arg):
        if not type(arg) == str:
            raise error.UncompatibleType(arg, "String")
        elif arg not in TEXT_SCALES:
            raise error.UncompatibleType(arg, "a text size (see TEXT_SCALES)")

        arg_num = TEXT_RANKS[arg]

        size_to_use = self.font_size_offset + arg_num

        if size_to_use < 0:
            size_to_use = 0
        elif size_to_use > len(self.text_sizes) - 1:
            size_to_use = len(self.text_sizes) - 1

        return self.text_sizes[size_to_use]

    ##
    #   @brief Writes to the output the command setting the text size
    def write_set_font_size_to(self, arg):
        output_str = self.translate_font_size(arg) + "\n"
        if self.redirect_output_to_str:
            return output_str
        else:
            self.out.write(output_str)

    ##
    #   @brief Writes content arranged like in a table.
    #   @brief In the case of latex, it will just be the same.
    #   @param size: (nb of lines, nb of columns)
    #   @param col_widths: [int]
    #   @param content: [strings]
    #   @options: borders=0|1|2|3... (not implemented yet)
    #   @options: unit='inch' etc. (check the possibilities...)
    def write_layout(self, size, col_widths, content, **options):
        if self.redirect_output_to_str:
            return self.create_table(size,
                                     content,
                                     col_fmt=col_widths,
                                     **options)
        else:
            self.out.write(self.create_table(size,
                                             content,
                                             col_fmt=col_widths,
                                             **options))

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
    def create_table(self, size, content, **options):
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
                raise ValueError("The number of elements of this list should "
                                 "be equal to the number of columns of the "
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
                    raise ValueError("Expecting 'left' or 'center' as values "
                                     "of this list.")

        elif 'center' in options:
            new_line_sep = "\\tabularnewline" + "\n"
            extra_last_column = "@{}m{0pt}@{}"
            extra_col_sep = " & "
            justify = [">{\centering}" for _ in range(n_col)]

        if 'min_row_height' in options:
            min_row_height = " [" + str(options['min_row_height']) \
                + length_unit + "] "

        cell_fmt = "p{"

        if 'center_vertically' in options and options['center_vertically']:
            cell_fmt = "m{"

        if 'borders' in options and options['borders'] in ['all',
                                                           'v_internal',
                                                           'penultimate']:
            v_border = "|"
            h_border = "\\hline \n"

        col_fmt = ['c' for i in range(n_col)]

        if ('col_fmt' in options and type(options['col_fmt']) == list
            and len(options['col_fmt']) == n_col):
            # __
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

        result += "\\begin{tabular}{" + tabular_format + "}" + "\n"
        result += h_border

        for i in range(int(n_lin)):
            for j in range(n_col):
                result += str(content[i * n_col + j])
                if j != n_col - 1:
                    result += "&" + "\n"
            if i != n_lin - 1:
                result += extra_col_sep + new_line_sep + min_row_height \
                    + h_border

        result += extra_col_sep + new_line_sep + min_row_height + h_border
        result += "\end{tabular}" + "\n"

        return result.replace(" $~", "$~").replace("~$~", "$~")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a LaTeX string of the given object
    def type_string(self, objct, **options):
        if isinstance(objct, Printable):
            options.update({'force_expression_begins': True})
            return objct.into_str(**options)
        elif is_.a_number(objct) or is_.a_string(objct):
            return str(objct)
        else:
            raise error.UncompatibleType(objct, "String|Number|Printable")

    # --------------------------------------------------------------------------
    ##
    #   @brief Draws a horizontal dashed line
    def insert_dashed_hline(self, **options):
        return "\\begin{tikzpicture}[x=2cm]" \
               + "\draw[black,line width=0.5pt,dashed] (0,0)--(9,0);" \
               + "\end{tikzpicture}" + "\n"

    # --------------------------------------------------------------------------
    ##
    #   @brief Puts a vertical space (default 1 cm)
    def insert_vspace(self, **options):
        return "\\vspace{1 cm}"

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a non-breaking space
    def insert_nonbreaking_space(self, **options):
        return "~"

    # --------------------------------------------------------------------------
    ##
    #   @brief Draws and inserts the picture of the drawable_arg
    def insert_picture(self, drawable_arg, **options):
        if not isinstance(drawable_arg, Drawable):
            raise error.WrongArgument(str(drawable_arg), 'a Drawable')

        if self.create_pic_files:
            drawable_arg.into_pic(**options)
        else:
            drawable_arg.into_pic(create_pic_files=False, **options)

        s = "1"
        if 'scale' in options:
            s = str(options['scale'])

        if 'vertical_alignment_in_a_tabular' in options:
            return "\\raisebox{-.5\height}{" \
                   + "\includegraphics[scale=" + s + "]{" \
                   + drawable_arg.eps_filename \
                   + "}" + "}"
        elif 'top_aligned_in_a_tabular' in options:
            # return "\includegraphics[align=t, scale=" + s + "]{" \
            #     + drawable_arg.eps_filename \
            #     + "}" + "\\newline" + "\n"
            return "\\raisebox{-0.9\height}{" \
                   + "\includegraphics[scale=" + s + "]{" \
                   + drawable_arg.eps_filename \
                   + "}" + "}"
        else:
            return "\includegraphics[scale=" + s + "]{" \
                + drawable_arg.eps_filename \
                + "}" + "\\newline" + "\n"

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the font_size_offset field
    def set_font_size_offset(self, arg):
        if not is_.an_integer(arg):
            raise error.UncompatibleType(arg, "Integer")

        else:
            self.font_size_offset = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the redirect_output_to_str field to True or False
    def set_redirect_output_to_str(self, arg):
        if type(arg) == bool:
            self.redirect_output_to_str = arg
        else:
            raise error.OutOfRangeArgument(arg, " boolean ")
