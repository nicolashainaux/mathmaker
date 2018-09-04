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

"""
This module gathers functions that should be run at startup.

These functions check dependencies, settings consistency and setup the
language for gettext translations.
"""

import os
import shlex
import gettext
import warnings
import subprocess
from tempfile import TemporaryFile
from distutils.version import LooseVersion

from mathmaker import __software_name__
from mathmaker.lib.constants import latex


def retrieve_fonts(fonts_list_file='mathmaker/data/fonts_list.txt',
                   datadir='mathmaker/data',
                   force=False) -> tuple:
    """
    Store in a file the list of the fonts available for lualatex.
    """
    if force:
        return []
    with TemporaryFile() as tmp_file:
        p = subprocess.Popen('luaotfload-tool --list "*"',
                             shell=True,
                             stdout=tmp_file)
        p.wait()
        tmp_file.seek(0)
        with open(fonts_list_file, mode='wt') as f:
            for line in tmp_file.readlines():
                if not line.startswith(b'luaotfload') and line[:-1]:
                    f.write(line.decode('utf-8').lower())
    return [(datadir, [fonts_list_file])]


def warning_msg(name: str, path_to: str, c_out: str, c_err: str,
                gkw: str, g_out: str, g_err: str):
    """
    Return the formatted warning message.

    :param name: name of the software
    :param path_to: the path to the software
    :param c_out: output of the call to `software --version`
    :param c_err: error output of the call to `software --version`
    :param gkw: keyword used to grep the version from output
    :param g_out: output of the call to `grep...`
    :param g_err: error output of the call to `grep...`
    """
    return 'Could not check the version of ' + name + '.\n'\
        '`' + str(path_to) + ' --version` returned:\n'\
        '  > OUT: ' + str(c_out) + '\n'\
        '  > ERR: ' + str(c_err) + '\n'\
        'Trying to `grep ' + str(gkw) + '` on OUT returned:\n'\
        '  > OUT: ' + str(g_out) + '\n'\
        '  > ERR: ' + str(g_err) + '\n'


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
    the_call = the_call_out = the_call_err = None
    try:
        the_call = subprocess.Popen([path_to, '--version'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        the_call_out, the_call_err = \
            subprocess.Popen([path_to, '--version'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT).communicate()
    except OSError:
        add_msg = " but the path to {n} written in mathmaker's "\
                  "config file doesn't seem to match anything.".format(n=name)
        raise EnvironmentError(err_msg + add_msg)

    if name in ['lualatex']:
        from mathmaker import settings
        try:
            grep_out, grep_err = subprocess.Popen(['grep', 'Version'],
                                                  stdin=the_call.stdout,
                                                  stdout=subprocess.PIPE)\
                .communicate()
            temp = shlex.split(grep_out.decode())[4]
            if len(temp.split(sep='-')) >= 2:
                v = temp.split(sep='-')[1]
            else:
                v = temp
            settings.luatex_version = str(v)
        except IndexError:
            warnings.warn(warning_msg(name=name, path_to=path_to,
                                      c_out=the_call_out, c_err=the_call_err,
                                      gkw='Version',
                                      g_out=grep_out, g_err=grep_err))
    elif name in ['luaotfload-tool']:
        try:
            grep_out, grep_err = subprocess.Popen(['grep',
                                                   'luaotfload-tool version'],
                                                  stdin=the_call.stdout,
                                                  stdout=subprocess.PIPE)\
                .communicate()
            temp = grep_out.decode().split()[-1]
            v = temp[1:-1]
        except IndexError:
            warnings.warn(warning_msg(name=name, path_to=path_to,
                                      c_out=the_call_out, c_err=the_call_err,
                                      gkw='luaotfload-tool version',
                                      g_out=grep_out, g_err=grep_err))
    elif name in ['msgfmt']:
        try:
            grep_out, grep_err = subprocess.Popen(['grep', name],
                                                  stdin=the_call.stdout,
                                                  stdout=subprocess.PIPE)\
                .communicate()
            v = shlex.split(grep_out.decode())[-1]
        except IndexError:
            warnings.warn(warning_msg(name=name, path_to=path_to,
                                      c_out=the_call_out, c_err=the_call_err,
                                      gkw=name,
                                      g_out=grep_out, g_err=grep_err))
    else:
        try:
            grep_out, grep_err = subprocess.Popen(['grep', 'version'],
                                                  stdin=the_call.stdout,
                                                  stdout=subprocess.PIPE)\
                .communicate()
            v = shlex.split(grep_out.decode())[-1]
        except IndexError:
            warnings.warn(warning_msg(name=name, path_to=path_to,
                                      c_out=the_call_out, c_err=the_call_err,
                                      gkw='version',
                                      g_out=grep_out, g_err=grep_err))
    installed_version_nb = str(v)

    try:
        if (LooseVersion(installed_version_nb)
            < LooseVersion(required_version_nb)):
            add_msg = ' but the installed version number {nb1} ' \
                      'is lower than expected (at least {nb2}).'\
                      .format(nb1=installed_version_nb,
                              nb2=required_version_nb)
            raise EnvironmentError(err_msg + add_msg)
    except TypeError:
        add_msg = ' but something went wrong while trying to determine ' \
            'the installed version number. Likely, {n} is installed but ' \
            'the version number could not be retrieved (got: {v}).'\
            .format(n=name, v=installed_version_nb)
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
              '. It means the desired language ({L}) isn\'t available yet '\
              'in mathmaker. Can\'t continue. Stopping mathmaker.'
    try:
        gettext.translation(__software_name__,
                            settings.localedir,
                            [language]).install()
        settings.language = language
    except IOError as msg:
        log.critical(err_msg.format(gettext_msg=msg, L=language))
        raise EnvironmentError(err_msg.format(gettext_msg=msg, L=language))
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
        retrieve_fonts()
        if not check_font():
            log.critical(err_msg)
            raise ValueError(err_msg)
