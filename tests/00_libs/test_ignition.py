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

from mathmaker.lib.tools.ignition import (check_dependency,
                                          check_dependencies,
                                          install_gettext_translations,
                                          check_settings_consistency)


def test_check_dependency_01():
    """Checks an exception is raised if the executable doesn't exist."""
    with pytest.raises(EnvironmentError):
        check_dependency('no_such_process', 'nothing', '/no_such_process',
                         '1.0.0')


def test_check_dependency_02():
    """Checks an exception is raised if the executable's version is wrong."""
    with pytest.raises(EnvironmentError):
        check_dependency('euktoeps', 'blabla', 'euktoeps',
                         '1000.0.0')


def test_check_dependencies():
    """Checks all dependencies are correctly installed."""
    assert check_dependencies()


def test_install_gettext_translations_01():
    """Checks an exception is raised for an unsupported language."""
    with pytest.raises(EnvironmentError):
        install_gettext_translations(language='no_such_language')


def test_installgettext_translations_02():
    """Checks the supported languages are installed correctly by gettext."""
    for l in ['en', 'en_US', 'en_GB', 'fr_FR']:
        assert install_gettext_translations(language=l)
    install_gettext_translations(language='en')


def test_check_settings_consistency_01():
    """Checks an exception is raised for an unsupported language."""
    with pytest.raises(ValueError):
        check_settings_consistency(language='unsupported_language')


def test_check_settings_consistency_02():
    """Checks an exception is raised for an unvalid output directory."""
    with pytest.raises(NotADirectoryError):
        check_settings_consistency(od='/path/to/nowhere')
