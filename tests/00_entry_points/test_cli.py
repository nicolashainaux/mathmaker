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
import sys
import locale
import gettext
from unittest.mock import patch

import pytest

from mathmaker import settings
from mathmaker.core.env import USER_LOCAL_SHARE
from mathmaker.lib import shared
from mathmaker.cli import entry_point
from mathmaker import __software_name__
from mathmaker.lib.constants import LOCALE_US


def test_list():
    """Test `mathmaker list`"""
    testargs = [__software_name__, 'list']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as excinfo:
            entry_point()
        assert str(excinfo.value) == '0'


def test_old_style_sheet():
    """Test `mathmaker fraction-simplification`"""
    testargs = [__software_name__, 'fraction-simplification']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as excinfo:
            entry_point()
        assert str(excinfo.value) == '0'


def test_xml_sheet():
    """Test `mathmaker trigonometry_vocabulary`"""
    testargs = [__software_name__, 'trigonometry_vocabulary']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as excinfo:
            entry_point()
        assert str(excinfo.value) == '0'


def test_yaml_sheet():
    """Test `mathmaker 01_white1_multiplications`"""
    testargs = [__software_name__, '01_white1_multiplications']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as excinfo:
            entry_point()
        assert str(excinfo.value) == '0'


def test_unknown_directive():
    """Test `mathmaker undefined`"""
    testargs = [__software_name__, 'undefined']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as excinfo:
            entry_point()
        assert str(excinfo.value) == '1'

    # Reset settings and re-open database
    settings.init()
    settings.language = 'en'
    settings.locale = LOCALE_US
    locale.setlocale(locale.LC_ALL, settings.locale)
    gettext.translation(__software_name__,
                        settings.localedir,
                        ['en']).install()
    settings.outputdir = os.path.join(USER_LOCAL_SHARE, 'outfiles')
    os.makedirs(settings.outputdir, mode=0o770, exist_ok=True)
    shared.init()
