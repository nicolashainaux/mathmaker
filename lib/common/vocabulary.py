# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import gettext, os, sys
from lib import error
from lib.common import software
from lib.common import default
from lib.common.cst import *

pathname = os.path.dirname(sys.argv[0])
localdir = os.path.abspath(pathname) + "/locale"

try:
    gettext.translation(software.NAME,
                        localdir,
                        [default.LANGUAGE]).install()
except IOError as msg:
    error.write_warning("gettext returned the following message:\n" \
                        + str(msg) + "\n" \
                        + "It means the language indicated either \
in the command line or read from the configuration file isn't available yet \
in {software_ref} which will try to produce output in the language of your \
system.".format(software_ref=software.NAME) + "\n" )
    try:
        gettext.install(software.NAME,
                        localdir)
    except IOError as msg:
        error.write_warning("gettext returned the following message:\n" \
                        + str(msg) + "\n" \
                        + "It means the language of your system isn't \
available yet in {software_ref} which will produce output in \
english. If this results in producing an error, then your installation isn't \
complete.".format(software_ref=software.NAME) + "\n")
        gettext.translation(software.NAME,
                            localdir,
                            ['en']).install()


PRECISION_IDIOMS = { UNIT: _("to the unit"),
                     TENTH: _("to the tenth"),
                     HUNDREDTH: _("to the hundreth"),
                     THOUSANDTH: _("to the thousandth"),
                     TEN_THOUSANDTH: _("to the ten thousandth")
                   }
