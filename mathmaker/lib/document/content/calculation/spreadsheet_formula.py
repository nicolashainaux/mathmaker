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

import copy
import random
from pathlib import Path
from string import ascii_uppercase as alphabet

from intspan import intspan
from mathmakerlib import required
from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.tools import divisors
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.frameworks import process_autofit

# Possible variants (where X and Y represent a cell; n and p fixed numbers)
# 100   = n + p*X           104   = X*p + n
# 101   = n + p/X           105   = X/p + n
# 102   = n - p*X           106   = X*p - n
# 103   = n - p/X           107   = X/p - n

# 108   = n + X*p           112   = p*X + n
# 109   = n + X/p           113   = p/X + n
# 110   = n - X*p           114   = p*X - n
# 111   = n - X/p           115   = p/X - n

# 116   = X*X               120   = X*X / n
# 117   = n + X*X           121   = X*X + n
# 118   = n - X*X           122   = X*X - n
# 119   = n * X*X           123   = X*X * n


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        # Since minimal setup will be called later for each source, do not call
        # it here, it would be overriden. Save it instead.
        self.options = options
        required.package['sourcecodepro'] = True
        required.package['tikz'] = True
        build_data = process_autofit(build_data[0])
        self.cell1 = self.cell2 = self.cell3 = ''
        self.col = shared.cols_for_spreadsheets_source.next()[0]
        self.row = random.randint(1, 9)
        build_data['tl_cell'] = [self.col, self.row]
        self.scheme = random.randint(1, 2)
        self.Xcell = f'{self.col}{self.row}'
        self.nextrow = self.row + 1
        # OK since letters up to M only are used:
        self.nextcol = alphabet[alphabet.index(self.col) + 1]
        if self.scheme == 1:
            self.qcell = f'{self.nextcol}{self.row}'
        elif self.scheme == 2:
            self.qcell = f'{self.col}{self.nextrow}'
        variant_span = intspan(build_data['fid']['source'][len('formulae:'):])
        if len(variant_span) == 1:
            self.variant_id = str(list(variant_span)[0])
        else:
            self.variant_id = shared.formulae_source.next(
                nb1_in=list(variant_span))[0]
        self.setup_sources(build_data)
        getattr(self, f'_create_variant_{self.variant_id}')(build_data)

        wording_part1 = _('In {cell_ref}, one types {formula}.')\
            .format(formula=r'{\codefont F}'.replace('F', self.formula),
                    cell_ref=r'{\codefont R}'.replace('R', self.qcell))
        wording_part2 = r'\small{TEXT}'\
            .replace('TEXT',
                     _('What will it display once enter is pressed?'))
        self.wording = f'{wording_part1} {wording_part2}'
        self.pic_options = ''
        self.setup_picture(build_data)
        self.transduration = 30

    def q(self, **options):
        if self.slideshow:
            template_name = 'templates/slide_picture_wording.tex'
        else:
            template_name = 'templates/inline_picture_wording.tex'
        template = (Path(__file__).parent / template_name).read_text()
        template = template.replace('PICTURE', self.picture)\
            .replace('WORDING', self.wording)
        if self.slideshow:
            return template.replace('HEIGHT', '2.5')
        else:
            w1 = {1: '5.75', 2: '4'}[self.scheme]
            w2 = {1: '7.75', 2: '9'}[self.scheme]
            return template.replace('COLW1', w1).replace('COLW2', w2)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer.printed

    def js_a(self, **kwargs):
        return [self.answer.uiprinted]

    def setup_sources(self, build_data):
        self.st1_source = build_data['st1']['source']
        self.st1_attr = {k: build_data['st1'][k]
                         for k in build_data['st1']
                         if k != 'source'}
        self.sf1_source = build_data['sf1']['source']
        self.sf1_attr = {k: build_data['sf1'][k]
                         for k in build_data['sf1']
                         if k != 'source'}
        self.sd1_source = build_data['sd1']['source']
        self.sd1_attr = {k: build_data['sd1'][k]
                         for k in build_data['sd1']
                         if k != 'source'}
        self.pr1_source = build_data['pr1']['source']
        self.pr1_attr = {k: build_data['pr1'][k]
                         for k in build_data['pr1']
                         if k != 'source'}
        self.sq1_source = build_data['sq1']['source']
        self.sq1_attr = {k: build_data['sq1'][k]
                         for k in build_data['sq1']
                         if k != 'source'}
        self.st2_source = build_data['st2']['source']
        self.st2_attr = {k: build_data['st2'][k]
                         for k in build_data['st2']
                         if k != 'source'}
        self.sf2_source = build_data['sf2']['source']
        self.sf2_attr = {k: build_data['sf2'][k]
                         for k in build_data['sf2']
                         if k != 'source'}
        self.sd2_source = build_data['sd2']['source']
        self.sd2_attr = {k: build_data['sd2'][k]
                         for k in build_data['sd2']
                         if k != 'source'}
        self.pr2_source = build_data['pr2']['source']
        self.pr2_attr = {k: build_data['pr2'][k]
                         for k in build_data['pr2']
                         if k != 'source'}
        self.sq2_source = build_data['sq2']['source']
        self.sq2_attr = {k: build_data['sq2'][k]
                         for k in build_data['sq2']
                         if k != 'source'}

    def setup_picture(self, build_data):
        var_nb = self.variant_id[0]
        template_name = f'templates/spreadsheet_{var_nb}_{self.scheme}.tikz'
        template = (Path(__file__).parent / template_name).read_text()
        row1 = r'\text{{{r1}}}'.format(r1=self.row)
        row2 = r'\text{{{r2}}}'.format(r2=self.nextrow)
        template = template.replace('ROW1', row1).replace('ROW2', row2)
        col1 = r'\text{{{c1}}}'.format(c1=self.col)
        col2 = r'\text{{{c2}}}'.format(c2=self.nextcol)
        template = template.replace('COL1', col1).replace('COL2', col2)
        template = template.replace('CELL1', self.cell1)\
            .replace('CELL2', self.cell2).replace('CELL3', self.cell3)
        self.pic_options = {1: '[baseline=30pt]',
                            2: '[baseline=3pt]'}[self.scheme]
        self.picture = template.replace('OPTIONS', self.pic_options)

    def setup_term_nb1_product_nb2_nb3(self):
        n = shared.mc_source.next(self.st1_source, qkw=self.st1_attr)[0]
        p, val = shared.mc_source.next(self.pr1_source, qkw=self.pr1_attr)
        # self.nb1 = n; self.nb2 = p; self.nb3 = val (X)
        super().setup("numbers", nb=[n, p, val], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.st1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], **self.st1_attr)
        options = copy.deepcopy(self.options)
        options.update(self.pr1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2, 3], **self.pr1_attr)

    def setup_term_nb1_square_nb2_nb3(self):
        n = shared.mc_source.next(self.st1_source, qkw=self.st1_attr)[0]
        p, v = shared.mc_source.next(self.sq1_source, qkw=self.sq1_attr)
        # self.nb1 = n; self.nb2 = self.nb3 = val (X)
        super().setup("numbers", nb=[n, p, v], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.st1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], **self.st1_attr)
        options = copy.deepcopy(self.options)
        options.update(self.sq1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2, 3], **self.sq1_attr)
        if self.nb2 < self.nb3:
            self.nb3 = self.nb2
        elif self.nb3 < self.nb3:
            self.nb2 = self.nb3

    def setup_square_nb2_nb3(self):
        p, v = shared.mc_source.next(self.sq1_source, qkw=self.sq1_attr)
        # self.nb2 = self.nb3 = val (X)
        super().setup("numbers", nb=[p, v], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.sq1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2, 3], **self.sq1_attr)
        if self.nb2 < self.nb3:
            self.nb3 = self.nb2
        elif self.nb3 < self.nb3:
            self.nb2 = self.nb3

    def setup_factor_nb1_square_nb2_nb3(self):
        n = shared.mc_source.next(self.sf1_source, qkw=self.sf1_attr)[0]
        p, v = shared.mc_source.next(self.sq1_source, qkw=self.sq1_attr)
        # self.nb1 = n; self.nb2 = self.nb3 = val (X)
        super().setup("numbers", nb=[n, p, v], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.sf1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], **self.sf1_attr)
        options = copy.deepcopy(self.options)
        options.update(self.sq1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2, 3], **self.sq1_attr)
        if self.nb2 < self.nb3:
            self.nb3 = self.nb2
        elif self.nb3 < self.nb3:
            self.nb2 = self.nb3

    def setup_divisor_nb1_square_nb2_nb3(self):
        p, v = shared.mc_source.next(self.sq1_source, qkw=self.sq1_attr)
        pv_divisors = divisors(p * v)
        sd_span = intspan(self.sd1_source.split(':')[1])
        sd_list = [d for d in sd_span if d in pv_divisors]
        sd_list += list(intspan(self.sd1_attr.get('include', '')))
        sd_span = intspan(sd_list)
        sd_source = f'nnsingletons:{str(sd_span)}'
        import sys
        sys.stderr.write(f'sd_source={sd_source}\n')
        n = shared.mc_source.next(sd_source, qkw=self.sd1_attr)[0]
        # self.nb1 = n; self.nb2 = self.nb3 = val (X)
        super().setup("numbers", nb=[n, p, v], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.sd1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], **self.sd1_attr)
        options = copy.deepcopy(self.options)
        options.update(self.sq1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2], **self.sq1_attr)
        self.nb3 = self.nb2

    def setup_formula_cell1_cell2(self):
        self.formula = self.formula.replace('n', self.nb1.printed)\
            .replace('p', self.nb2.printed).replace('X', self.Xcell)
        self.cell1 = r'\text{{{c1}}}'.format(c1=self.nb3.printed)
        self.cell2 = r'\textcolor{BrickRed}{\text{?}}'

    def _create_variant_100(self, build_data):
        self.formula = '=n+p*X'
        self.setup_term_nb1_product_nb2_nb3()
        self.answer = (self.nb1 + self.nb2 * self.nb3).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_101(self, build_data):
        self.formula = '=n+p/X'
        self.setup_term_nb1_product_nb2_nb3()
        while self.nb3.fracdigits_nb():  # to avoid dividing by a decimal
            self.nb2 /= 10
            self.nb3 *= 10
        self.nb2 = self.nb2 * self.nb3
        self.nb2 = self.nb2.standardized()
        self.nb3 = self.nb3.standardized()
        self.answer = (self.nb1 + self.nb2 / self.nb3).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_102(self, build_data):
        self.formula = '=n-p*X'
        self.setup_term_nb1_product_nb2_nb3()
        if (self.subvariant == 'only_positive'
            and self.nb2 * self.nb3 > self.nb1):
            self.nb1 += self.nb2 * self.nb3
            self.nb1 = self.nb1.standardized()
        self.answer = (self.nb1 - self.nb2 * self.nb3).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_103(self, build_data):
        self._create_variant_101(build_data)
        self.formula = '=n-p/X'
        self.answer = self.nb1 - self.nb2 / self.nb3
        # add up to self.nb1 to avoid negative result
        if self.subvariant == 'only_positive' and self.answer < 0:
            self.nb1 = (self.nb1 + self.nb2 / self.nb3).standardized()
        self.answer = (self.nb1 - self.nb2 / self.nb3).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_104(self, build_data):
        self._create_variant_100(build_data)
        self.formula = '=X*p+n'
        self.setup_formula_cell1_cell2()

    def _create_variant_105(self, build_data):
        self.formula = '=X/p + n'
        self.setup_term_nb1_product_nb2_nb3()
        while self.nb2.fracdigits_nb():  # to avoid dividing by a decimal
            self.nb3 /= 10
            self.nb2 *= 10
        self.nb3 = (self.nb2 * self.nb3).standardized()
        self.nb2 = self.nb2.standardized()
        self.answer = (self.nb3 / self.nb2 + self.nb1).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_106(self, build_data):
        self.formula = '=X*p-n'
        self.setup_term_nb1_product_nb2_nb3()
        if (self.subvariant == 'only_positive'
            and self.nb1 > self.nb2 * self.nb3):
            decimals = 0
            if self.pr1_attr.get('nb_variant', '').startswith('decimal'):
                decimals = int(self.pr1_attr['nb_variant'][-1])
                maxi = self.nb2 * self.nb3 * 10 ** decimals
            else:  # the product is actually an integer
                maxi = int(self.nb2 * self.nb3)
            options = copy.deepcopy(self.st1_attr)
            options.update({'nb1_lt': maxi})
            self.nb1 = shared.mc_source.next(self.st1_source, qkw=options)[0]
            self.nb1 = Number(self.nb1).standardized()
            if self.pr1_attr.get('nb_variant', '').startswith('decimal'):
                self.nb1 = self.nb1 / (10 ** decimals)
        self.answer = (self.nb3 * self.nb2 - self.nb1).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_107(self, build_data):
        self.formula = '=X/p-n'
        self.setup_term_nb1_product_nb2_nb3()
        while self.nb2.fracdigits_nb():  # to avoid dividing by a decimal
            self.nb3 /= 10
            self.nb2 *= 10
        self.nb3 = (self.nb2 * self.nb3).standardized()
        self.nb2 = self.nb2.standardized()
        if (self.subvariant == 'only_positive'
            and self.nb1 > self.nb3 / self.nb2):
            decimals = 0
            if self.pr1_attr.get('nb_variant', '').startswith('decimal'):
                decimals = int(self.pr1_attr['nb_variant'][-1])
                maxi = (self.nb3 / self.nb2) * 10 ** decimals
            else:  # the product is actually an integer
                maxi = int(self.nb3 / self.nb2)
            options = copy.deepcopy(self.st1_attr)
            options.update({'nb1_lt': maxi})
            self.nb1 = shared.mc_source.next(self.st1_source, qkw=options)[0]
            self.nb1 = Number(self.nb1).standardized()
            if self.pr1_attr.get('nb_variant', '').startswith('decimal'):
                self.nb1 = self.nb1 / (10 ** decimals)
        self.answer = (self.nb3 / self.nb2 - self.nb1).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_108(self, build_data):
        self._create_variant_100(build_data)
        self.formula = '=n+X*p'
        self.setup_formula_cell1_cell2()

    def _create_variant_109(self, build_data):
        self._create_variant_105(build_data)
        self.formula = '=n+X/p'
        self.setup_formula_cell1_cell2()

    def _create_variant_110(self, build_data):
        self._create_variant_102(build_data)
        self.formula = '=n-X*p'
        self.setup_formula_cell1_cell2()

    def _create_variant_111(self, build_data):
        self._create_variant_105(build_data)
        self.formula = '=n-X/p'
        if (self.subvariant == 'only_positive'
            and self.nb1 < self.nb3 / self.nb2):
            self.nb1 = (self.nb1 + self.nb3 / self.nb2).standardized()
        self.answer = (self.nb1 - self.nb3 / self.nb2).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_112(self, build_data):
        self._create_variant_100(build_data)
        self.formula = '=p*X+n'
        self.setup_formula_cell1_cell2()

    def _create_variant_113(self, build_data):
        self._create_variant_101(build_data)
        self.formula = '=p/X+n'
        self.setup_formula_cell1_cell2()

    def _create_variant_114(self, build_data):
        self._create_variant_106(build_data)
        self.formula = '=p*X-n'
        self.setup_formula_cell1_cell2()

    def _create_variant_115(self, build_data):
        self.formula = '=p/X-n'
        self.setup_term_nb1_product_nb2_nb3()
        while self.nb3.fracdigits_nb():  # to avoid dividing by a decimal
            self.nb2 /= 10
            self.nb3 *= 10
        self.nb2 = (self.nb3 * self.nb2).standardized()
        self.nb3 = self.nb3.standardized()
        if (self.subvariant == 'only_positive'
            and self.nb1 > self.nb2 / self.nb3):
            decimals = 0
            if self.pr1_attr.get('nb_variant', '').startswith('decimal'):
                decimals = int(self.pr1_attr['nb_variant'][-1])
                maxi = (self.nb2 / self.nb3) * 10 ** decimals
            else:  # the product is actually an integer
                maxi = int(self.nb2 / self.nb3)
            options = copy.deepcopy(self.st1_attr)
            options.update({'nb1_lt': maxi})
            self.nb1 = shared.mc_source.next(self.st1_source, qkw=options)[0]
            self.nb1 = Number(self.nb1).standardized()
            if self.pr1_attr.get('nb_variant', '').startswith('decimal'):
                self.nb1 = self.nb1 / (10 ** decimals)
        self.answer = (self.nb2 / self.nb3 - self.nb1).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_116(self, build_data):
        self.setup_term_nb1_square_nb2_nb3()
        self.formula = '=X*X'
        self.answer = (self.nb2 * self.nb2).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_117(self, build_data):
        self.setup_term_nb1_square_nb2_nb3()
        self.formula = '=n+X*X'
        self.answer = (self.nb1 + self.nb2 * self.nb2).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_118(self, build_data):
        self.setup_term_nb1_square_nb2_nb3()
        self.formula = '=n-X*X'
        if (self.subvariant == 'only_positive'
            and self.nb1 < self.nb2 * self.nb2):
            self.nb1 = (self.nb1 + self.nb2 * self.nb2).standardized()
        self.answer = (self.nb1 - self.nb2 * self.nb2).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_119(self, build_data):
        self.setup_factor_nb1_square_nb2_nb3()
        self.formula = '=n*X*X'
        self.answer = (self.nb1 * self.nb2 * self.nb2).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_120(self, build_data):
        self.setup_divisor_nb1_square_nb2_nb3()
        self.formula = '=X*X/n'
        self.answer = (self.nb2 * self.nb2 / self.nb1).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_121(self, build_data):
        self._create_variant_117(build_data)
        self.formula = '=X*X+n'
        self.setup_formula_cell1_cell2()

    def _create_variant_122(self, build_data):
        self.formula = '=X*X-n'
        self.setup_term_nb1_square_nb2_nb3()
        if (self.subvariant == 'only_positive'
            and self.nb1 > self.nb2 * self.nb2):
            decimals = 0
            if self.sq1_attr.get('nb_variant', '').startswith('decimal'):
                decimals = int(self.sq1_attr['nb_variant'][-1])
                maxi = self.nb2 * self.nb2 * 10 ** (2 * decimals)
            else:  # the product is actually an integer
                maxi = int(self.nb2 * self.nb2)
            options = copy.deepcopy(self.st1_attr)
            options.update({'nb1_lt': maxi})
            self.nb1 = shared.mc_source.next(self.st1_source, qkw=options)[0]
            self.nb1 = Number(self.nb1).standardized()
            if self.sq1_attr.get('nb_variant', '').startswith('decimal'):
                self.nb1 = self.nb1 / (10 ** (2 * decimals))
        self.answer = (self.nb2 * self.nb2 - self.nb1).standardized()
        self.setup_formula_cell1_cell2()

    def _create_variant_123(self, build_data):
        self.setup_factor_nb1_square_nb2_nb3()
        self.formula = '=X*X*n'
        self.answer = (self.nb1 * self.nb2 * self.nb2).standardized()
        self.setup_formula_cell1_cell2()
