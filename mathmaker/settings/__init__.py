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

import os
import logging
import logging.config
from glob import glob
from pathlib import Path
from shutil import copyfile

from mathmaker import __version__, __software_name__
from mathmaker.lib.tools import ext_dict, load_config
from mathmaker.core.env import USER_LOCAL_SHARE

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
        lg = logging.getLogger(loggername)
        lg.setLevel(getattr(logging, level))
        lg.addFilter(ContextFilter())
        if loggername in ['dbg.db', 'dbg.db_lock', 'dbg.db_timestamp',
                          'dbg.Exercise.init']:
            raw_logger = logging.getLogger('raw')
            lg.addHandler(raw_logger.handlers[0])
            lg.propagate = False


class default_object(object):
    def __init__(self):
        self.MONOMIAL_LETTER = 'x'
        self.EQUATION_NAME = 'E'


class path_object(object):
    def __init__(self, ldd='', dd='', logger=None):
        ldd += '/'
        self.db = ldd + '{}-{}.db'.format(__software_name__, __version__)
        self.db_dist = dd + '{}.db-dist'.format(__software_name__)
        self.natural_nb_tuples_db = ldd + 'natural_nb_tuples-{}.db'\
            .format(__version__)
        self.natural_nb_tuples_db_dist = dd + 'natural_nb_tuples.db-dist'
        self.daemon_db = ldd + '{}d.db'.format(__software_name__)
        self.shapes_db = ldd + 'shapes-{}.db'.format(__version__)
        self.shapes_db_dist = dd + 'shapes.db-dist'
        self.solids_db = ldd + 'solids-{}.db'.format(__version__)
        self.solids_db_dist = dd + 'solids.db-dist'
        self.anglessets_db = ldd + 'anglessets-{}.db'.format(__version__)
        self.anglessets_db_dist = dd + 'anglessets.db-dist'
        logger.info('db={}'.format(self.db))
        logger.info('shapes db={}'.format(self.shapes_db))
        logger.info('solids db={}'.format(self.solids_db))
        logger.info('anglessets db={}'.format(self.anglessets_db))
        logger.info('natural_nb_tuples db={}'
                    .format(self.natural_nb_tuples_db))
        if (not os.path.isfile(self.db)
            or os.path.getmtime(self.db) < os.path.getmtime(self.db_dist)):
            logger.info('Copy main db from {}\n'.format(self.db_dist))
            copyfile(self.db_dist, self.db)
        if (not os.path.isfile(self.shapes_db)
            or os.path.getmtime(self.shapes_db)
            < os.path.getmtime(self.shapes_db_dist)):
            logger.info('Copy shapes db from {}\n'
                        .format(self.shapes_db_dist))
            copyfile(self.shapes_db_dist, self.shapes_db)
        if (not os.path.isfile(self.solids_db)
            or os.path.getmtime(self.solids_db)
            < os.path.getmtime(self.solids_db_dist)):
            logger.info('Copy solids db from {}\n'
                        .format(self.solids_db_dist))
            copyfile(self.solids_db_dist, self.solids_db)
        if (not os.path.isfile(self.anglessets_db)
            or os.path.getmtime(self.anglessets_db)
            < os.path.getmtime(self.anglessets_db_dist)):
            logger.info('Copy anglessets db from {}\n'
                        .format(self.anglessets_db_dist))
            copyfile(self.anglessets_db_dist, self.anglessets_db)
        if (not os.path.isfile(self.natural_nb_tuples_db)
            or os.path.getmtime(self.natural_nb_tuples_db)
            < os.path.getmtime(self.natural_nb_tuples_db_dist)):
            logger.info('Copy natural_nb_tuples db from {}\n'
                        .format(self.natural_nb_tuples_db_dist))
            copyfile(self.natural_nb_tuples_db_dist, self.natural_nb_tuples_db)


def init():
    global rootdir, localedir, libdir, datadir, settingsdir
    global projectdir
    global outputdir
    global toolsdir
    global testsdir
    global frameworksdir
    global index_path
    global db_index_path
    global shapes_db_index_path
    global solids_db_index_path
    global anglessets_db_index_path
    global natural_nb_tuples_db_index_path
    global default, path
    global mainlogger
    global dbg_logger
    global daemon_logger
    global output_watcher_logger
    global language
    global locale
    global currency
    global font
    global q_numbering_tpl
    global q_numbering_tpl_weight
    global q_numbering_tpl_slideshows
    global q_numbering_tpl_weight_slideshows
    global fonts_list_file
    global encoding
    global xmllint
    global euktoeps
    global lualatex
    global luaotfload_tool
    global msgfmt
    global round_letters_in_math_expr
    global mm_executable
    global available_wNl
    global luatex_version

    luatex_version = ''

    settings_dirname = "settings/"

    __process_name = os.path.basename(__file__)
    __abspath = os.path.abspath(__file__)
    __l1 = len(__process_name)
    __l2 = len(__abspath)
    rootdir = __abspath[:__l2 - __l1][:-(len(settings_dirname))]
    testsdir = os.path.join(Path(rootdir).parent, 'tests')
    localedir = rootdir + "locale/"
    libdir = rootdir + "lib/"
    datadir = rootdir + "data/"
    fonts_list_file = datadir + 'fonts_list.txt'
    toolsdir = rootdir + 'tools/'
    frameworksdir = datadir + 'frameworks/'
    index_path = frameworksdir + 'index.json'
    db_index_path = datadir + 'db_index.json'
    shapes_db_index_path = datadir + 'shapes_db_index.json'
    solids_db_index_path = datadir + 'solids_db_index.json'
    anglessets_db_index_path = datadir + 'anglessets_db_index.json'
    natural_nb_tuples_db_index_path = \
        datadir + 'natural_nb_tuples_db_index.json'
    settingsdir = rootdir + settings_dirname
    projectdir = rootdir[:-len('mathmaker/')]

    available_wNl = sorted([int(os.path.basename(dirname)[1])
                            for dirname in glob(datadir + 'w*l')])

    default = default_object()

    logging.config.dictConfig(load_config('logging', settingsdir))
    mainlogger = logging.getLogger("__main__")
    mainlogger.info("Starting...")
    dbg_logger = logging.getLogger("dbg")
    config_dbglogger(settingsdir)
    daemon_logger = logging.getLogger('__daemon__')
    output_watcher_logger = logging.getLogger("__output_watcher__")

    os.makedirs(USER_LOCAL_SHARE, mode=0o770, exist_ok=True)
    path = path_object(ldd=USER_LOCAL_SHARE, dd=datadir, logger=mainlogger)

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
    q_numbering_tpl = CONFIG['DOCUMENT'].get('QUESTION_NUMBERING_TEMPLATE')
    q_numbering_tpl_weight = CONFIG['DOCUMENT']\
        .get('QUESTION_NUMBERING_TEMPLATE_WEIGHT')
    q_numbering_tpl_slideshows = CONFIG['DOCUMENT']\
        .get('QUESTION_NUMBERING_TEMPLATE_SLIDESHOWS')
    q_numbering_tpl_weight_slideshows = CONFIG['DOCUMENT']\
        .get('QUESTION_NUMBERING_TEMPLATE_WEIGHT_SLIDESHOWS')
    # The locale must be redefined after command line options are known
    locale = language + '.' + encoding
    config_path = CONFIG['PATHS'].get('OUTPUT_DIR')
    if os.path.isabs(config_path):
        msg = 'The path to outfiles read from the configuration ({}) is ' \
            'absolute. It must be a relative path.'.format(config_path)
        mainlogger.error(msg)
        raise ValueError(msg)
    outputdir = os.path.join(Path.home(), config_path)
    if not os.path.isdir(outputdir):
        mainlogger.warning('The output directory read from the '
                           'configuration ({}) does not exist.'
                           .format(outputdir))
        try:
            Path(outputdir).mkdir(parents=True)
        except Exception:
            mainlogger.exception('Impossible to create the missing output '
                                 'directory')
            raise
        mainlogger.warning('Created the output directory read from the '
                           'configuration.')

    round_letters_in_math_expr = CONFIG['LATEX']\
        .get('ROUND_LETTERS_IN_MATH_EXPR', False)
