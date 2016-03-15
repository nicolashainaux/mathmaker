# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from core.base_calculus import *

class sub_object(object):

    def __init__(self, **options):
        if 'variant' in options and options['variant'] == 'decimal':
                options['variant'] = randomly.pop(['decimal1', 'decimal2'])

        self.variant = options['variant'] if 'variant' in options else "default"
        self.context = options['context'] if 'context' in options else "default"
        self.picture = True if 'picture' in options \
                               and options['picture'] == "true" \
                            else False
