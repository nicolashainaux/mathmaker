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

from pathlib import Path
from decimal import Decimal

from mathmakerlib import required
from mathmakerlib.LaTeX import TikZPicture, OptionsList


class OrthogonalCoordinateSystemPicture(object):

    def __init__(self, pointxy=None, point_color='BrickRed', label='',
                 mode=None, gradoptions=None, pointoptions=None,
                 labeloptions=None, gridthickness='', axesthickness='',
                 baseline='', scale=''):
        """
        So far, this is a fixed -5 to 5 coordinate system for both axes. All
        graduations are drawn.

        pointxy is a pair of the coordinates of the possible point to draw
        in the coordinate system.
        pointoptions are used to draw the point itself (a fixed ×, so far)
        and the labeloptions to draw the point's label.
        mode is a shorcut to setup values for either 'tabular' or 'slideshow',
        it will override any value provided for gradoptions, pointoptions,
        labeloptions, *thickness, baseline and scale.
        """
        self.mode = mode
        self.point = False
        if pointxy is not None:
            self.point = True
            self.pointx, self.pointy = pointxy
            fx = Decimal('0.63') if self.pointx >= 0 else -Decimal('0.63')
            fy = Decimal('0.63') if self.pointy >= 0 else -Decimal('0.63')
            self.labelx = Decimal(self.pointx) + fx
            self.labely = Decimal(self.pointy) + fy
        self.point_color = point_color
        if self.mode == 'tabular':
            axesthickness = 'thick'
            gridthickness = 'very thin'
            baseline = '-3pt'
            scale = '0.25'
            pointoptions = {'font': r'\tiny'}
            labeloptions = {'font': r'\tiny'}
            gradoptions = {'font': r'\tiny'}
        elif self.mode == 'slideshow':
            axesthickness = 'very thick'
            gridthickness = 'thin'
            pointoptions = {'font': r'\scriptsize'}
            labeloptions = {'font': r'\scriptsize'}
            gradoptions = {'font': r'\scriptsize'}
            baseline = ''
            scale = '0.5'
        self.label = label
        self.gradoptions = gradoptions
        self.pointoptions = pointoptions
        self.labeloptions = labeloptions
        self.gridthickness = gridthickness
        self.axesthickness = axesthickness
        self.baseline = baseline
        self.scale = scale

    def __str__(self):
        required.package['tikz'] = True
        template_file = Path(__file__).parent \
            / 'templates/orthogonal_coordinate_system.tikz'
        content = template_file.read_text()
        content = content.replace('GRADOPTIONS',
                                  str(OptionsList(self.gradoptions)))
        content = content.replace('GRIDTHICKNESS', self.gridthickness)
        content = content.replace('AXESTHICKNESS', self.axesthickness)
        point = ''
        if self.point:
            point_file = Path(__file__).parent / 'templates/point.tikz'
            point = point_file.read_text()
            point = point.replace('POINTOPTIONS',
                                  str(OptionsList(self.pointoptions)))
            point = point.replace('LABELOPTIONS',
                                  str(OptionsList(self.labeloptions)))
            point = point.replace('POINTX', str(self.pointx))
            point = point.replace('POINTY', str(self.pointy))
            point = point.replace('LABELX', str(self.labelx))
            point = point.replace('LABELY', str(self.labely))
            point = point.replace('COLOR', str(self.point_color))
            point = point.replace('LABEL', str(self.label))
        content = content.replace('POINT', point)
        pic_options = []
        if self.baseline:
            pic_options.append({'baseline': self.baseline})
        if self.scale:
            pic_options.append({'scale': self.scale})
        return str(TikZPicture(content, *pic_options))
