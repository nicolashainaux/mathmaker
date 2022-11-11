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


class SlideContent(object):

    def __init__(self, w1_size=None, wording1='', w2_size=None, wording2='',
                 height1='', height2='', picture=''):
        if w1_size is None:
            self.w1_size = r'\small'
        else:
            self.w1_size = w1_size
        self.wording1 = wording1
        if w2_size is None:
            self.w2_size = r'\footnotesize'
        else:
            self.w2_size = w2_size
        self.wording2 = wording2
        self.height1 = height1
        self.height2 = height2
        self.picture = picture

    def __str__(self):
        wording1 = ''
        if self.wording1:
            if self.w1_size:
                wording1 = r'{S W}'.replace('W', self.wording1)\
                    .replace('S', self.w1_size) + '\n'
            else:
                wording1 = f'{wording1}\n'
        wording2 = ''
        if self.wording2:
            if self.w2_size:
                wording2 = r'{S W}'.replace('W', self.wording2)\
                    .replace('S', self.w2_size) + '\n'
            else:
                wording2 = f'{wording2}\n'
        vspace1 = ''
        if self.height1:
            vspace1 = r'\par\addvspace{H}'.replace('H', self.height1) + '\n'
        vspace2 = ''
        if self.height2:
            vspace2 = r'\par\addvspace{H}'.replace('H', self.height2) + '\n'

        content = 'WORDING1VSPACE1PICTUREVSPACE2WORDING2'
        content = content.replace('WORDING1', wording1)
        content = content.replace('VSPACE1', vspace1)
        content = content.replace('WORDING2', wording2)
        content = content.replace('VSPACE2', vspace2)
        content = content.replace('PICTURE', self.picture + '\n')
        return content
