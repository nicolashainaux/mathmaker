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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module gathers functions that should be run at startup.

These functions check dependencies, settings consistency and setup the
language for gettext translations.
"""

import os
import subprocess
import shlex
import gettext
from distutils.version import LooseVersion

from mathmaker import __software_name__
from mathmaker.lib.common import latex


def check_dependency(name: str, goal: str, path_to: str,
                     required_version_nb: str) -> bool:
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
    err_msg = "mathmaker requires {n} to {g}".format(n=name, g=goal)
    the_call = None
    try:
        the_call = subprocess.Popen([path_to, "--version"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
    except OSError:
        add_msg = " but the path to {n} written in mathmaker's "\
                  "config file doesn't seem to match anything.".format(n=name)
        raise EnvironmentError(err_msg + add_msg)

    if name in ['lualatex']:
        temp = shlex.split(subprocess.Popen(["grep", "Version"],
                                            stdin=the_call.stdout,
                                            stdout=subprocess.PIPE)
                                     .communicate()[0].decode())[4]
        v = temp.split(sep='-')[1]
    elif name in ['luaotfload-tool']:
        temp = shlex.split(subprocess.Popen(["grep",
                                             "luaotfload-tool version"],
                                            stdin=the_call.stdout,
                                            stdout=subprocess.PIPE)
                                     .communicate()[0].decode())[-1]
        v = temp[1:-1]
    elif name in ['msgfmt']:
        v = shlex.split(subprocess.Popen(["grep", name],
                                         stdin=the_call.stdout,
                                         stdout=subprocess.PIPE)
                                  .communicate()[0].decode())[-1]
    else:
        v = shlex.split(subprocess.Popen(["grep", "version"],
                                         stdin=the_call.stdout,
                                         stdout=subprocess.PIPE)
                        .communicate()[0].decode())[-1]

    installed_version_nb = str(v)

    if LooseVersion(installed_version_nb) < LooseVersion(required_version_nb):
        add_msg = " but the installed version number {nb1} " \
                  "is lower than expected (at least {nb2})."\
                  .format(nb1=installed_version_nb, nb2=required_version_nb)
        raise EnvironmentError(err_msg + add_msg)


def check_dependencies(euktoeps='euktoeps',
                       xmllint='xmllint',
                       lualatex='lualatex',
                       luaotfload_tool='luaotfload-tool') -> bool:
    """Will check all mathmaker's dependencies."""
    infos = ''
    missing_dependency = False
    try:
        check_dependency("euktoeps", "produce pictures",
                         euktoeps, "1.5.4")
    except EnvironmentError as e:
        infos += str(e) + '\n'
        missing_dependency = True
    try:
        check_dependency("xmllint", "read xml files",
                         xmllint, "20901")
    except EnvironmentError as e:
        infos += str(e) + '\n'
        missing_dependency = True
    try:
        check_dependency("lualatex", "compile LaTeX files",
                         lualatex, "0.76.0")
    except EnvironmentError as e:
        infos += str(e) + '\n'
        missing_dependency = True
    try:
        check_dependency("luaotfload-tool", "list the fonts available for"
                                            " lualatex",
                         luaotfload_tool, "2.4-3")
    except EnvironmentError as e:
        infos += str(e) + '\n'
        missing_dependency = True
    if missing_dependency:
        raise EnvironmentError('Some dependencies are missing or outdated. '
                               'Following message(s) have been returned:\n'
                               + infos + '\n'
                               'You will have to install the correct versions '
                               'of these dependencies in order to run '
                               'mathmaker correctly.\n')
    return True


def install_gettext_translations(**kwargs):
    """Will install output's language (gettext functions)."""
    from mathmaker import settings
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


def check_font() -> bool:
    """
    Will check if settings.font belongs to data/fonts_list.txt.

    It will first check if the exact name is in the list, then if one line
    of the list starts with the exact name.
    """
    from mathmaker import settings
    if settings.font:
        try:
            found = int(subprocess.check_output(['grep', '-c',
                                                 settings.font.lower(),
                                                 settings.fonts_list_file]))
            return found >= 1
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return False
            else:
                raise
    else:
        return True


def check_settings_consistency(language=None, od=None):
    """
    Will check the consistency of several settings values.

    The checked values are: whether the language is supported as a LaTeX
    package that mathmaker uses, the output directory (is it an existing
    directory?) and whether the chosen font is usable by lualatex.
    """
    from mathmaker.lib.tools import fonts
    from mathmaker import settings
    log = settings.mainlogger
    language = language if language is not None else settings.language
    od = od if od is not None else settings.outputdir
    font = settings.font
    # Check the chosen language belongs to latex.LANGUAGE_PACKAGE_NAME
    err_msg = 'The language chosen for output (' + language \
              + ') is not defined in the LaTeX packages known by mathmaker. '\
              'Stopping mathmaker.'
    try:
        latex.LANGUAGE_PACKAGE_NAME[language]
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
        settings.outputdir += '/'

    err_msg = 'Looks like the chosen font (' + str(font) + ') is not '\
        'in the list of available fonts for lualatex. Will try to update the '\
        'list.'
    if not check_font():
        log.warning(err_msg)
        err_msg = 'Unable to find the chosen font (' + str(font) + ') after '\
            'the update of luatex available fonts. Check if it is installed '\
            'and if you have not misspelled it.'
        fonts.create_list()
        if not check_font():
            log.critical(err_msg)
            raise ValueError(err_msg)
