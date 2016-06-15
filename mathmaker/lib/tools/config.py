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
import logging
import errno
import yaml

from .ext_dict import ext_dict

def load_config(file_tag, settingsdir):
    """
    Will load the values from the yaml config file, named file_tag.yaml.

    The default configuration values are loaded from
    mathmaker/settings/default/*.yaml, then load_config
    will update with values found successively in
    /etc/mathmaker/*.yaml, then in ~/.config/mathmaker/*.yaml,
    finally in mathmaker/settings/dev/*.yaml.
    """
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
                                file_tag + ".yaml")
    for d in ['/etc/mathmaker',
              os.path.join(os.path.expanduser("~"), '.config', 'mathmaker'),
              settingsdir + 'dev']:
        try:
            with open(os.path.join(d, file_tag + '.yaml')) as file_path:
                if file_tag != 'logging':
                    mainlogger.info('Updating config values for ' + file_tag
                                    + ' from ' + file_path.name + '.yaml ')
                configuration.recursive_update(yaml.load(file_path))
        except IOError:
            pass
    return configuration

