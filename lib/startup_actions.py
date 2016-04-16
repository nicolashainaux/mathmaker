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
from distutils.version import LooseVersion

from lib.common.settings import CONFIG

##
#   @brief  Will check if a dependency is installed plus its version number.
#           The version number is supposed to be displayed at the end of first
#           line when calling `executable --version` (or the equivalent)
#   @param  name    The name of the executable to test
#   @param  goal    A string telling shortly why mathmaker needs it
#   @param  path_to The path to the executable to test
#   @param  version_option  Usually it's --version or -v
#   @param  required_version_nb A string containing the required version number
def check_dependency(name, goal, path_to, version_option, required_version_nb):
    ERR_MSG = "mathmaker requires {n} to {g}".format(n=name,
                                                     g=goal)
    the_call = None
    try:
        the_call = subprocess.Popen([path_to, "--version"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
    except OSError:
        sys.stderr.write(ERR_MSG \
                         + " but the path to {n} " \
                         "written in mathmaker's config file " \
                         "doesn't seem to match anything.\n"\
                         .format(n=name))
        sys.exit(2)

    v = shlex.split(subprocess.Popen(["grep", "version"],
                                     stdin=the_call.stdout,
                                     stdout=subprocess.PIPE)\
                                    .communicate()[0].decode())[-1]

    installed_version_nb = str(v)

    if LooseVersion(installed_version_nb) <  LooseVersion(required_version_nb):
        sys.stderr.write(ERR_MSG \
                         + " but the installed version number {nb1} " \
                         "is lower than expected (at least {nb2}).\n" \
                         .format(nb1=installed_version_nb,
                                 nb2=required_version_nb))
        sys.exit(2)

##
#   @brief  Will check all mathmaker's dependencies.
def check_dependencies():
    check_dependency("euktoeps", "produce pictures",
                     CONFIG["PATHS"]["EUKTOEPS"], "-v",
                     "1.5.4")
    check_dependency("xmllint", "read xml files",
                     CONFIG["PATHS"]["XMLLINT"], "--version",
                     "20901")


