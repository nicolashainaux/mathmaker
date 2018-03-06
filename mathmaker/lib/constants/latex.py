# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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


FORMAT = 'LATEX'
FORMAT_NAME_PRINT = 'LaTeX'

# ENCODING
DEFAULT_ENCODING = 'utf8'
UTF8 = 'utf8'
UCS_UTF8X = 'ucs-utf8x'
UTF8X = 'utf8x'
LATIN1 = 'latin1'
ANSINEW = 'ansinew'

# VARIOUS
SPRING_HARDNESS = '4'

# LANGUAGE PACKAGES
FRANCAIS = 'french'
US_ENGLISH = 'english'
UK_ENGLISH = 'english'

# MATCHES BETWEEN LANGUAGE CODE ('fr', 'en' etc.)
# AND RELATED LATEX PACKAGE NAMES:
LANGUAGE_PACKAGE_NAME = {'fr': FRANCAIS,
                         'fr_FR': FRANCAIS,
                         'en': US_ENGLISH,
                         'en_US': US_ENGLISH,
                         'en_GB': UK_ENGLISH}

LANGUAGE_OPTIONS = {'en_US': {'variant': 'american'},
                    'en_GB': {'variant': 'british'}}

# TEXT SIZES
TEXT_SIZES = ['\\tiny', '\\scriptsize', '\\footnotesize', '\\small',
              '\\normalsize', '\large', '\Large', '\LARGE', '\\huge', '\\HUGE']

# LATEX MARKUPS' DICTIONNARY
MARKUP = {'LaTeX': "\LaTeX",
          'one': "\\text{1}",
          'zero': "\\text{0}",
          'space': " ",
          'small_space': "\\smallskip",
          'med_space': "\\medskip",
          'big_space': "\\bigskip",
          'nonbreaking_space': "~",
          'opening_bracket': "(",
          'closing_bracket': ")",
          'opening_exponent': "^{",
          'closing_exponent': "}",
          'opening_out_striked': "\\bcancel{",
          'closing_out_striked': "}",
          'plus': "+",
          'minus': "-",
          'times': "\\times ",
          'divide': "\div ",
          'equal': "=",
          'not_equal': "\\neq ",
          'opening_fraction': "\\frac{",
          'fraction_vinculum': "}{",
          'closing_fraction': "}",
          'opening_subscript': "_{",
          'closing_subscript': "}",
          'colon': ":",
          'newline': "\\newline ",
          'opening_math_style2': "$",
          'closing_math_style2': "$",
          'opening_math_style1': "\[",
          'closing_math_style1': "\]",
          'simeq': "\\simeq",
          'opening_sqrt': "\\sqrt{\mathstrut ",
          'closing_sqrt': "}",
          'open_text_in_maths': "\\text{",
          'close_text_in_maths': "}",
          'open_num': "\\num{",
          'close_num': "}",
          'open_underline': r"\uline{",
          'close_underline': "}",
          'opening_widehat': "\widehat{",
          'closing_widehat': "}",
          'opening_square_bracket': "\[",
          'closing_square_bracket': "\]",
          'text_degree': "\\textdegree",
          'fct_cos': "\cos"}

TEXT_SCALES = ['tiny', 'scriptsize', 'footnotesize', 'small', 'normal',
               'large', 'Large', 'LARGE', 'huge', 'HUGE']

TEXT_RANKS = {'tiny': 0, 'scriptsize': 1, 'footnotesize': 2, 'small': 3,
              'normal': 4, 'large': 5, 'Large': 6, 'LARGE': 7, 'huge': 8,
              'HUGE': 9}

COLORED_QUESTION_MARK = r'\textcolor{BrickRed}{\text{?}}'
COLORED_ANSWER = r'\textcolor{{OliveGreen}}{text}'
