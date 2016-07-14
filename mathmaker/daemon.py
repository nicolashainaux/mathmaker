# -*- coding: utf-8 -*-

# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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
from subprocess import Popen, PIPE
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

import daemon

from mathmaker import settings
from mathmaker import DAEMON_PORT
from mathmaker.lib import sheet
from mathmaker.lib.tools.xml_sheet import get_xml_sheets_paths


class MathmakerHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # settings.init() is required here in order to have the logger
        # working (if it's in run(), even in the with clause, it works once)
        settings.init()
        log = settings.daemon_logger
        XML_SHEETS = get_xml_sheets_paths()
        all_sheets = {}
        all_sheets.update(sheet.AVAILABLE)
        all_sheets.update(XML_SHEETS)
        query = parse_qs(self.path[2:])
        if len(query) != 1:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 404: only one parameter allowed',
                                   'UTF-8'))
            log.warning(self.address_string() + ' ' + self.requestline
                        + ' 404 (only one parameter allowed)')
        else:
            if 'sheetname' not in query:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('Error 404: No allowed parameter '
                                       'other than sheetname',
                                       'UTF-8'))
                log.warning(self.address_string() + ' ' + self.requestline
                            + ' 404 (no allowed parameter other than '
                            'sheetname)')
            else:
                if query['sheetname'][0] in all_sheets:
                    document = ''
                    try:
                        p = Popen(['mathmaker',
                                   '--pdf',
                                   query['sheetname'][0]],
                                  stdout=PIPE)
                        document = p.stdout.read()
                    except Exception:
                        self.send_response(500)
                        self.send_header('Content-Type', 'text/html')
                        self.end_headers()
                        self.wfile.write(bytes('Error 500: something failed',
                                               'UTF-8'))
                        log.error(self.address_string() + ' '
                                  + self.requestline + ' 500')
                    else:
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/pdf')
                        self.end_headers()
                        self.wfile.write(document)
                        log.info(self.address_string() + ' '
                                 + self.requestline + ' 200')
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes('Error 404: No such sheetname',
                                           'UTF-8'))

                    log.warning(self.address_string() + ' ' + self.requestline
                                + ' 404 (no such sheetname)')


def run():
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        server_address = ('', DAEMON_PORT)
        httpd = HTTPServer(server_address, MathmakerHTTPRequestHandler)
        httpd.serve_forever()

if __name__ == '__main__':
    run()
