# -*- coding: utf-8 -*-

# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
from http.server import HTTPServer

import daemon

from mathmaker import DAEMON_PORT, __version__
from mathmaker.lib.tools.request_handler import MathmakerHTTPRequestHandler


def entry_point():
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        server_address = ('', DAEMON_PORT)
        try:
            httpd = HTTPServer(server_address, MathmakerHTTPRequestHandler)
        except OSError as excinfo:
            if str(excinfo) == '[Errno 98] Address already in use':
                sys.stderr.write('\nmathmakerd: Another process is already '
                                 f'listening to port {DAEMON_PORT}. '
                                 'Aborting.\n')
                sys.exit(1)
            else:
                raise
        sys.stdout.write(f'Starting mathmakerd {__version__}')
        httpd.serve_forever()
