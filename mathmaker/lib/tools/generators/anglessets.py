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

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Angle, AnglesSet, AngleDecoration, Point

from mathmaker.lib import shared
from mathmaker.lib.tools.generators import Generator

OFFSET = Number('0.6', unit='cm')
LAYER_THICKNESS = Number('0.1', unit='cm')


class AnglesSetGenerator(Generator):

    def generate(self, codename=None, variant=None, labels=None, name=None,
                 **kwargs):
        """
        :param codename: the distcode, describing the type of anglesset and
        the measures distribution, grouped by equal measures batches, like
        1_1_1, 3_2 etc. The letter 'r' may be suffixed to the distcode, then it
        concerns a series of variants containing one right angle.
        :type codename: str
        :param variant: the variant number
        :type variant: int
        :param labels: the labels to set, in the form of a list of couples
        (nb_of_measures, measure). This list will be checked at start.
        :type labels: list (of couples)
        :param name: the series of letters to use to name the AnglesSet's
        Points
        :type name: str (or None, then it will be set automatically)
        """
        extra_deco = kwargs.pop('extra_deco', None)
        thickness = kwargs.get('thickness', None)
        self.check_args(distcode=codename, variant=variant, labels=labels,
                        name=name)
        return getattr(self,
                       '_' + codename)(variant=variant, labels=labels,
                                       name=name, extra_deco=extra_deco,
                                       thickness=thickness)

    def _anglesset(self, shapes_source, subvariants, labels, name=None,
                   extra_deco=None, subvariant_nb=None, thickness=None):
        angles = []
        names = name
        if subvariant_nb is None:
            subvariant_nb = next(shapes_source)[0]
        build_data = subvariants[subvariant_nb]
        # right_angle_radius = build_data.pop('right_angle_radius', None)
        Ω = build_data.pop('center', Point(0, 0, name=names[0]))
        # Let an error be raised if no endpoints are defined
        endpoints = build_data.pop('endpoints')
        labels = [Number(lbl, unit=r'\textdegree') for lbl in labels]
        eccentricities = build_data.pop('eccentricities',
                                        ['automatic'
                                         for _ in range(len(endpoints) - 1)])
        # Setup default decorations of all i, i+1 angles
        decorations = {'{}:{}'.format(i, i + 1):
                       AngleDecoration(label=labels[i],
                                       radius=OFFSET + i * LAYER_THICKNESS,
                                       eccentricity=eccentricities[i])
                       for i in range(len(endpoints) - 1)}
        for d in extra_deco:
            if d in decorations:
                decorations[d].color = extra_deco[d].color
                decorations[d].thickness = extra_deco[d].thickness
                decorations[d].label = extra_deco[d].label
            else:
                decorations.update({d: extra_deco[d]})
        for p in endpoints:
            p.name += '1'
        for kn, key in enumerate(decorations):
            i, j = key.split(':')
            i, j = int(i), int(j)
            armspoints = [(names[i + 1], ), (names[j + 1], )]
            angles.append(Angle(endpoints[i], Ω, endpoints[j],
                                decoration=decorations[key],
                                label_vertex=True, draw_vertex=True,
                                label_armspoints=True, draw_armspoints=True,
                                armspoints=armspoints,
                                naming_mode='from_armspoints'))
        anglesset = AnglesSet(*angles)
        anglesset.baseline = build_data.pop('baseline', None)
        anglesset.boundingbox = build_data.pop('boundingbox', None)
        return anglesset

    def _1_1_1(self, variant=None, labels=None, name=None, extra_deco=None,
               subvariant_nb=None, thickness=None):
        if variant != 0:
            raise ValueError('variant must be 0 (not \'{}\')'.format(variant))
        if extra_deco is None:
            extra_deco = {}
        subvariants = {1: {'endpoints': [Point('2.5', 0),
                                         Point(2, '1.5'),
                                         Point(1, '2.3'),
                                         Point(-2, '1.5')],
                           'eccentricities': [Number('1.6'),
                                              Number('1.8'),
                                              Number('1.4')],
                           'baseline': '22pt'}
                       }
        shapes_source = shared.anglessets_1_1_1_source
        lbls = [labels[i][1] for i in range(len(labels))]
        return self._anglesset(
            shapes_source, subvariants,
            labels=lbls, name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb
        )
