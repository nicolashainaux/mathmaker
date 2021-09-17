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
from mathmaker.lib.core.base_calculus import Sum
from mathmaker.lib.core.root_calculus import Value
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
        if self.nb_source == 'clocktime_data':
            build_data = [ClockTime(b, context=TIME_CONTEXT[lang])
                          for b in list(reversed(build_data[3:]))]
            options['shuffle_nbs'] = False
        super().setup("numbers", nb=build_data, **options)
        super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 18
        if self.nb_source == 'clocktime_data':
            self.transduration = 30

        if self.subvariant == 'only_positive':
            self.nb1, self.nb2 = max(self.nb1, self.nb2), min(self.nb1,
                                                              self.nb2)
        if (options.get('nb_source', 'default').startswith('complement')
            and self.nb_variant.startswith('decimal')):
            self.nb1 //= 10
        if (options.get('nb_source', 'default').startswith('complement')
            and random.choice([True, False])):
            self.nb2 = self.nb1 - self.nb2

        if self.nb_source == 'clocktime_data':
            self.diff_str = ' - '.join([_.printed.replace('~', '', 1)
                                        for _ in self.nb_list])
            self.result = ClockTime(self.nb1 - self.nb2,
                                    context=TIME_CONTEXT[lang])
        else:
            the_diff = Sum([self.nb1, -self.nb2])
            self.diff_str = the_diff.printed
            self.result = the_diff.evaluate()

        if self.context == 'mini_problem':
            self.transduration = 25
            super().setup('mini_problem_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)
        elif self.context.startswith('complement_wording'):
            self.transduration = 12
            super().setup('complement_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)
        elif self.context == 'angles':
            self.transduration = 25
            deg = r'\textdegree'
            from mathmakerlib.geometry import AngleDecoration
            self.result = Number(self.nb1 - self.nb2)
            self.hint = deg
            required.package['xcolor'] = True
            required.options['xcolor'].add('dvipsnames')
            extra_deco = {'0:1': AngleDecoration(label='?',
                                                 thickness='ultra thick',
                                                 color='BrickRed',
                                                 radius=Number('0.5',
                                                               unit='cm')),
                          }
            extra_deco2 = {}
            if self.nb1 != 90:
                extra_deco.update({'0:2':
                                   AngleDecoration(label=None,
                                                   thickness='ultra thick',
                                                   color='NavyBlue',
                                                   radius=Number('1.6',
                                                                 unit='cm'),
                                                   eccentricity=2,
                                                   arrow_tips='<->')})
                extra_deco2.update({'1:2':
                                    AngleDecoration(label=Number(self.nb1,
                                                                 unit=deg),
                                                    do_draw=False,
                                                    color='NavyBlue',
                                                    radius=Number('1.6',
                                                                  unit='cm'))})
            else:
                extra_deco.update({'0:2':
                                   AngleDecoration(label=None,
                                                   radius=Number('0.25',
                                                                 unit='cm'))})
            super().setup('angles_bunch', extra_deco=extra_deco,
                          extra_deco2=extra_deco2,
                          labels=nndist([self.nb1, self.nb2])[::-1],
                          subvariant_nb=options.get('subvariant_nb', None),
                          variant=options.get('variant', None),
                          subtr_shapes=True)
            self.hint = r'\si{\degree}'

    def q(self, **options):
        if self.context == 'angles':
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
                 .format(math_expr=self.angles_bunch.angles[0].name,
                         q_mark=COLORED_QUESTION_MARK)])
        elif hasattr(self, 'wording'):
            return post_process(self.wording.format(**self.wording_format))
        else:
            self.substitutable_question_mark = True
            return _('{math_expr} = {q_mark}')\
                .format(
                math_expr=shared.machine.write_math_style2(self.diff_str),
                q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        v = None
        if hasattr(self, 'hint'):
            if self.nb_source == 'clocktime_data':
                v = self.result.printed.replace('~', '', 1)
            else:
                v = Value(self.result, unit=self.hint)\
                    .into_str(display_SI_unit=True)
        else:
            if self.nb_source == 'clocktime_data':
                v = self.result.printed.replace('~', '', 1)
            else:
                v = Value(self.result).into_str()
        return v

    def js_a(self, **kwargs):
        if self.nb_source == 'clocktime_data':
            return [[str(self.result.hour), str(self.result.minute)]]
        else:
            return [Value(self.result).jsprinted]
