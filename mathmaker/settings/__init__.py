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

import os
import logging
import logging.config
from shutil import copyfile

from mathmaker.lib.tools.ext_dict import ext_dict
from mathmaker.lib.tools.config import load_config

AVAILABLE = {'LANGUAGES': ['fr', 'fr_FR', 'en', 'en_US', 'en_GB'],
             'CURRENCY': {'fr': 'euro', 'fr_FR': 'euro',
                          'en': 'dollar', 'en_US': 'dollar',
                          'en_GB': 'sterling'}}


class ContextFilter(logging.Filter):
    """
    Removes the 'dbg.' at the beginning of logged messages.
    """
    def filter(self, record):
        record.name = record.name[4:]
        return True


def config_dbglogger(sd):
    """
    Configures dbg_logger, using to the configuration file values.
    """
    d = ext_dict(load_config('debug_conf', sd)).flat()
    for loggername, level in d.items():
        l = logging.getLogger(loggername)
        l.setLevel(getattr(logging, level))
        l.addFilter(ContextFilter())
        if loggername in ['dbg.db']:
            raw_logger = logging.getLogger('raw')
            l.addHandler(raw_logger.handlers[0])
            l.propagate = False


class default_object(object):
    def __init__(self):
        self.MONOMIAL_LETTER = 'x'
        self.EQUATION_NAME = 'E'


class path_object(object):
    def __init__(self, **dirs):
        dd = dirs.get('dd')
        self.db = dd + "mathmaker.db"
        self.db_dist = dd + "mathmaker.db-dist"
        self.daemon_db = dd + "mathmakerd.db"
        if (not os.path.isfile(self.db)
            or os.path.getmtime(self.db) < os.path.getmtime(self.db_dist)):
            # __
            copyfile(self.db_dist, self.db)


def init():
    global rootdir, localedir, libdir, datadir, settingsdir
    global projectdir
    global outputdir
    global toolsdir
    global frameworksdir
    global default, path
    global mainlogger
    global dbg_logger
    global daemon_logger
    global language
    global locale
    global currency
    global font
    global fonts_list_file
    global encoding
    global xmllint
    global euktoeps
    global lualatex
    global luaotfload_tool
    global msgfmt
    global round_letters_in_math_expr
    global mm_executable

    settings_dirname = "settings/"

    __process_name = os.path.basename(__file__)
    __abspath = os.path.abspath(__file__)
    __l1 = len(__process_name)
    __l2 = len(__abspath)
    rootdir = __abspath[:__l2 - __l1][:-(len(settings_dirname))]
    localedir = rootdir + "locale/"
    libdir = rootdir + "lib/"
    datadir = rootdir + "data/"
    fonts_list_file = datadir + 'fonts_list.txt'
    toolsdir = rootdir + 'tools/'
    frameworksdir = datadir + 'frameworks/'
    settingsdir = rootdir + settings_dirname
    projectdir = rootdir[:-len('mathmaker/')]

    default = default_object()
    path = path_object(dd=datadir)

    logging.config.dictConfig(load_config('logging', settingsdir))
    mainlogger = logging.getLogger("__main__")
    mainlogger.info("Starting...")
    dbg_logger = logging.getLogger("dbg")
    config_dbglogger(settingsdir)
    daemon_logger = logging.getLogger('__daemon__')

    CONFIG = load_config('user_config', settingsdir)
    xmllint = CONFIG["PATHS"]["XMLLINT"]
    lualatex = CONFIG["PATHS"]["LUALATEX"]
    luaotfload_tool = CONFIG["PATHS"]["LUAOTFLOAD_TOOL"]
    msgfmt = CONFIG["PATHS"]["MSGFMT"]
    euktoeps = CONFIG["PATHS"]["EUKTOEPS"]
    mm_executable = CONFIG["DAEMON"]["MATHMAKER_EXECUTABLE"]
    language = CONFIG['LOCALES'].get('LANGUAGE', 'en_US')
    if language not in AVAILABLE['LANGUAGES']:
        language = 'en_US'
        mainlogger.warning('The language was overriden by an unsupported '
                           'value (' + str(language) + ') in a '
                           'a configuration file.')
    encoding = CONFIG['LOCALES'].get('ENCODING', 'UTF-8')
    if encoding is None:
        encoding = 'UTF-8'
        mainlogger.warning('The encoding was overriden by None in '
                           'a configuration file.')
    currency = CONFIG['LOCALES'].get('CURRENCY',
                                     AVAILABLE['CURRENCY'][language])
    if currency is None:
        currency = AVAILABLE['CURRENCY'][language]
    if currency not in iter(AVAILABLE['CURRENCY'].values()):
        currency = AVAILABLE['CURRENCY'][language]
    font = CONFIG['LATEX'].get('FONT')  # defaults to None in all cases
    # The locale must be redefined after command line options are known
    locale = language + '.' + encoding
    outputdir = CONFIG['PATHS'].get('OUTPUT_DIR')
    if not os.path.isdir(outputdir):
        mainlogger.warning('The output directory read from the '
                           'configuration is not a valid directory.')
    round_letters_in_math_expr = CONFIG['LATEX']\
        .get('ROUND_LETTERS_IN_MATH_EXPR', False)
