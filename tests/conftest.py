# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

from mathmaker import __software_name__
from mathmaker import settings
from mathmaker.lib import shared
settings.init()
settings.language = 'en'
settings.locale = 'en_US.UTF-8'
locale.setlocale(locale.LC_ALL, settings.locale)
gettext.translation(__software_name__, settings.localedir, ['en']).install()
settings.outputdir = settings.projectdir + 'outfiles/'
if not os.path.isdir(settings.outputdir):
    os.mkdir(settings.outputdir, mode=0o777)
shared.init()
