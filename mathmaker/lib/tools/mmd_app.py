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

import logging
from pathlib import Path
from urllib.parse import parse_qs
from subprocess import Popen, PIPE

from .mmd_tools import block_ip, manage_daemon_db, get_all_sheets


def request_handler(environ, start_response):
    app_logger = logging.getLogger('webapp')

    daemon_db_dir = Path.home() / '.local/share/mathmakerd'
    daemon_db_dir.mkdir(parents=False, exist_ok=True)
    daemon_db_path = daemon_db_dir / 'db.sqlite3'

    now_timestamp = manage_daemon_db(daemon_db_path)
    all_sheets = get_all_sheets()

    # Parse query parameters from environ
    if environ['PATH_INFO'] == '/':
        query_string = environ.get('QUERY_STRING', '')
        query = parse_qs(query_string)
    else:
        query = {}

    client_ip = environ.get('REMOTE_ADDR', 'unknown')
    request_line = f"{environ.get('REQUEST_METHOD', 'GET')} "\
        f"{environ.get('PATH_INFO', '/')}?{environ.get('QUERY_STRING', '')}"
    log_header = f'{client_ip} {request_line}'

    if block_ip(query, now_timestamp, daemon_db_path):
        response_body = 'Error 429: wait at least 10 s between two requests.'
        start_response('429 Too Many Requests',
                       [('Content-Type', 'text/html')])
        ip = query.get("ip", ['unknown'])[0]
        app_logger.warning(f'{log_header} 429 too many requests from {ip}')
        return [response_body.encode('UTF-8')]

    if not (1 <= len(query) <= 2):
        response_body = 'Error 404: one or two parameters allowed'
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        app_logger.warning(f'{log_header} 404 (only one or two parameters '
                           f'allowed)')
        return [response_body.encode('UTF-8')]

    if ('sheetname' not in query
            or (len(query) == 2 and 'ip' not in query)):
        response_body = ('Error 404: sheetname must be in parameters. '
                         'Only ip is accepted as other possible argument.')
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        app_logger.warning(f'{log_header} 404 (sheetname not in query or '
                           f'second argument different from ip)')
        return [response_body.encode('UTF-8')]

    sheet_name = query['sheetname'][0]
    optional_args = []

    if '|' in query['sheetname'][0]:
        sheet_name, arg = sheet_name.split('|')
        if arg == 'interactive':
            optional_args.append('--interactive')
        else:
            response_body = 'Error 400: unknown parameter.'
            start_response('400 Bad Request', [('Content-Type', 'text/html')])
            app_logger.warning(f'{log_header} 400 (unknown parameter)')
            return [response_body.encode('UTF-8')]

    if sheet_name not in all_sheets:
        response_body = 'Error 404: No such sheetname'
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        app_logger.warning(f'{log_header} 404 (no such sheetname)')
        return [response_body.encode('UTF-8')]

    document = b''
    try:
        command = ['mathmaker', '--pdf', *optional_args, sheet_name]
        p = Popen(command, stdout=PIPE)
        document = p.stdout.read()
    except Exception:
        response_body = 'Error 500: something failed'
        start_response('500 Internal Server Error',
                       [('Content-Type', 'text/html')])
        app_logger.error(f'{log_header} 500', exc_info=True)
        return [response_body.encode('UTF-8')]
    else:
        start_response('200 OK', [('Content-Type', 'application/pdf')])
        app_logger.info(f'{log_header} 200')
        return [document]


def mmd_app():
    """
    Factory function to create the WSGI application
    """
    return request_handler
