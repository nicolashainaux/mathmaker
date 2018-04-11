#!/usr/bin/env python3
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

import sys
import locale
import gettext

from mathmakerlib import required, mmlib_setup
from mathmakerlib.calculus import Number
from mathmakerlib.LaTeX import KNOWN_AMSSYMB_SYMBOLS

from mathmaker import settings
from mathmaker import __software_name__
from mathmaker.lib import shared
from mathmaker.lib.tools.generators.shapes import ShapeGenerator
from mathmaker.lib.constants import LOCALE_US

SHAPES_CATALOG_PATH = './shapes_catalog.tex'
SG = ShapeGenerator()
MAX_ROWS_PER_PAGE = 11
COL_NB = 2


def __main__():
    settings.init()
    settings.language = 'en'
    settings.locale = LOCALE_US
    locale.setlocale(locale.LC_ALL, settings.locale)
    gettext.translation(__software_name__,
                        settings.localedir, ['en']).install()
    shared.init()
    required.init()
    mmlib_setup.init()

    output = ''
    rows_per_page = 0
    polygons = tuple(shared.shapes_db.execute('SELECT * FROM polygons;'))
    for polygon_data in polygons:
        pictures = []
        codename, variant = polygon_data[4], polygon_data[7]
        table_name = '{}_shapes'.format(codename)
        if (codename, variant) == ('triangle_1_1_1', 0):
            table_name = 'scalene_triangle_shapes'
        elif (codename, variant) == ('triangle_1_1_1', 1):
            table_name = 'right_triangle_shapes'
        subvariants = tuple(shared.shapes_db.execute('SELECT * FROM {};'
                                                     .format(table_name)))
        subvariants = [t[0] for t in subvariants]
        sys.stderr.write('{}, variant {}, subvariants = {}\n'
                         .format(codename, variant, subvariants))
        sys.stderr.write('rows_per_page={}\n'.format(rows_per_page))
        coeffs = [int(c) for c in codename.split('_')[1:]][::-1]
        lbls = [Number('1.5') + n for n in range(len(coeffs))]
        labels = [(c, lbl) for c, lbl in zip(coeffs, lbls)]
        sg = getattr(SG, '_{}'.format(codename))
        # print('{}, {}, subvariants = {}, labels = {}'
        #       .format(codename, variant, subvariants, labels))
        for sv in subvariants:
            sys.stderr.write('create picture of subvariant #{}\n'.format(sv))
            pictures.append(sg(variant=variant, labels=labels,
                               label_vertices=False,
                               length_unit='dam', shape_variant_nb=sv).drawn)
        rows_nb = len(pictures) // COL_NB
        if len(pictures) % COL_NB != 0:
            rows_nb += 1
        sys.stderr.write('rows_nb={}\n'.format(rows_nb))
        rows_per_page += rows_nb
        if rows_per_page > MAX_ROWS_PER_PAGE:
            output += r'\newpage' + '\n'
            rows_per_page = rows_nb
            sys.stderr.write('reset rows_per_page to {}\n'
                             .format(rows_per_page))
        else:
            output += r'\noindent\makebox[\linewidth]'\
                r'{\rule{\paperwidth}{0.4pt}}' + '\n' + r'\newline' + '\n'
        cell1 = '{}, variant: {}\n'\
            .format(codename.replace('_', r'\_'), variant) + r' \newline '
        pictures += ['' for _ in range(COL_NB - (len(pictures) % COL_NB))]
        cell2 = shared.machine.write_layout((rows_nb, COL_NB), None,
                                            pictures)
        output += shared.machine.write_layout((1, 2), None,
                                              [cell1, cell2])
        output += r'\newline' + '\n'
    pkg = []
    if any([s in output for s in KNOWN_AMSSYMB_SYMBOLS]):
        pkg.append('amssymb')
    preamble = shared.machine.write_preamble(required_pkg=pkg)
    sys.stdout.write(r'''{preamble}
\begin{{document}}
{content}
\end{{document}}'''.format(preamble=preamble, content=output))


if __name__ == '__main__':
    __main__()
