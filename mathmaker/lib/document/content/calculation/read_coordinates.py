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

from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.LaTeX import OrthogonalCoordinateSystemPicture
from mathmaker.lib.LaTeX import SlideContent, TabularCellPictureWording


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: ('default', ) so far which is equivalent to:
        coordinates_xy, nb1_ge=-4, nb1_lt=5, nb2_ge=-4, nb2_lt=5, nb2_neq=nb1
        :type build_data: str, so far
        """
        super().setup("minimal", **options)
        if build_data == ('default', ):
            self.x, self.y = shared.coordinates_xy_source.next(
                nb1_ge='-4', nb1_lt='5', nb2_ge='-4', nb2_lt='5',
                nb2_neq='nb1')
        if self.slideshow:
            mode = 'slideshow'
        else:
            mode = 'tabular'
        self.point_label = alphabet[random.randint(1, 25)]
        self.picture = str(OrthogonalCoordinateSystemPicture(
            pointxy=(self.x, self.y), label=self.point_label, mode=mode))
        self.wording1 = _('Coordinates of point {point_name}?')\
            .format(point_name=self.point_label)
        self.transduration = 24

    def q(self, **options):
        if self.slideshow:
            output = SlideContent(wording1=self.wording1,
                                  height1='0.25pt',
                                  picture=self.picture)
        else:
            output = TabularCellPictureWording(self.picture, self.wording1)
        return str(output)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        answer = f'(${Number(self.x).printed}$; ${Number(self.y).printed}$)'
        return answer

    def js_a(self, **kwargs):
        answers = [f'({self.x};{self.y})', f'({self.x}; {self.y})',
                   f'({self.x} ; {self.y})', f'({self.x} ;{self.y})',
                   f'( {self.x};{self.y})', f'( {self.x}; {self.y})',
                   f'( {self.x} ; {self.y})', f'( {self.x} ;{self.y})',
                   f'( {self.x};{self.y} )', f'( {self.x}; {self.y} )',
                   f'( {self.x} ; {self.y} )', f'( {self.x} ;{self.y} )',
                   f'({self.x};{self.y} )', f'({self.x}; {self.y} )',
                   f'({self.x} ; {self.y} )', f'({self.x} ;{self.y} )']
        return answers
