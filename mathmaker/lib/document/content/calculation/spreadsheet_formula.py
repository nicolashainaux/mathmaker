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

import random
from string import ascii_uppercase as alphabet

from intspan import intspan
from mathmakerlib import required

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.document.content.expression_creator import ExpressionCreator
from mathmaker.lib.tools.frameworks import process_autofit
from mathmaker.lib.LaTeX import SlideContent, TabularCellPictureWording
from mathmaker.lib.LaTeX import SpreadsheetPicture

# Possible variants (where X and Y represent a cell; n and p fixed numbers)

# 100   = n + p*X           104   = n + X/p
# 101   = n - p*X           105   = n - X/p
# 102   = p*X + n           106   = X/p + n
# 103   = p*X - n           107   = X/p - n

# 108   = n + p/X           112   = n*(X + p)
# 109   = n - p/X           113   = n*(X - p)
# 110   = p/X + n           114   = n/(X + p)
# 111   = p/X - n           115   = n/(X - p)

# 116   = n*(p + X)         120   = (X + p)/n
# 117   = n*(p - X)         121   = (X - p)/n
# 118   = n/(p + X)         122   = (p + X)/n
# 119   = n/(p - X)         123   = (p - X)/n

# 124   = X*X + n           128   = X*X
# 125   = n + X*X           129   = n * X*X
# 126   = X*X - n           130   = X*X / n
# 127   = n - X*X           131   = n / (X*X)

# 132   = X*X + X           136   = X*p + n
# 133   = X + X*X           137   = X*p - n
# 134   = X*X - X           138   = n + X*p
# 135   = X*X * n           139   = n - X*p

# 140   = X*X + n*X

# 200   =                   204   =
# 201   =                   205   =
# 202   =                   206   =
# 203   =                   207   =

# 208   =                   212   =
# 209   =                   213   =
# 210   =                   214   =
# 211   =                   215   =

FORMULAE = {
    '100': '=n+p*X', '101': '=n-p*X', '102': '=p*X+n', '103': '=p*X-n',
    '104': '=n+X/p', '105': '=n-X/p', '106': '=X/p+n', '107': '=X/p-n',
    '108': '=n+p/X', '109': '=n-p/X', '110': '=p/X+n', '111': '=p/X-n',
    '112': '=n*(X+p)', '113': '=n*(X-p)', '114': '=n/(X+p)', '115': '=n/(X-p)',
    '116': '=n*(p+X)', '117': '=n*(p-X)', '118': '=n/(p+X)', '119': '=n/(p-X)',
    '120': '=(X+p)/n', '121': '=(X-p)/n', '122': '=(p+X)/n', '123': '=(p-X)/n',
    '124': '=X*X+n', '125': '=n+X*X', '126': '=X*X-n', '127': '=n-X*X',
    '128': '=X*X', '129': '=n*X*X', '130': '=X*X/n', '131': '=n/(X*X)',
    '132': '=X*X+X', '133': '=X+X*X', '134': '=X*X-X',
    '135': '=X*X*n', '136': '=X*p+n', '137': '=X*p-n', '138': '=n+X*p',
    '139': '=n-X*p',
    '140': '=X*X+n*X'
}


class sub_object(ExpressionCreator, component.structure):

    def __init__(self, build_data, **options):
        # Since minimal setup will be called later for each source, do not call
        # it here, it would be overriden. Save it instead.
        self.options = options
        required.package['sourcecodepro'] = True
        build_data = process_autofit(build_data[0])
        self.cell1 = self.cell2 = self.cell3 = ''
        self.col = shared.cols_for_spreadsheets_source.next()[0]
        self.row = random.randint(1, 9)
        build_data['tl_cell'] = [self.col, self.row]
        self.layout = random.choice(['horizontal', 'vertical'])
        self.Xcell = f'{self.col}{self.row}'
        self.nextrow = self.row + 1
        # OK since letters up to M only are used:
        self.nextcol = alphabet[alphabet.index(self.col) + 1]
        if self.layout == 'horizontal':
            self.qcell = f'{self.nextcol}{self.row}'
        elif self.layout == 'vertical':
            self.qcell = f'{self.col}{self.nextrow}'
        variant_span = intspan(build_data['xid']['source']
                               [len('expressions:'):])
        if len(variant_span) == 1:
            self.variant_id = str(list(variant_span)[0])
        else:
            self.variant_id = shared.expressions_source.next(
                nb1_in=list(variant_span))[0]
        var_nb = str(self.variant_id)[0]
        self.variant_name = {'1': '1variable', '2': '2variables'}[var_nb]
        self.setup_sources(build_data)
        getattr(self, f'_create_variant_{self.variant_id}')(build_data)
        self.formula = FORMULAE[str(self.variant_id)]
        self.setup_formula_cell1_cell2()

        self.wording1 = _('In {cell_ref}, one types {formula}.')\
            .format(formula=r'{\codefont F}'.replace('F', self.formula),
                    cell_ref=r'{\codefont R}'.replace('R', self.qcell))
        self.wording2 = _('What will it display once enter is pressed?')
        self.wording = f'{self.wording1} {self.wording2}'
        self.setup_picture(build_data)
        self.transduration = 30

    def q(self, **options):
        if self.slideshow:
            output = SlideContent(wording1=self.wording1,
                                  height1='0.25pt',
                                  picture=self.picture,
                                  height2='0.25pt',
                                  wording2=self.wording2)
        else:
            w1 = {'horizontal': '5.75', 'vertical': '4'}[self.layout]
            w2 = {'horizontal': '7.75', 'vertical': '9'}[self.layout]
            output = TabularCellPictureWording(self.picture,
                                               self.wording, w1=w1, w2=w2)
        return str(output)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer.printed

    def js_a(self, **kwargs):
        return [self.answer.uiprinted]

    def setup_picture(self, build_data):
        bl = {'horizontal': '30pt', 'vertical': '3pt'}[self.layout]
        options = {'baseline': bl}
        if self.slideshow:
            options['cellnodeoptions'] = {'font': r'\small'}
            options['coordoptions'] = {'font': r'\small'}
            options['scale'] = '1.5'
        self.picture = str(SpreadsheetPicture(
            self.variant_name, self.layout, self.row, self.nextrow, self.col,
            self.nextcol, self.cell1, self.cell2, **options))

    def setup_formula_cell1_cell2(self):
        self.formula = self.formula.replace('n', self.nb1.printed)\
            .replace('p', self.nb2.printed).replace('X', self.Xcell)
        self.cell1 = r'\text{{{c1}}}'.format(c1=self.nb3.printed)
        self.cell2 = r'\textcolor{BrickRed}{\text{?}}'
