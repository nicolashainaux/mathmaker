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

from intspan import intspan

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.frameworks import process_autofit
from mathmaker.lib.LaTeX import SlideContent

from mathmakerlib.calculus import Fraction, Number

# Possible variants (< sign may change to >; left and right numbers may be
# exchanged, only true versions are shown here)
# 0     -nn1 < -nn2
# 1     -nn1 < nn2
# 2     -fr < nn
# 3     -nn < fr
# 4     -nn -0.25|-0.5|-0.75 < -nn
# 5     -nn < -nn +0.25|+0.5|+0.75
# 6     -nn -0.1|-0.2|-0.3...|-0.9 < -nn
# 7     -nn < -nn +0.1|+0.2|+0.3...|+0.9
# 8     -nn -0.25|-0.5|-0.75 < nn
# 9     -nn < nn -0.25|-0.5|-0.75
# 10     -nn -0.1|-0.2|-0.3...|-0.9 < nn
# 11     -nn < nn -0.1|-0.2|-0.3...|-0.9


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        # Since minimal setup will be called later for each source, do not call
        # it here, it would be overriden. Save it instead.
        self.options = options
        build_data = process_autofit(build_data[0])
        variant_span = intspan(build_data['Sid']['source']
                               [len('signed_nb_comparisons:'):])
        if len(variant_span) == 1:
            self.variant_id = str(list(variant_span)[0])
        else:
            self.variant_id = shared.signed_nb_comparisons_source.next(
                nb1_in=list(variant_span))[0]
        self.setup_sources(build_data)
        self.answer = random.choice([True, False])
        getattr(self, f'_create_variant_{self.variant_id}')(build_data)
        self.answer = {True: _('True'), False: _('False')}[self.answer]
        text = _('(True, or false?)')
        sep = '\hspace{4em}'
        if self.slideshow:
            sep = r'\par'
        self.wording = f'{self.inequality}{sep}{text}'
        self.transduration = 20

    def q(self, **options):
        if self.slideshow:
            output = SlideContent(wording1=self.wording)
        else:
            output = self.wording
        return str(output)

    def a(self, **kwargs):
        # This is actually meant for self.preset == 'mental calculation'
        return str(self.answer)

    def js_a(self, **kwargs):
        return [self.answer, self.answer.lower(),
                self.answer[0], self.answer[0].lower()]

    def setup_nn1_nn2(self, build_data):
        n1 = shared.mc_source.next(self.at1_source, qkw=self.at1_attr)[0]
        n2 = shared.mc_source.next(self.at2_source, qkw=self.at2_attr)[0]
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.at1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], enforce_decimal=False,
                      standardize_decimal_numbers=True, **self.at1_attr)
        options = copy.deepcopy(self.options)
        options.update(self.at2_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2], enforce_decimal=False,
                      standardize_decimal_numbers=True, **self.at2_attr)

    def setup_nn_fr(self, build_data):
        n1 = shared.mc_source.next(self.at1_source, qkw=self.at1_attr)[0]
        n, d = shared.mc_source.next(self.sF1_source, qkw=self.sF1_attr)
        super().setup("numbers", nb=[n1, Fraction(n, d)], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.at1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], enforce_decimal=False,
                      standardize_decimal_numbers=True, **self.at1_attr)

    def setup_inequality_between_negatives(self):
        if ((self.nb1 < self.nb2 and self.answer)
            or (self.nb1 > self.nb2 and not self.answer)):
            # -nn2 < -nn1 and -nn1 > -nn2 are true|false (depending on answer)
            self.inequality = random.choice(
                [f'$-{self.nb2.printed} < -{self.nb1.printed}$',
                 f'$-{self.nb1.printed} > -{self.nb2.printed}$'])
        else:  # false
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} < -{self.nb2.printed}$',
                 f'$-{self.nb2.printed} > -{self.nb1.printed}$'])

    def setup_inequality_between_pos_and_neg(self):
        if self.answer:
            # -nn1 < nn2 and nn2 > -nn1 are always true
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} < {self.nb2.printed}$',
                 f'${self.nb2.printed} > -{self.nb1.printed}$'])
        else:  # false
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} > {self.nb2.printed}$',
                 f'${self.nb2.printed} < -{self.nb1.printed}$'])

    def _create_variant_0(self, build_data):
        self.setup_nn1_nn2(build_data)
        self.setup_inequality_between_negatives()

    def _create_variant_1(self, build_data):
        self.setup_nn1_nn2(build_data)
        if self.answer:
            # -nn1 < nn2 and nn2 > -nn1 are always true
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} < {self.nb2.printed}$',
                 f'${self.nb2.printed} > -{self.nb1.printed}$'])
        else:  # false
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} > {self.nb2.printed}$',
                 f'${self.nb2.printed} < -{self.nb1.printed}$'])

    def _create_variant_2(self, build_data):
        self.setup_nn_fr(build_data)
        if self.answer:
            # -nn < fr and fr > -nn are always true
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} < {self.nb2.printed}$',
                 f'${self.nb2.printed} > -{self.nb1.printed}$'])
        else:  # false
            self.inequality = random.choice(
                [f'$-{self.nb1.printed} > {self.nb2.printed}$',
                 f'${self.nb2.printed} < -{self.nb1.printed}$'])

    def _create_variant_3(self, build_data):
        self.setup_nn_fr(build_data)
        if self.answer:
            # -nn < fr and fr > -nn are always true
            self.inequality = random.choice(
                [f'$-{self.nb2.printed} < {self.nb1.printed}$',
                 f'${self.nb1.printed} > -{self.nb2.printed}$'])
        else:  # false
            self.inequality = random.choice(
                [f'$-{self.nb2.printed} > {self.nb1.printed}$',
                 f'${self.nb1.printed} < -{self.nb2.printed}$'])

    def _create_variant_4(self, build_data):
        super().setup("minimal", **self.options)
        n2 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n1 = n2 - Number(random.choice(['0.25', '0.5', '0.75']))
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_negatives()

    def _create_variant_5(self, build_data):
        super().setup("minimal", **self.options)
        n1 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n2 = n1 + Number(random.choice(['0.25', '0.5', '0.75']))
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_negatives()

    def _create_variant_6(self, build_data):
        super().setup("minimal", **self.options)
        n2 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n1 = n2 - Number(random.randint(1, 9)) / 10
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_negatives()

    def _create_variant_7(self, build_data):
        super().setup("minimal", **self.options)
        n1 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n2 = n1 + Number(random.randint(1, 9)) / 10
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_negatives()

    def _create_variant_8(self, build_data):
        super().setup("minimal", **self.options)
        n2 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n1 = n2 - Number(random.choice(['0.25', '0.5', '0.75']))
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_pos_and_neg()

    def _create_variant_9(self, build_data):
        super().setup("minimal", **self.options)
        n1 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n2 = n1 - Number(random.choice(['0.25', '0.5', '0.75']))
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_pos_and_neg()

    def _create_variant_10(self, build_data):
        super().setup("minimal", **self.options)
        n2 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n1 = n2 + Number(random.randint(1, 9)) / 10
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_pos_and_neg()

    def _create_variant_11(self, build_data):
        super().setup("minimal", **self.options)
        n1 = Number(shared.mc_source.next(self.at1_source,
                                          qkw=self.at1_attr)[0])
        n2 = n1 - Number(random.randint(1, 9)) / 10
        super().setup("numbers", nb=[n1, n2], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        self.setup_inequality_between_pos_and_neg()
