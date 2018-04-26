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
import time
import sqlite3
from datetime import datetime
from urllib.parse import parse_qs
from subprocess import Popen, PIPE
from http.server import BaseHTTPRequestHandler

MINIMUM_DAEMON_TIME_INTERVAL = 10


class MathmakerHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        from mathmaker import settings
        from mathmaker.lib import old_style_sheet
        from mathmaker.lib.tools.xml import get_xml_sheets_paths
        from mathmaker.lib.tools.frameworks import read_index
        # settings.init() is required here in order to have the logger
        # working (if it's in run(), even in the with clause, it works once)
        settings.init()
        log = settings.daemon_logger
        # If the db is too old (more than 1 hour, hardcoded), we delete it.
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now_timestamp = time.mktime(datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
                                    .timetuple())
        if os.path.isfile(settings.path.daemon_db):
            t = time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(os.path.getmtime(
                                  settings.path.daemon_db)))
            last_access_timestamp = time.mktime(datetime.strptime(t,
                                                "%Y-%m-%d %H:%M:%S")
                                                .timetuple())
            if now_timestamp - last_access_timestamp >= 3600:
                os.remove(settings.path.daemon_db)

        # If there's no db, a brand new one is created
        if not os.path.isfile(settings.path.daemon_db):
            open(settings.path.daemon_db, 'a').close()
            db = sqlite3.connect(settings.path.daemon_db)
            db.execute('''CREATE TABLE ip_addresses
                       (id INTEGER PRIMARY KEY,
                       ip_addr TEXT, timeStamp TEXT)''')
            db.close()

        XML_SHEETS = get_xml_sheets_paths()
        all_sheets = {}
        all_sheets.update(old_style_sheet.AVAILABLE)
        all_sheets.update(XML_SHEETS)
        all_sheets.update(read_index())
        query = parse_qs(self.path[2:])
        if not (1 <= len(query) <= 2):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Error 404: one or two parameters allowed',
                                   'UTF-8'))
            log.warning(self.address_string() + ' ' + self.requestline
                        + ' 404 (only one or two parameters allowed)')
        else:
            if ('sheetname' not in query
                or (len(query) == 2 and 'ip' not in query)):
                # __
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('Error 404: sheetname must be in '
                                       'parameters. Only ip is accepted as '
                                       'other possible argument.',
                                       'UTF-8'))
                log.warning(self.address_string() + ' ' + self.requestline
                            + ' 404 (sheetname not in query or '
                            'second argument different from ip)')
            else:
                block_ip = False
                if 'ip' in query:
                    db = sqlite3.connect(settings.path.daemon_db)
                    cmd = "SELECT id,timeStamp FROM ip_addresses "\
                          "WHERE ip_addr = '" + query['ip'][0]\
                          + "' ORDER BY timeStamp DESC LIMIT 1;"
                    #   + " AND WHERE "\
                    #   "timeStamp >= datetime('now','-10 seconds');"
                    qr = tuple(db.execute(cmd))
                    most_recent_request_timestamp = 0
                    if len(qr):
                        most_recent_request_timestamp = \
                            time.mktime(datetime.strptime(qr[0][1],
                                                          "%Y-%m-%d %H:%M:%S")
                                        .timetuple())
                    cmd = "INSERT INTO ip_addresses VALUES(null, '" \
                          + query['ip'][0] + "', '" \
                          + datetime.now().strftime('%Y-%m-%d %H:%M:%S') \
                          + "');"
                    db.execute(cmd)
                    db.commit()
                    db.close()
                    if (len(qr)
                        and (now_timestamp - most_recent_request_timestamp
                             <= MINIMUM_DAEMON_TIME_INTERVAL)):
                        # __
                        block_ip = True
                        self.send_response(429)
                        self.send_header('Content-Type', 'text/html')
                        self.end_headers()
                        self.wfile.write(bytes('Error 429: wait at least 10 s '
                                               'between two requests.',
                                               'UTF-8'))
                        log.warning(self.address_string()
                                    + ' ' + self.requestline + ' '
                                    '429 (too many requests) '
                                    'from ip ' + query['ip'][0])

                if not block_ip:
                    sheet_name = query['sheetname'][0]
                    optional_args = []
                    wrong_arg = False
                    if '|' in query['sheetname'][0]:
                        sheet_name, arg = sheet_name.split('|')
                        if arg == 'interactive':
                            optional_args.append('--interactive')
                        else:
                            self.send_response(400)
                            self.send_header('Content-Type', 'text/html')
                            self.end_headers()
                            self.wfile.write(bytes('Error 400: unknown '
                                                   'parameter.',
                                                   'UTF-8'))
                            log.warning(self.address_string()
                                        + ' ' + self.requestline
                                        + ' 400 (unknown parameter)')
                            wrong_arg = True
                    if not wrong_arg:
                        if sheet_name in all_sheets:
                            document = ''
                            try:
                                p = Popen([settings.mm_executable, '--pdf']
                                          + optional_args + [sheet_name],
                                          stdout=PIPE)
                                document = p.stdout.read()
                            except Exception:
                                self.send_response(500)
                                self.send_header('Content-Type', 'text/html')
                                self.end_headers()
                                self.wfile.write(bytes('Error 500: something '
                                                       'failed',
                                                       'UTF-8'))
                                log.error(self.address_string() + ' '
                                          + self.requestline + ' 500',
                                          exc_info=True)
                            else:
                                self.send_response(200)
                                self.send_header('Content-Type',
                                                 'application/pdf')
                                self.end_headers()
                                self.wfile.write(document)
                                log.info(self.address_string() + ' '
                                         + self.requestline + ' 200')
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', 'text/html')
                            self.end_headers()
                            self.wfile.write(bytes('Error 404: '
                                                   'No such sheetname',
                                                   'UTF-8'))

                            log.warning(self.address_string() + ' '
                                        + self.requestline
                                        + ' 404 (no such sheetname)')
