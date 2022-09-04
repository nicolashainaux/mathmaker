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

import datetime
from pathlib import Path

import toml

from . import lib

pp_path = Path(__file__).parent.parent / 'pyproject.toml'
if not pp_path.is_file():
    pp_path = Path(__file__).parent / 'data/pyproject.toml'

METADATA = toml.loads(pp_path.read_text())

__version__ = METADATA['tool']['poetry']['version']

__software_name__ = METADATA['tool']['poetry']['name']
__release__ = __version__ + ' (alpha)'
__author__ = 'Nicolas Hainaux'
__author_email__ = 'nh.techn@posteo.net'
__licence__ = METADATA['tool']['poetry']['license']
__url__ = 'https://gitlab.com/nicolas.hainaux/mathmaker/'
__copyright__ = f'Copyright 2006-{datetime.datetime.now().year}'
__contact__ = '{author} <{author_email}>'\
              .format(author=__author__, author_email=__author_email__)
__licence_info__ = '{software_ref} is free software. Its license is '\
                   '{software_license}.'
__url_info__ = f'Further details on {__url__}'
__info__ = f'{__software_name__} {__release__}\n'\
    f'License: {__licence__}\n{__copyright__} {__contact__}'

DAEMON_PORT = 9999

__all__ = ['lib', ]
