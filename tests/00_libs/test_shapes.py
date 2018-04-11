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

import pytest

from mathmaker.lib.tools.generators.shapes import ShapeGenerator


@pytest.fixture()
def SG(): return ShapeGenerator()


def test_ShapeGenerator_errors(SG):
    """Check exceptions."""
    with pytest.raises(TypeError) as excinfo:
        SG.generate()
    assert str(excinfo.value) == 'keyword argument label_vertices must be '\
        'set to True or False'
    with pytest.raises(TypeError) as excinfo:
        SG.check_args(codename_prefix=1)
    assert str(excinfo.value) == 'codename must be a str, found <class '\
        '\'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        SG.check_args(codename_prefix='1', distcode=1)
    assert str(excinfo.value) == 'distcode must be a str, found <class '\
        '\'int\'> instead.'
    with pytest.raises(ValueError) as excinfo:
        SG.generate(label_vertices=False, codename='undefined')
    assert str(excinfo.value) == 'Cannot generate \'undefined_\'.'
    with pytest.raises(TypeError) as excinfo:
        SG.generate(label_vertices=False, codename='triangle_1_1_1',
                    labels=(2, 3))
    assert str(excinfo.value) == 'labels must be a list, found <class '\
        '\'tuple\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        SG.generate(label_vertices=False, codename='triangle_1_1_1',
                    labels=[2, 3, 4])
    assert str(excinfo.value) == 'All elements of the labels list must be '\
        'tuples of two elements, first being an int.'
    with pytest.raises(TypeError) as excinfo:
        SG.generate(label_vertices=False, codename='triangle_1_1_1',
                    labels=[(2, 3), 4])
    assert str(excinfo.value) == 'All elements of the labels list must be '\
        'tuples of two elements, first being an int.'
    with pytest.raises(TypeError) as excinfo:
        SG.generate(label_vertices=False, codename='triangle_1_1_1',
                    labels=[(2, 3), ('4', 3)])
    assert str(excinfo.value) == 'All elements of the labels list must be '\
        'tuples of two elements, first being an int.'
    with pytest.raises(TypeError) as excinfo:
        SG.generate(label_vertices=False, codename='triangle_1_1_1',
                    labels=[(2, 3, 5), (4, 3)])
    assert str(excinfo.value) == 'All elements of the labels list must be '\
        'tuples of two elements, first being an int.'
    with pytest.raises(ValueError) as excinfo:
        SG.generate(label_vertices=False, codename='triangle_1_1_1',
                    labels=[(2, 4), (1, 5)])
    assert str(excinfo.value) == 'The given labels list: [(2, 4), (1, 5)]\n'\
        'does not match the distcode: 1_1_1\n'


def test_ShapeGenerator(SG):
    """Check normal use cases."""
    SG.generate(label_vertices=False, codename='pentagon_2_2_1',
                labels=[(1, 3), (2, 4), (2, 5)], variant=0)


def test_triangle_1_1_1(SG):
    """Check triangle_1_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._triangle_1_1_1()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    SG._triangle_1_1_1(variant=0, labels=[(1, 4), (1, 5), (1, 6)],
                       label_vertices=False)
    SG._triangle_1_1_1(variant=1, labels=[(1, 3), (1, 4), (1, 5)],
                       label_vertices=False)


def test_triangle_2_1(SG):
    """Check triangle_2_1 generation proceeds as expected."""
    SG._triangle_2_1(label_vertices=False, labels=[(2, 4), (1, 5)])


def test_triangle_3(SG):
    """Check triangle_3 generation proceeds as expected."""
    SG._triangle_3(label_vertices=False, labels=[(3, 4)])


def test_quadrilateral_1_1_1_1(SG):
    """Check quadrilateral_1_1_1_1 generation proceeds as expected."""
    SG._quadrilateral_1_1_1_1(labels=[(1, 4), (1, 5), (1, 6), (1, 7)],
                              label_vertices=False)


def test_quadrilateral_2_1_1(SG):
    """Check quadrilateral_2_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._quadrilateral_2_1_1()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    SG._quadrilateral_2_1_1(variant=0, labels=[(2, 4), (1, 5), (1, 6)],
                            label_vertices=False)
    SG._quadrilateral_2_1_1(variant=1, labels=[(2, 4), (1, 5), (1, 6)],
                            label_vertices=False)


def test_quadrilateral_2_2(SG):
    """Check quadrilateral_2_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._quadrilateral_2_2()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._quadrilateral_2_2(variant=0, labels=[(2, 4), (2, 5)],
                          label_vertices=False)
    SG._quadrilateral_2_2(variant=1, labels=[(2, 4), (2, 5)],
                          label_vertices=False)
    SG._quadrilateral_2_2(variant=2, labels=[(2, 4), (2, 5)],
                          label_vertices=False)


def test_quadrilateral_3_1(SG):
    """Check quadrilateral_3_1 generation proceeds as expected."""
    SG._quadrilateral_3_1(label_vertices=False, labels=[(3, 4), (1, 5)])


def test_quadrilateral_4(SG):
    """Check quadrilateral_4 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._quadrilateral_4()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    SG._quadrilateral_4(variant=0, label_vertices=False, labels=[(4, 7)])
    SG._quadrilateral_4(variant=1, label_vertices=False, labels=[(4, 7)])


def test_pentagon_1_1_1_1_1(SG):
    """Check pentagon_1_1_1_1_1 generation proceeds as expected."""
    SG._pentagon_1_1_1_1_1(label_vertices=False,
                           labels=[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)])


def test_pentagon_2_1_1_1(SG):
    """Check pentagon_2_1_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._pentagon_2_1_1_1()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    SG._pentagon_2_1_1_1(variant=0, label_vertices=False,
                         labels=[(2, 1), (1, 3), (1, 4), (1, 5)])
    SG._pentagon_2_1_1_1(variant=1, label_vertices=False,
                         labels=[(2, 1), (1, 3), (1, 4), (1, 5)])


def test_pentagon_2_2_1(SG):
    """Check pentagon_2_2_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._pentagon_2_2_1()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._pentagon_2_2_1(variant=0, label_vertices=False,
                       labels=[(2, 1), (2, 3), (1, 4)])
    SG._pentagon_2_2_1(variant=1, label_vertices=False,
                       labels=[(2, 1), (2, 3), (1, 4)])
    SG._pentagon_2_2_1(variant=2, label_vertices=False,
                       labels=[(2, 1), (2, 3), (1, 4)])


def test_pentagon_3_1_1(SG):
    """Check pentagon_3_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._pentagon_3_1_1()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    SG._pentagon_3_1_1(variant=0, label_vertices=False,
                       labels=[(3, 1), (1, 3), (1, 4)])
    SG._pentagon_3_1_1(variant=1, label_vertices=False,
                       labels=[(3, 1), (1, 3), (1, 4)])


def test_pentagon_3_2(SG):
    """Check pentagon_3_2 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._pentagon_3_2()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    SG._pentagon_3_2(variant=0, label_vertices=False,
                     labels=[(3, 1), (2, 3)])
    SG._pentagon_3_2(variant=1, label_vertices=False,
                     labels=[(3, 1), (2, 3)])


def test_pentagon_4_1(SG):
    """Check pentagon_4_1 generation proceeds as expected."""
    SG._pentagon_4_1(label_vertices=False, labels=[(4, 3), (1, 2)])


def test_pentagon_5(SG):
    """Check pentagon_5 generation proceeds as expected."""
    SG._pentagon_5(label_vertices=False, labels=[(5, 6)])


def test_hexagon_1_1_1_1_1_1(SG):
    """Check hexagon_1_1_1_1_1_1 generation proceeds as expected."""
    SG._hexagon_1_1_1_1_1_1(label_vertices=False,
                            labels=[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                                    (1, 6)])


def test_hexagon_2_1_1_1_1(SG):
    """Check hexagon_2_1_1_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_2_1_1_1_1()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._hexagon_2_1_1_1_1(variant=0, label_vertices=False,
                          labels=[(2, 1), (1, 3), (1, 4), (1, 5), (1, 6)])
    SG._hexagon_2_1_1_1_1(variant=1, label_vertices=False,
                          labels=[(2, 1), (1, 3), (1, 4), (1, 5), (1, 6)])
    SG._hexagon_2_1_1_1_1(variant=2, label_vertices=False,
                          labels=[(2, 1), (1, 3), (1, 4), (1, 5), (1, 6)])


def test_hexagon_2_2_1_1(SG):
    """Check hexagon_2_2_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_2_2_1_1()
    assert str(excinfo.value) == 'variant must be 0, 1, 2, 3, 4, 5, 6, or 7'\
        ' (not \'None\')'
    SG._hexagon_2_2_1_1(variant=0, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=1, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=2, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=3, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=4, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=5, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=6, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])
    SG._hexagon_2_2_1_1(variant=7, label_vertices=False,
                        labels=[(2, 1), (2, 3), (1, 4), (1, 5)])


def test_hexagon_2_2_2(SG):
    """Check hexagon_2_2_2 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_2_2_2()
    assert str(excinfo.value) == 'variant must be 0, 1, 2 or 3'\
        ' (not \'None\')'
    SG._hexagon_2_2_2(variant=0, label_vertices=False,
                      labels=[(2, 1), (2, 3), (2, 4)])
    SG._hexagon_2_2_2(variant=1, label_vertices=False,
                      labels=[(2, 1), (2, 3), (2, 4)])
    SG._hexagon_2_2_2(variant=2, label_vertices=False,
                      labels=[(2, 1), (2, 3), (2, 4)])
    SG._hexagon_2_2_2(variant=3, label_vertices=False,
                      labels=[(2, 1), (2, 3), (2, 4)])


def test_hexagon_3_1_1_1(SG):
    """Check hexagon_3_1_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_3_1_1_1()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2'\
        ' (not \'None\')'
    SG._hexagon_3_1_1_1(variant=0, label_vertices=False,
                        labels=[(3, 1), (1, 3), (1, 4), (1, 5)])
    SG._hexagon_3_1_1_1(variant=1, label_vertices=False,
                        labels=[(3, 1), (1, 3), (1, 4), (1, 5)])
    SG._hexagon_3_1_1_1(variant=2, label_vertices=False,
                        labels=[(3, 1), (1, 3), (1, 4), (1, 5)])


def test_hexagon_3_2_1(SG):
    """Check hexagon_3_2_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_3_2_1()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._hexagon_3_2_1(variant=0, label_vertices=False,
                      labels=[(3, 1), (2, 3), (1, 4)])
    SG._hexagon_3_2_1(variant=1, label_vertices=False,
                      labels=[(3, 1), (2, 3), (1, 4)])
    SG._hexagon_3_2_1(variant=2, label_vertices=False,
                      labels=[(3, 1), (2, 3), (1, 4)])


def test_hexagon_3_3(SG):
    """Check hexagon_3_3 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_3_3()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._hexagon_3_3(variant=0, label_vertices=False,
                    labels=[(3, 4), (3, 3)])
    SG._hexagon_3_3(variant=1, label_vertices=False,
                    labels=[(3, 4), (3, 3)])
    SG._hexagon_3_3(variant=2, label_vertices=False,
                    labels=[(3, 4), (3, 3)])


def test_hexagon_4_1_1(SG):
    """Check hexagon_4_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_4_1_1()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._hexagon_4_1_1(variant=0, label_vertices=False,
                      labels=[(4, 2), (1, 3), (1, 2), (1, 1)])
    SG._hexagon_4_1_1(variant=1, label_vertices=False,
                      labels=[(4, 2), (1, 3), (1, 2), (1, 1)])
    SG._hexagon_4_1_1(variant=2, label_vertices=False,
                      labels=[(4, 2), (1, 3), (1, 2), (1, 1)])


def test_hexagon_4_2(SG):
    """Check hexagon_4_2 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        SG._hexagon_4_2()
    assert str(excinfo.value) == 'variant must be 0, 1 or 2 (not \'None\')'
    SG._hexagon_4_2(variant=0, label_vertices=False,
                    labels=[(4, 2), (2, 3), (1, 2), (1, 1)])
    SG._hexagon_4_2(variant=1, label_vertices=False,
                    labels=[(4, 2), (2, 3), (1, 2), (1, 1)])
    SG._hexagon_4_2(variant=2, label_vertices=False,
                    labels=[(4, 2), (2, 3), (1, 2), (1, 1)])


def test_hexagon_5_1(SG):
    """Check hexagon_5_1 generation proceeds as expected."""
    SG._hexagon_5_1(label_vertices=False,
                    labels=[(5, 2), (1, 3)])


def test_hexagon_6(SG):
    """Check hexagon_6 generation proceeds as expected."""
    SG._hexagon_6(label_vertices=False, labels=[(6, 4)])
