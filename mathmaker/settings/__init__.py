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

import os, sys
import configparser
import logging, logging.config
import yaml
from shutil import copyfile

from lib.tools.ext_dict import ext_dict
from lib.tools.config import load_config


class ContextFilter(logging.Filter):
    """
    Removes the 'dbg.' at the beginning of logged messages.
    """
    def filter(self, record):
        record.name = record.name[4:]
        return True


def config_dbglogger():
    """
    Configures dbg_logger, using to the configuration file values.
    """
    d = ext_dict(load_config('debug_conf', settingsdir)).flat()
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
        self.CURRENCY = {'fr': 'euro', 'fr_FR': 'euro',
                         'en': 'dollar', 'en_US': 'dollar',
                         'en_GB': 'sterling'}


class config_object(object):
    def __init__(self):
        try:
            dummy = CONFIG['LOCALES']
            dummy = CONFIG['LATEX']
        except KeyError:
            mainlogger.error('KeyError: missing category in user_config.yaml.')
            raise KeyError('One expected category is missing in '
                           'user_config.yaml')
        try:
            self.LANGUAGE = CONFIG['LOCALES']['LANGUAGE']
        except KeyError:
            self.LANGUAGE = 'en'
            mainlogger.warning('No value found for the language in '
                               'user_config.yaml. Defaulting to english.')
        # If there's no category/item, then the value will get the default
        # from get()
        # But if no value matches an category/item, the value will still
        # be None, so we have to set it afterwards.
        self.ENCODING = CONFIG['LOCALES'].get('ENCODING', 'UTF-8')
        if self.ENCODING is None:
            self.ENCODING = 'UTF-8'
        self.CURRENCY = CONFIG['LOCALES'].get('CURRENCY',
                                              default.CURRENCY[self.LANGUAGE])
        if self.CURRENCY is None:
            self.CURRENCY = default.CURRENCY[self.LANGUAGE]
        self.FONT = CONFIG['LATEX'].get('FONT') # defaults to None in all cases


class path_object(object):
    def __init__(self):
        self.db = datadir + "mathmaker.db"
        self.db_dist = datadir + "mathmaker.db-dist"
        if not os.path.isfile(self.db)\
            or os.path.getmtime(self.db) < os.path.getmtime(self.db_dist):
            copyfile(self.db_dist, self.db)


def init():
    global rootdir, localedir, libdir, datadir, settingsdir
    global CONFIG, config
    global default, path
    global mainlogger
    global dbg_logger
    global language
    global locale_id

    settings_dirname = "settings/"

    __process_name = os.path.basename(__file__)
    __abspath = os.path.abspath(__file__)
    __l1 = len(__process_name)
    __l2 = len(__abspath)
    rootdir = __abspath[:__l2-__l1][:-(len(settings_dirname))]
    localedir = rootdir + "locale/"
    libdir = rootdir + "lib/"
    datadir = rootdir + "data/"
    settingsdir = rootdir + settings_dirname

    default = default_object()
    path = path_object()

    logging.config.dictConfig(load_config('logging', settingsdir))
    mainlogger = logging.getLogger("__main__")
    mainlogger.info("Starting...")
    dbg_logger = logging.getLogger("dbg")
    config_dbglogger()

    CONFIG = load_config('user_config', settingsdir)
    config = config_object()

    locale_id = config.LANGUAGE + '.' + config.ENCODING

    language = None
