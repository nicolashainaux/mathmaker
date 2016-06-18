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

import os
import subprocess
import shlex
import gettext
from distutils.version import LooseVersion

from mathmaker import settings
from lib import __software_name__
from lib.common import latex


def check_dependency(name, goal, path_to, required_version_nb):
    """
    Will check if a dependency is installed plus its version number.

    The version number is supposed to be displayed at the end of the
    line containing 'version' when calling `executable --version`
    (or the equivalent).
    :param name: the dependency's name.
    :type name: str
    :param goal: tells shortly why mathmaker needs it for
    :type goal: str
    :param path_to: the path to the executable to test
    :type path_to: str
    :param required_version_nb: well, the required version number
    :type required_version_nb: str
    :rtype: bool
    """
    log = settings.mainlogger
    err_msg = "mathmaker requires {n} to {g}".format(n=name, g=goal)
    the_call = None
    try:
        the_call = subprocess.Popen([path_to, "--version"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
    except OSError:
        add_msg = " but the path to {n} written in mathmaker's "\
                  "config file doesn't seem to match anything.".format(n=name)
        log.error(err_msg + add_msg)
        raise EnvironmentError(err_msg + add_msg)

    v = shlex.split(subprocess.Popen(["grep", "version"],
                                     stdin=the_call.stdout,
                                     stdout=subprocess.PIPE)\
                                    .communicate()[0].decode())[-1]

    installed_version_nb = str(v)

    if LooseVersion(installed_version_nb) < LooseVersion(required_version_nb):
        add_msg = " but the installed version number {nb1} " \
                  "is lower than expected (at least {nb2})."\
                  .format(nb1=installed_version_nb, nb2=required_version_nb)
        log.error(err_msg + add_msg)
        raise EnvironmentError(err_msg + add_msg)

    return True


def check_dependencies():
    """Will check all mathmaker's dependencies."""
    return (check_dependency("euktoeps", "produce pictures",
                            settings.euktoeps, "1.5.4")
            and check_dependency("xmllint", "read xml files",
                                 settings.xmllint, "20901"))


def install_gettext_translations(**kwargs):
    """Will install output's language (gettext functions)"""
    log = settings.mainlogger
    language = kwargs.get('language', settings.language)
    err_msg = 'gettext returned the following message:"{gettext_msg}"'\
              '. It means the desired language ({l}) isn\'t available yet '\
              'in mathmaker. Can\'t continue. Stopping mathmaker.'
    try:
        gettext.translation(__software_name__,
                            settings.localedir,
                            [language]).install()
        settings.language = language
    except IOError as msg:
        log.critical(err_msg.format(gettext_msg=msg, l=language))
        raise EnvironmentError(err_msg.format(gettext_msg=msg, l=language))
    return True


def check_settings_consistency(**kwargs):
    """
    Will check the consistency of several settings values.

    :param language: language to use. Should be settings.language.
    :type language: str
    :param od: output directory. Shouldn't be else than settings.outputdir
    :type od: str
    """
    log = settings.mainlogger
    language = kwargs.get('language', settings.language)
    od = kwargs.get('od', settings.outputdir)
    # Check the chosen language belongs to latex.LANGUAGE_PACKAGE_NAME
    err_msg = 'The language chosen for output (' + language \
              + ') is not defined in the LaTeX packages known by mathmaker. '\
              'Stopping mathmaker.'
    try:
        dummy = latex.LANGUAGE_PACKAGE_NAME[language]
    except KeyError:
        log.critical(err_msg, exc_info=True)
        raise ValueError(err_msg)

    err_msg = 'The output directory (' + str(od) \
              + ') is not valid. Stopping mathmaker.'
    if not os.path.isdir(od):
        log.critical(err_msg)
        raise NotADirectoryError(err_msg)
    # We need to modify settings.outputdir directly, so no use of od kw
    elif not settings.outputdir.endswith('/'):
        log.warning('The output directory is correct but should end '
                    'with a /. Correcting it.')
        settings.outputdir += '/'
