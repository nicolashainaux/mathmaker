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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  US

import os
import gettext
import locale

import mathmakerlib.config

from mathmaker import __software_name__
from mathmaker.core.env import USER_LOCAL_SHARE
from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.constants import LOCALE_US
from mathmaker.lib.tools.ignition import check_dependencies
settings.init()
check_dependencies(euktoeps=settings.euktoeps,
                   xmllint=settings.xmllint,
                   lualatex=settings.lualatex,
                   luaotfload_tool=settings.luaotfload_tool)
settings.language = 'en'
settings.locale = LOCALE_US
locale.setlocale(locale.LC_ALL, settings.locale)
gettext.translation(__software_name__, settings.localedir, ['en']).install()
settings.outputdir = os.path.join(USER_LOCAL_SHARE, 'outfiles')
os.makedirs(settings.outputdir, mode=0o770, exist_ok=True)
mathmakerlib.config.PolygonsSetup.ENABLE_MISMATCH_WINDING_WARNING = False
shared.init()
