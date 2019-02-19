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

from mathmakerlib.calculus import ClockTime

from mathmaker import settings
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process

TIME_CONTEXT = {'en': {'show_0s': False},
                'fr': {'sep': 'as_si_units', 'si_show_0s': False,
                       'si_only_central': True}}

DURATION_CONTEXT = {'sep': 'as_si_units', 'si_show_0h': False,
                    'si_show_0min': False, 'si_show_0s': False}


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: tuple containing: wording's context and type, the
        wording itself and two ClockTime objects: start and arrival hours.
        :type build_data: tuple
        """
        super().setup("minimal", **options)
        wording_type = build_data[1]
        self.wording = _(build_data[2])
        lang = settings.language[:2]
        start_time = ClockTime(build_data[3], context=TIME_CONTEXT[lang])
        arrival_time = ClockTime(build_data[4], context=TIME_CONTEXT[lang])
        duration_ctxt = TIME_CONTEXT[lang] if wording_type == 'duration' \
            else DURATION_CONTEXT
        duration_time = ClockTime(arrival_time - start_time,
                                  context=duration_ctxt)
        self.start_time = start_time.printed
        self.arrival_time = arrival_time.printed
        self.duration_time = duration_time.printed
        self.solution = {'duration': duration_time,
                         'start': start_time,
                         'arrival': arrival_time}[wording_type]
        self.transduration = 24
        time_sep = {'en': ':', 'fr': 'h'}[lang]
        self.time_unit = ('', time_sep, '', '')
        setup_wording_format_of(self)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        # u = self.hint if hasattr(self, 'hint') else None
        return self.solution.printed

    def js_a(self, **kwargs):
        return [[str(self.solution.hour), str(self.solution.minute)]]
