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
import random

from mathmakerlib import required
from mathmakerlib.calculus import Number
from mathmakerlib.calculus import ClockTime

from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process
from mathmaker.lib.tools.distcode import nndist

TIME_CONTEXT = {'en': {'show_0s': False},
                'fr': {'sep': 'as_si_units', 'si_show_0s': False,
                       'si_only_central': True}}


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        lang = settings.language[:2]
        super().setup("minimal", **options)
        if self.nb_source.startswith('complement'):
            # This will add a patch for the case of 2 pairs of complements
            # (This is crap programming and should be rewritten: question
            # modules should never have to modify the numbers they're given)
            if len(build_data) == 4 and options.get('patch', None) == 'true':
                maxi, mini = max(build_data[:2]), min(build_data[:2])
                build_data = [mini, maxi - mini] + list(build_data[2:])
            # This will be OK for 2 complementary numbers among 2, 3, 4 etc.
            # numbers, the 2 complementary ones being the 2 last ones (in
            # given build_data).
            maxi, mini = max(build_data[-2:]), min(build_data[-2:])
            build_data = [mini, maxi - mini] + list(build_data[:-2])
            previous = build_data.copy()
            while build_data == previous:
                previous = build_data.copy()
                random.shuffle(build_data)
        if self.nb_source == 'clocktime_data':
            t0 = ClockTime(build_data[3], context=TIME_CONTEXT[lang])
            t1 = ClockTime(build_data[4] - build_data[3],
                           context=TIME_CONTEXT[lang])
            build_data = [t0, t1]
        super().setup("numbers", nb=build_data,
                      shuffle_nbs=(self.nb_source != 'decimalfractionssums'
                                   and not self.nb_source.startswith('compl'
                                                                     'ement')
                                   and not self.nb_source == 'clocktime_data'),
                      **options)
        super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 12
        if (self.nb_source.startswith('decimalfractionssums')
           or self.nb_source == 'clocktime_data'):
            self.transduration = 24

        # TODO: better use a Sum object (when it's available in mathmakerlib)
        self.sum_str = ' + '.join([_.printed for _ in self.nb_list])
        if self.nb_source == 'clocktime_data':
            self.sum_str = ' + '.join([_.printed.replace('~', '', 1)
                                       for _ in self.nb_list])
            self.result = ClockTime(build_data[0] + build_data[1],
                                    context=TIME_CONTEXT[lang])
        else:
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
        output = self.result.printed
        if self.nb_source == 'clocktime_data':
            output = output.replace('~', '', 1)
        return output

    def js_a(self, **kwargs):
        if self.nb_source == 'clocktime_data':
            return [[str(self.result.hour), str(self.result.minute)]]
        else:
            return [Number(self.result, unit=None).uiprinted]
