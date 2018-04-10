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

import os

from mathmakerlib import required
from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process
from mathmaker.lib.tools.distcode import nndist


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        if self.nb_source.startswith('complement'):
            maxi, mini = max(build_data), min(build_data)
            build_data = [mini, maxi - mini]
        super().setup("numbers", nb=build_data,
                      shuffle_nbs=(self.nb_source != 'decimalfractionssums'),
                      **options)
        super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 8
        if (self.nb1 > 20 and self.nb2 > 20
            and not self.nb1 % 10 == 0 and not self.nb2 % 10 == 0):
            self.transduration = 12
        if self.nb_source.startswith('decimalfractionssums'):
            self.transduration = 15

        # TODO: better use a Sum object (when it's available in mathmakerlib)
        self.sum_str = ' + '.join([_.printed for _ in self.nb_list])
        self.result = sum([_.evaluate() for _ in self.nb_list])

        if self.context == 'mini_problem':
            self.transduration = 25
            super().setup('mini_problem_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)
        elif self.context.startswith('ask:'):
            super().setup('ask_question',
                          q_key=self.context.split(sep=':')[1],
                          values=[
                              shared.machine.write_math_style2(self.sum_str)],
                          fix_math_style2_fontsize=True)
        elif self.context == 'angles':
            self.transduration = 25
            deg = r'\textdegree'
            from mathmakerlib.geometry import AngleDecoration
            self.result = Number(self.result, unit=deg)
            required.package['xcolor'] = True
            required.options['xcolor'].add('dvipsnames')
            extra_deco = {'0:{}'.format(self.nb_nb):
                          AngleDecoration(label=None,
                                          thickness='ultra thick',
                                          color='BrickRed')}
            super().setup('angles_bunch', extra_deco=extra_deco,
                          labels=nndist(self.nb_list),
                          subvariant_nb=options.get('subvariant_nb', None),
                          variant=options.get('variant', None))
            self.hint = r'\si{\degree}'
            # if not self.slideshow:
            #     self.angles_bunch.baseline = '20pt'

    def q(self, **options):
        if self.context == 'mini_problem':
            return post_process(self.wording.format(**self.wording_format))
        elif self.context.startswith('ask:'):
            return self.wording
        elif self.context == 'angles':
            if self.slideshow:
                col_widths = [6, 7]
            else:
                col_widths = [8.25, 4.75]
            self.substitutable_question_mark = True
            return shared.machine.write_layout(
                (1, 2),
                col_widths,
                [self.angles_bunch.drawn,
                 _('${math_expr}$ = {q_mark}')
                 .format(math_expr=self.angles_bunch.angles[-1].name,
                         q_mark=COLORED_QUESTION_MARK)])
        else:
            self.substitutable_question_mark = True
            return shared.machine.write_math_style2(
                _('{math_expr} = {q_mark}')
                .format(math_expr=self.sum_str, q_mark=COLORED_QUESTION_MARK))

    def a(self, **options):
        return self.result.printed

    def js_a(self, **kwargs):
        return [Number(self.result, unit=None).uiprinted]
