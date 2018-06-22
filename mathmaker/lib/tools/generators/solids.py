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

import mathmakerlib.config as mmlib_cfg
from mathmakerlib.geometry import RightCuboid, ObliqueProjection

from mathmaker.lib.tools.generators import Generator


class SolidGenerator(Generator):

    def generate(self, codename=None, variant=None, labels=None, name=None,
                 **kwargs):
        """
        Possible kwargs: direction, thickness, label_vertices

        :param codename: the type of solid (rightcuboid...)
        :type codename: str
        :param variant: the variant number
        :type variant: int
        :param labels: the labels to set, in the form of a list that can be
        used by the setup_labels() method of the solid.
        :type labels: list
        :param name: the series of letters to use to name the Solid
        :type name: str (or None, then it will be set automatically)
        """
        return getattr(self, '_' + codename)(variant, labels, name, **kwargs)

    def _rightcuboid(self, variant, labels, name, **kwargs):
        RECEDING_ANGLE = mmlib_cfg.oblique_projection.RECEDING_AXIS_ANGLE
        # dimensions are: width, height, depth
        build_data = {0: {'dimensions': (2.5, 0.5, 1), 'α': 60,
                          'boundingbox': (-0.2, -0.5, 1.05, 1.05)},
                      1: {'dimensions': (0.5, 0.8, 1.3), 'α': 70,
                          'baseline': '12pt',
                          'boundingbox': (-0.2, -0.5, 1, 1.2)},
                      2: {'dimensions': (0.5, 0.6, 1.4), 'α': 60,
                          'baseline': '11pt',
                          'boundingbox': (-0.2, -0.6, 1, 1.2)},
                      3: {'dimensions': (2, 1, 0.5),
                          'baseline': '13pt',
                          'boundingbox': (-0.2, -0.5, 1, 1.35)},
                      4: {'dimensions': (0.75, 1.25, 0.5),
                          'baseline': '16pt',
                          'boundingbox': (-0.2, -0.5, 1, 1.65)},
                      5: {'dimensions': (1, 0.5, 1.25), 'α': 70,
                          'baseline': '8pt',
                          'boundingbox': (-0.2, -0.5, 1, 0.9)}
                      }[variant]
        rc = RightCuboid(dimensions=build_data['dimensions'], name=name,
                         thickness=kwargs.get('thickness', 'thick'))
        rc.setup_labels(labels)
        label_vertices = kwargs.get('label_vertices', False)
        direction = kwargs.get('direction', 'top-right')
        op = ObliqueProjection(rc, direction=direction,
                               α=build_data.get('α', RECEDING_ANGLE),
                               label_vertices=label_vertices)
        op.baseline = build_data.get('baseline', '10pt')
        op.boundingbox = build_data.pop('boundingbox', None)
        return rc, op
