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

from urllib.parse import parse_qs
from subprocess import Popen, PIPE
from http.server import BaseHTTPRequestHandler

from .mmd_tools import block_ip, manage_daemon_db, get_all_sheets

MINIMUM_DAEMON_TIME_INTERVAL = 10


class MathmakerHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        from mathmaker import settings
        # settings.init() is required here in order to have the logger
        # working (if it's in run(), even in the with clause, it works once)
        settings.init()
        log = settings.daemon_logger
        daemon_db_path = settings.path.daemon_db
        now_timestamp = manage_daemon_db(daemon_db_path)
        all_sheets = get_all_sheets()

        query = parse_qs(self.path[2:])
        log_header = f'{self.address_string()} {self.requestline}'

        if block_ip(query, now_timestamp, daemon_db_path):
            self.send_response(429)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 429: wait at least 10 s between '
                                   'two requests.', 'UTF-8'))
            ip = query["ip"][0]
            log.warning(f'{log_header} 429 too many requests from {ip}')
            return

        if not (1 <= len(query) <= 2):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 404: one or two parameters allowed',
                                   'UTF-8'))
            log.warning(f'{log_header} 404 (only one or two parameters '
                        f'allowed)')
            return

        if ('sheetname' not in query
            or (len(query) == 2 and 'ip' not in query)):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 404: sheetname must be in '
                                   'parameters. Only ip is accepted as '
                                   'other possible argument.', 'UTF-8'))
            log.warning(f'{log_header} 404 (sheetname not in query or '
                        f'second argument different from ip)')
            return

        sheet_name = query['sheetname'][0]
        optional_args = []

        if '|' in query['sheetname'][0]:
            sheet_name, arg = sheet_name.split('|')
            if arg == 'interactive':
                optional_args.append('--interactive')
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('Error 400: unknown parameter.',
                                       'UTF-8'))
                log.warning(f'{log_header} 400 (unknown parameter)')
                return

        if sheet_name not in all_sheets:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 404: No such sheetname', 'UTF-8'))

            log.warning(f'{log_header} 404 (no such sheetname)')
            return

        document = ''
        try:
            command = [settings.mm_executable, '--pdf'] + optional_args \
                + [sheet_name]
            p = Popen(command, stdout=PIPE)
            document = p.stdout.read()
        except Exception:
            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 500: something failed', 'UTF-8'))
            log.error(f'{log_header} 500', exc_info=True)
            return
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.end_headers()
            self.wfile.write(document)
            log.info(f'{log_header} 200')
