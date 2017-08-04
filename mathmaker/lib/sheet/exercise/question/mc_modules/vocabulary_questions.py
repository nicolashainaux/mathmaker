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

# This module will add a question about the sum of two numbers

from mathmaker.lib.core.root_calculus import Value
from .. import submodule
from mathmaker.lib.tools.wording import setup_wording_format_of


class structure(submodule.structure):

    def __init__(self, nbs_to_use, **kwargs):
        result_fct = kwargs.pop('result_fct', None)
        wording = kwargs.pop('wording', "")
        super().setup("minimal", **kwargs)
        super().setup("numbers", nb=nbs_to_use, **kwargs)
        super().setup("nb_variants", nb=nbs_to_use, **kwargs)
        self.result = Value(result_fct(self.nb1, self.nb2)
                            .evaluate()).into_str()
        if 'swap_nb1_nb2' in kwargs and kwargs['swap_nb1_nb2']:
            self.nb1, self.nb2 = self.nb2, self.nb1
        if ('permute_nb1_nb2_result' in kwargs
            and kwargs['permute_nb1_nb2_result']):
            # __
            self.nb1, self.nb2, self.result = self.result, self.nb1, self.nb2
        self.nb1 = Value(self.nb1)
        self.nb2 = Value(self.nb2)
        self.wording = wording
        setup_wording_format_of(self)

    def q(self, **kwargs):
        return self.wording.format(**self.wording_format)

    def a(self, **kwargs):
        return str(self.result)
