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

# TODO: add yaml schema validation (per json?)
import os
import sys
import logging
import errno
# from collections import OrderedDict
# # from abc import ABCMeta, abstractmethod
#
# import yaml
#
from mathmaker import settings
from mathmaker.lib.tools import ext_dict


def load_config(file_tag, settingsdir):
    """
    Will load the values from the yaml config file, named file_tag.yaml.

    The default configuration values are loaded from
    mathmaker/settings/default/*.yaml, then load_config
    will update with values found successively in
    /etc/mathmaker/*.yaml, then in ~/.config/mathmaker/*.yaml,
    finally in mathmaker/settings/dev/*.yaml.
    """
    import yaml
    # As one wants to log anything as soon as possible, but at least the
    # default values from ``logging.yaml`` must be read before anything
    # can be logged, the logger is only set and used if the filename is
    # not 'logging.yaml'.
    if file_tag != 'logging':
        mainlogger = logging.getLogger("__main__")
    configuration = ext_dict()
    try:
        with open(os.path.join(settingsdir, 'default/', file_tag + '.yaml'))\
                as file_path:
            # __
            if file_tag != 'logging':
                mainlogger.info('Loading ' + file_tag + '.yaml from '
                                + file_path.name)
            configuration = ext_dict(yaml.load(file_path))
    except IOError:
        if file_tag != 'logging':
            mainlogger.error('FileNotFoundError: No default config file for '
                             + file_tag)
        raise FileNotFoundError(errno.ENOENT,
                                os.strerror(errno.ENOENT),
                                file_tag + '.yaml')
    if file_tag == 'logging' and sys.platform.startswith('freebsd'):
        try:
            with open(os.path.join(settingsdir, 'default/',
                                   file_tag + '_freebsd.yaml')) as file_path:
                # __
                configuration.recursive_update(yaml.load(file_path))
        except IOError:
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    file_tag + "_freebsd.yaml")
    for d in ['/etc/mathmaker',
              os.path.join(os.path.expanduser("~"), '.config', 'mathmaker'),
              settingsdir + 'dev']:
        try:
            with open(os.path.join(d, file_tag + '.yaml')) as file_path:
                if file_tag != 'logging':
                    mainlogger.info('Updating config values for ' + file_tag
                                    + ' from ' + file_path.name)
                configuration.recursive_update(yaml.load(file_path))
        except IOError:
            pass
        if file_tag == 'logging' and sys.platform.startswith('freebsd'):
            try:
                with open(os.path.join(d,
                                       file_tag
                                       + '_freebsd.yaml')) as file_path:
                    # __
                    configuration.recursive_update(yaml.load(file_path))
            except IOError:
                pass
    return configuration


def load_sheet(theme, subtheme, sheet_name):
    """
    Retrieve sheet data from yaml file.

    :param theme: the theme where to find the sheet
    :type theme: str
    :param subtheme: the subtheme where to find the sheet
    :type subtheme: str
    :param sheet_name: the name of the sheet
    :type sheet_name: str
    :rtype: OrderedDict
    """
    from ruamel import yaml
    # from ruamel.yaml import YAML
    # yaml = YAML(typ='safe')

    theme_dir = os.path.join(settings.frameworksdir, theme)
    subtheme_file = os.path.join(settings.frameworksdir, theme,
                                 subtheme + '.yaml')
    if os.path.isdir(theme_dir):
        if os.path.isfile(subtheme_file):
            with open(subtheme_file) as file_path:
                file_data = yaml.round_trip_load(file_path)
                if sheet_name in file_data:
                    return file_data[sheet_name]
                else:
                    raise ValueError('No sheet of this name ({}) in the '
                                     'provided theme and subtheme ({}, {}).'
                                     .format(sheet_name, theme, subtheme))
        else:
            raise IOError('Could not find the provided subtheme ({}) in the '
                          'provided theme ({}).'.format(subtheme, theme))
    else:
        raise IOError('Could not find the provided theme ({}) among the '
                      'frameworks.'.format(theme))
