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
        extra_deco2 = kwargs.pop('extra_deco2', None)
        subtr_shapes = kwargs.pop('subtr_shapes', False)
        thickness = kwargs.get('thickness', None)
        subvariant_nb = kwargs.get('subvariant_nb', None)
        self.check_args(distcode=codename, variant=variant, labels=labels,
                        name=name)
        labels = sorted(labels, key=lambda x: x[0])[::-1]
        return getattr(self,
                       '_' + codename)(variant=variant, labels=labels,
                                       name=name, extra_deco=extra_deco,
                                       thickness=thickness,
                                       extra_deco2=extra_deco2,
                                       subvariant_nb=subvariant_nb,
                                       subtr_shapes=subtr_shapes)

    def _anglesset(self, shapes_source, subvariants, labels, name=None,
                   extra_deco=None, subvariant_nb=None, thickness=None,
                   rdeco=None, remove_labels=None, labels_dist=None,
                   extra_deco2=None):
        # if extra_deco is None:
        #     extra_deco = {}
        if extra_deco2 is None:
            extra_deco2 = {}
        if rdeco is None:
            rdeco = []
        for deco_id in rdeco:
            if deco_id not in extra_deco:
                extra_deco[deco_id] = \
                    AngleDecoration(radius=Number('0.4', unit='cm'),
                                    label=None)
        if remove_labels is None:
            remove_labels = [False for _ in range(len(labels))]
        hatchmarks = {}
        if labels_dist is not None:
            # Then, labels_dist is a values list that tells the order of the
            # angles' measures (used if some are duplicates)
            # e.g. [0, 1, 0] means first label value, second, first again
            # Also, in that case, labels is given "raw", as list of tuples:
            # [(nb of occurences, value), ...]
            labels = [labels[k][1] for k in labels_dist][::-1]
            for k in labels_dist:
                if labels_dist.count(k) != 1 and k not in hatchmarks:
                    hatchmarks[k] = next(shared.angle_decorations_source)[0:2]
        lbls = []
        for i in range(len(remove_labels)):
            if remove_labels[i]:
                lbls.append(None)
                labels.pop()
            else:
                lbls.append(labels.pop())
        angles = []
        names = name
        if subvariant_nb is None:
            subvariant_nb = next(shapes_source)[0]
        subvariant_nb = int(subvariant_nb)
        build_data = subvariants[subvariant_nb]
        # right_angle_radius = build_data.pop('right_angle_radius', None)
        Ω = build_data.pop('center', Point(0, 0, name=names[0]))
        # Let an error be raised if no endpoints are defined
        endpoints = build_data.pop('endpoints')
        labels = [Number(lbl, unit=r'\textdegree') if lbl is not None else None
                  for lbl in lbls]
        eccentricities = build_data.pop('eccentricities',
                                        ['auto'
                                         for _ in range(len(endpoints) - 1)])
        # Setup default decorations of all i, i+1 angles
        decorations = {}
        collected_radii = {}
        layer_nb = 0
        for i in range(len(endpoints) - 1):
            r = OFFSET + layer_nb * LAYER_THICKNESS
            if labels_dist is not None:
                if labels_dist[i] in collected_radii:
                    r = collected_radii[labels_dist[i]]
                else:
                    collected_radii[labels_dist[i]] = r
                    layer_nb += 1
            else:
                layer_nb += 1
            ad = AngleDecoration(label=labels[i], radius=r,
                                 eccentricity=eccentricities[i])
            if labels_dist is not None and labels_dist[i] in hatchmarks:
                ad.variety = hatchmarks[labels_dist[i]][0]
                ad.hatchmark = hatchmarks[labels_dist[i]][1]
            decorations.update({'{}:{}'.format(i, i + 1): ad})
        for d in extra_deco:
            if d in decorations:
                decorations[d].color = extra_deco[d].color
                decorations[d].thickness = extra_deco[d].thickness
                decorations[d].label = extra_deco[d].label
                decorations[d].radius = extra_deco[d].radius
            else:
                decorations.update({d: extra_deco[d]})
        for p in endpoints:
            p.name += '1'
        for kn, key in enumerate(decorations):
            i, j = key.split(':')
            i, j = int(i), int(j)
            mark_right = True if key in rdeco else False
            armspoints = [(names[i + 1], ), (names[j + 1], )]
            θ = Angle(endpoints[i], Ω, endpoints[j],
                      decoration=decorations[key],
                      label_vertex=True, draw_vertex=True,
                      label_armspoints=True, draw_armspoints=True,
                      armspoints=armspoints, mark_right=mark_right,
                      naming_mode='from_armspoints')
            if key in extra_deco2:
                θ.decoration2 = extra_deco2[key]
            angles.append(θ)
        anglesset = AnglesSet(*angles)
        anglesset.baseline = build_data.pop('baseline', None)
        anglesset.boundingbox = build_data.pop('boundingbox', None)
        return anglesset

    def _1_1(self, variant=None, labels=None, name=None, extra_deco=None,
             subvariant_nb=None, thickness=None, extra_deco2=None,
             subtr_shapes=False):
        if variant != 0:
            raise ValueError('variant must be 0 (not \'{}\')'.format(variant))
        if extra_deco is None:
            extra_deco = {}
        subvariants = {1: {'endpoints': [Point('2.5', 0),
                                         Point(2, '1.5'),
                                         Point('0.5', '2.45')],
                           'eccentricities': [Number('1.6'), Number('1.6')],
                           'baseline': '25pt'},
                       2: {'endpoints': [Point(2, '1.5'),
                                         Point(0, '2.5'),
                                         Point('-2.3', 1)],
                           'eccentricities': [Number('1.6'), Number('1.6')],
                           'baseline': '25pt'},
                       3: {'endpoints': [Point(1, '2.3'),
                                         Point('-1.5', 2),
                                         Point('-2.5', 0)],
                           'eccentricities': [Number('1.6'), Number('1.6')],
                           'baseline': '22pt'},
                       }
        shapes_source = shared.anglessets_1_1_source
        lbls = [labels[i][1] for i in range(len(labels))]
        return self._anglesset(
            shapes_source, subvariants,
            labels=lbls, name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, extra_deco2=extra_deco2
        )

    def _1_1r(self, variant=None, labels=None, name=None, extra_deco=None,
              subvariant_nb=None, thickness=None, extra_deco2=None,
              subtr_shapes=False):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
        if extra_deco is None:
            extra_deco = {}
        lbls = [labels[i][1] for i in range(len(labels))]
        if not subtr_shapes:
            lbls.remove(90)
        if subtr_shapes:
            remove_labels = [False, False]
            rdeco = ['0:2']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point('1.5', 2),
                                             Point(0, '2.5')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '25pt'},
                           2: {'endpoints': [Point('2.29', 1),
                                             Point('1.25', '2.17'),
                                             Point(-1, '2.29')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '24pt'},
                           3: {'endpoints': [Point('0.5', '2.45'),
                                             Point('-1.8', '1.73'),
                                             Point('-2.45', '0.5')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '25pt'}}
        elif variant == 0:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [True, False]
            # /!\ order of labels: from right to left, counterclockwise
            # (reversed order of remove_labels)
            lbls = lbls + [Number(90)]
            # Tells which angles will be marked as right
            rdeco = ['0:1']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point(0, '2.5'),
                                             Point(-2, '1.5')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '25pt'},
                           2: {'endpoints': [Point('1.5', 2),
                                             Point(-2, '1.5'),
                                             Point('-2.5', 0)],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '20pt'},
                           3: {'endpoints': [Point('2.3', 1),
                                             Point(-1, '2.3'),
                                             Point('-2.45', '0.5')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '23pt'}
                           }
        elif variant == 1:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, True]
            # /!\ order of labels: from right to left, counterclockwise
            # (reversed order of remove_labels)
            lbls = [Number(90)] + lbls
            # Tells which angles will be marked as right
            rdeco = ['1:2']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point('2.3', 1),
                                             Point(-1, '2.3')],
                               'eccentricities': [Number('2.1'),
                                                  Number('1.6')],
                               'baseline': '24pt'},
                           2: {'endpoints': [Point('2.5', 0),
                                             Point(1, '2.3'),
                                             Point('-2.3', 1)],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '23pt'},
                           3: {'endpoints': [Point(2, '1.5'),
                                             Point('0.5', '2.45'),
                                             Point('-2.45', '0.5')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6')],
                               'baseline': '23pt'}
                           }
        shapes_source = shared.anglessets_1_1r_source
        return self._anglesset(
            shapes_source, subvariants,
            labels=lbls, name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, rdeco=rdeco,
            remove_labels=remove_labels, extra_deco2=extra_deco2
        )

    def _2(self, variant=None, labels=None, name=None, extra_deco=None,
           subvariant_nb=None, thickness=None, extra_deco2=None,
           subtr_shapes=False):
        if variant != 0:
            raise ValueError('variant must be 0 (not \'{}\')'.format(variant))
        lbls_dist = [0, 0]
        remove_labels = [False, True]
        if extra_deco is None:
            extra_deco = {}
        subvariants = {1: {'endpoints': [Point('2.5', 0),
                                         Point(2, '1.5'),
                                         Point('0.7', '2.4')],
                           'eccentricities': [Number('1.8'),
                                              Number('1.6')],
                           'baseline': '24pt'},
                       2: {'endpoints': [Point('2.5', 0),
                                         Point('1.5', 2),
                                         Point('-0.7', '2.4')],
                           'eccentricities': [Number('1.8'),
                                              Number('1.6')],
                           'baseline': '24pt'},
                       3: {'endpoints': [Point('1.3', '2.14'),
                                         Point(-1, '2.3'),
                                         Point('-2.45', '0.5')],
                           'eccentricities': [Number('1.7'),
                                              Number('1.6')],
                           'baseline': '23pt'},
                       }
        shapes_source = shared.anglessets_2_source
        return self._anglesset(
            shapes_source, subvariants, labels=labels, name=name,
            extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, extra_deco2=extra_deco2,
            remove_labels=remove_labels, labels_dist=lbls_dist
        )

    def _1_1_1(self, variant=None, labels=None, name=None, extra_deco=None,
               subvariant_nb=None, thickness=None, extra_deco2=None,
               subtr_shapes=False):
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
                           'baseline': '22pt'},
                       2: {'endpoints': [Point('2.5', 0),
                                         Point('1.5', 2),
                                         Point(-1, '2.3'),
                                         Point('-2.5', '0.25')],
                           'eccentricities': [Number('1.6'),
                                              Number('1.5'),
                                              Number('1.4')],
                           'baseline': '22pt'},
                       3: {'endpoints': [Point('1.6', '1.92'),
                                         Point(0, '2.5'),
                                         Point(-2, '1.5'),
                                         Point('-2.5', 0)],
                           'eccentricities': [Number('1.6'),
                                              Number('1.5'),
                                              Number('1.4')],
                           'baseline': '26pt'},
                       }
        shapes_source = shared.anglessets_1_1_1_source
        lbls = [labels[i][1] for i in range(len(labels))]
        return self._anglesset(
            shapes_source, subvariants,
            labels=lbls, name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, extra_deco2=extra_deco2
        )

    def _1_1_1r(self, variant=None, labels=None, name=None, extra_deco=None,
                subvariant_nb=None, thickness=None, extra_deco2=None,
                subtr_shapes=False):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be in [0, 1, 2] (found \'{}\')'
                             .format(variant))
        if extra_deco is None:
            extra_deco = {}
        lbls = [labels[i][1] for i in range(len(labels))]
        lbls.remove(90)
        if variant == 0:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [True, False, False]
            # /!\ order of labels: from right to left, counterclockwise
            # (reversed order of remove_labels)
            lbls = lbls + [Number(90)]
            # Tells which angles will be marked as right
            rdeco = ['0:1']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point(0, '2.5'),
                                             Point('-1.5', 2),
                                             Point('-2.4', '0.7')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.8'),
                                                  Number('1.4')],
                               'baseline': '26pt'}
                           }
        elif variant == 1:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, True, False]
            lbls = [lbls[0], Number(90), lbls[1]]
            # Tells which angles will be marked as right
            rdeco = ['1:2']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point(2, '1.5'),
                                             Point('-1.5', 2),
                                             Point('-2.4', '0.7')],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.8'),
                                                  Number('1.4')],
                               'baseline': '18pt'}
                           }
        elif variant == 2:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, False, True]
            lbls = [Number(90)] + lbls
            # Tells which angles will be marked as right
            rdeco = ['2:3']
            subvariants = {1: {'endpoints': [Point('2.45', '0.5'),
                                             Point('1.5', 2),
                                             Point(0, '2.5'),
                                             Point('-2.5', 0)],
                               'eccentricities': [Number('1.6'),
                                                  Number('1.6'),
                                                  Number('1.5')],
                               'baseline': '26pt'}
                           }
        shapes_source = shared.anglessets_1_1_1r_source
        return self._anglesset(
            shapes_source, subvariants, labels=lbls,
            name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, rdeco=rdeco,
            remove_labels=remove_labels, extra_deco2=extra_deco2
        )

    def _2_1(self, variant=None, labels=None, name=None, extra_deco=None,
             subvariant_nb=None, thickness=None, extra_deco2=None,
             subtr_shapes=False):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be in [0, 1, 2] (found \'{}\')'
                             .format(variant))
        if extra_deco is None:
            extra_deco = {}
        if variant == 0:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, True, False]
            lbls_dist = [0, 0, 1]
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point('1.93', '1.59'),
                                             Point('0.5', '2.45'),
                                             Point('-2.3', 1)],
                               'eccentricities': [Number('1.7'),
                                                  Number('1.8'),
                                                  Number('1.6')],
                               'baseline': '24pt'}
                           }
        elif variant == 1:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, False, True]
            lbls_dist = [0, 1, 0]
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point(2, '1.5'),
                                             Point(-1, '2.3'),
                                             Point('-2.2', '1.2')],
                               'eccentricities': [Number('1.7'),
                                                  Number('1.8'),
                                                  Number('1.6')],
                               'baseline': '23pt'}
                           }
        elif variant == 2:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, False, True]
            lbls_dist = [1, 0, 0]
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point('0.6', '2.43'),
                                             Point('-1.1', '2.24'),
                                             Point('-2.3', 1)],
                               'eccentricities': [Number('1.7'),
                                                  Number('1.5'),
                                                  Number('1.6')],
                               'baseline': '25pt'}
                           }
        shapes_source = shared.anglessets_2_1_source
        return self._anglesset(
            shapes_source, subvariants, labels=labels,
            name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, extra_deco2=extra_deco2,
            remove_labels=remove_labels, labels_dist=lbls_dist
        )

    def _2_1r(self, variant=None, labels=None, name=None, extra_deco=None,
              subvariant_nb=None, thickness=None, extra_deco2=None,
              subtr_shapes=False):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be in [0, 1, 2] (found \'{}\')'
                             .format(variant))
        if extra_deco is None:
            extra_deco = {}
        if variant == 0:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [True, True, False]
            lbls_dist = [1, 0, 0]
            rdeco = ['0:1']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point(0, '2.5'),
                                             Point('-1.5', 2),
                                             Point('-2.4', '0.7')],
                               'eccentricities': [Number('1.7'),
                                                  Number('1.8'),
                                                  Number('1.5')],
                               'baseline': '25pt'}
                           }
        elif variant == 1:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, True, True]
            lbls_dist = [0, 1, 0]
            rdeco = ['1:2']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point(2, '1.5'),
                                             Point('-1.5', 2),
                                             Point('-2.4', '0.7')],
                               'eccentricities': [Number('1.7'),
                                                  Number('1.8'),
                                                  Number('1.5')],
                               'baseline': '24pt'}
                           }
        elif variant == 2:
            # Tells which angles shouldn't have any label (e.g. right angles)
            remove_labels = [False, True, True]
            lbls_dist = [0, 0, 1]
            rdeco = ['2:3']
            subvariants = {1: {'endpoints': [Point('2.5', 0),
                                             Point('1.94', '1.58'),
                                             Point('0.5', '2.45'),
                                             Point('-2.45', '0.5')],
                               'eccentricities': [Number('1.7'),
                                                  Number('1.8'),
                                                  Number('1.5')],
                               'baseline': '24pt'}
                           }
        shapes_source = shared.anglessets_2_1r_source
        return self._anglesset(
            shapes_source, subvariants, labels=labels,
            name=name, extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, rdeco=rdeco,
            remove_labels=remove_labels, labels_dist=lbls_dist,
            extra_deco2=extra_deco2
        )

    def _3(self, variant=None, labels=None, name=None, extra_deco=None,
           subvariant_nb=None, thickness=None, extra_deco2=None,
           subtr_shapes=False):
        if variant != 0:
            raise ValueError('variant must be 0 (not \'{}\')'.format(variant))
        lbls_dist = [0, 0, 0]
        remove_labels = [False, True, True]
        if extra_deco is None:
            extra_deco = {}
        subvariants = {1: {'endpoints': [Point('2.5', 0),
                                         Point(2, '1.5'),
                                         Point('0.7', '2.4'),
                                         Point('-0.88', '2.34')],
                           'eccentricities': [Number('1.6'),
                                              Number('1.8'),
                                              Number('1.4')],
                           'baseline': '24pt'},
                       2: {'endpoints': [Point('2.5', 0),
                                         Point('1.5', 2),
                                         Point('-0.7', '2.4'),
                                         Point('-2.34', '0.88')],
                           'eccentricities': [Number('1.6'),
                                              Number('1.8'),
                                              Number('1.4')],
                           'baseline': '24pt'},
                       3: {'endpoints': [Point(1, '2.3'),
                                         Point('-0.61', '2.42'),
                                         Point('-1.97', '1.54'),
                                         Point('-2.5', 0)],
                           'eccentricities': [Number('1.6'),
                                              Number('1.8'),
                                              Number('1.4')],
                           'baseline': '24pt'},
                       }
        shapes_source = shared.anglessets_3_source
        return self._anglesset(
            shapes_source, subvariants, labels=labels, name=name,
            extra_deco=extra_deco, thickness=thickness,
            subvariant_nb=subvariant_nb, extra_deco2=extra_deco2,
            remove_labels=remove_labels, labels_dist=lbls_dist
        )
