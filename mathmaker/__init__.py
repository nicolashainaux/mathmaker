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

from . import lib

__version_info__ = (0, 7, 6)
__dev__ = 0
__patch_nb__ = 0
__version__ = '.'.join(str(c) for c in __version_info__)
if __dev__ != 0:
    __version__ += 'dev' + str(__dev__)
if __patch_nb__ != 0:
    __version__ += '-' + str(__patch_nb__)

__software_name__ = 'mathmaker'
__release__ = __version__ + ' (alpha)'
__author__ = 'Nicolas Hainaux'
__author_email__ = 'nh.techn@gmail.com'
__licence__ = 'GNU General Public License v3 or later (GPLv3+)'
__url__ = 'https://gitlab.com/nicolas.hainaux/mathmaker/'
__copyright__ = 'Copyright 2006-2017'
__contact__ = '{author} <{author_email}>'\
              .format(author=__author__, author_email=__author_email__)
__licence_info__ = '{software_ref} is free software. Its license is '\
                   '{software_license}.'
__url_info__ = 'Further details on {software_website}'
__info__ = '{software_name} {r}\nLicense: {li}\n{c} {contact}'\
           .format(software_name=__software_name__,
                   r=__release__, li=__licence__, c=__copyright__,
                   contact=__contact__)

DAEMON_PORT = 9999

__all__ = ['lib', ]
