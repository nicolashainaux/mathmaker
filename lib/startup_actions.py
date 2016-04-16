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

import sys, subprocess, shlex

from lib.common.settings import CONFIG

def check_xmllint():
	pass

def check_euktoeps():
    EUKTOEPS_ERR_MSG = "mathmaker requires euktoeps to produce pictures"
    EUKTOEPS_VERSION_ERR_MSG = " but euktoeps did not return the correct "\
                               "version information"

    path_to_euktoeps = CONFIG["PATHS"]["EUKTOEPS"]
    call_euktoeps = None

    try:
        call_euktoeps = subprocess.Popen([path_to_euktoeps, "-v"],
                                          stdout=subprocess.PIPE)
    except OSError:
        sys.stderr.write(EUKTOEPS_ERR_MSG \
                         + " but the path to euktoeps " \
                         + "written in mathmaker's config file " \
                         + "doesn't seem to match anything.\n")
        sys.exit(2)

    check_euktoeps = shlex.split(subprocess.Popen(["grep", "version"],
                                                  stdin=call_euktoeps.stdout,
                                                  stdout=subprocess.PIPE)\
                                                 .communicate()[0].decode()
                                )

    if not len(check_euktoeps) == 3:
        sys.stderr.write(EUKTOEPS_ERR_MSG + EUKTOEPS_VERSION_ERR_MSG + ".\n")
        sys.exit(2)

    if not check_euktoeps[0] == "Euktoeps":
        sys.stderr.write(  EUKTOEPS_ERR_MSG \
                         + EUKTOEPS_VERSION_ERR_MSG \
                         + " (name was not 'Euktoeps').\n")
        sys.exit(2)

    if not check_euktoeps[1] == "version":
        sys.stderr.write(  EUKTOEPS_ERR_MSG \
                         + EUKTOEPS_VERSION_ERR_MSG \
                         + " (the 'version' word was absent).\n")
        sys.exit(2)

    if not len(check_euktoeps[2]) == 5:
        sys.stderr.write(  EUKTOEPS_ERR_MSG \
                         + EUKTOEPS_VERSION_ERR_MSG \
                         + " (the version number seems incorrect).\n")
        sys.exit(2)

    if not check_euktoeps[2][0:3] == "1.5":
        sys.stderr.write(  EUKTOEPS_ERR_MSG \
                         + EUKTOEPS_VERSION_ERR_MSG \
                         + " (version number should begin with '1.5').\n")
        sys.exit(2)

    if not int(check_euktoeps[2][4]) >= 4:
        sys.stderr.write(  EUKTOEPS_ERR_MSG \
                         + EUKTOEPS_VERSION_ERR_MSG \
                         + " (version number should be at least 1.5.4).\n")
        sys.exit(2)


def check_dependencies():
    check_xmllint()
    check_euktoeps()


