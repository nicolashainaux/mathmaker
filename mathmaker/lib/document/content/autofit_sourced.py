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

from intspan import intspan

from mathmaker.lib import shared
from mathmaker.lib.tools import divisors


class AutofitSourced(object):

    def setup_term_nb1_product_nb2_nb3(self):
        n = shared.mc_source.next(self.at1_source, qkw=self.at1_attr)[0]
        p, val = shared.mc_source.next(self.pr1_source, qkw=self.pr1_attr)
        # self.nb1 = n; self.nb2 = p; self.nb3 = val (X)
        super().setup("numbers", nb=[n, p, val], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.at1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], **self.at1_attr)
        options = copy.deepcopy(self.options)
        options.update(self.pr1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[2, 3], **self.pr1_attr)

    def setup_term_nb1_square_nb2_nb3(self):
        n = shared.mc_source.next(self.at1_source, qkw=self.at1_attr)[0]
        p, v = shared.mc_source.next(self.sq1_source, qkw=self.sq1_attr)
        # self.nb1 = n; self.nb2 = self.nb3 = val (X)
        super().setup("numbers", nb=[n, p, v], shuffle_nbs=False,
                      standardize_decimal_numbers=True)
        options = copy.deepcopy(self.options)
        options.update(self.at1_attr)
        super().setup("minimal", **options)
        super().setup("nb_variants", included=[1], **self.at1_attr)
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
