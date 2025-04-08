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
import socket
import logging
import platform
from pathlib import Path
from logging.handlers import RotatingFileHandler, SysLogHandler

import daemon
from waitress import serve

from mathmaker import __version__
from mathmaker.lib.tools.mmd_app import mmd_app
from mathmaker.lib.tools.mmd_tools import load_config


def configure_logging():
    config = load_config()

    log_dir0 = Path(config['logging'].get('log_dir', '/var/log/mathmakerd'))
    log_level_name = config['logging'].get('log_level', 'INFO')
    log_level = getattr(logging, log_level_name)
    use_syslog = config['logging'].get('use_syslog', False)

    # /var/log requires root rights; otherwise fallback to another place
    try:
        log_dir0.mkdir(parents=False, exist_ok=True)
        log_dir = log_dir0
    except PermissionError:
        log_dir1 = Path.home() / '.local/log/mathmakerd'
        log_dir1.mkdir(parents=False, exist_ok=True)
        print(f"Cannot use {log_dir0}, utilisation de {log_dir1} à la place")
        log_dir = log_dir1

    log_file = log_dir / 'mathmakerd.log'

    # Setup root logger, formatter, handlers
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - '
        '%(message)s'
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config['logging']['max_bytes'] * 1024 * 1024,
        backupCount=config['logging']['backup_count']
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add Syslog if configured
    if use_syslog:
        syslog_facility = config.get('syslog_facility', 'daemon')
        facility = getattr(SysLogHandler, f'LOG_{syslog_facility.upper()}')

        system = platform.system().lower()
        if system == 'linux':
            syslog_address = '/dev/log'
        elif system == 'freebsd':
            syslog_address = '/var/run/log'
        else:
            syslog_address = ('localhost', 514)  # Standard fallback

        try:
            syslog_handler = SysLogHandler(address=syslog_address,
                                           facility=facility)
            syslog_format = \
                '%(name)s[%(process)d]: %(levelname)s - %(message)s'
            syslog_handler.setFormatter(logging.Formatter(syslog_format))
            logger.addHandler(syslog_handler)
            logger.info('Syslog enabled')
        except (FileNotFoundError, PermissionError) as e:
            logger.warning(f'Cannot connect to syslog: {e}')

    return logger, log_dir, config['settings']


def entry_point():
    main_logger, log_dir, settings = configure_logging()
    main_logger.info(f'Starting mathmakerd {__version__}')

    daemon_context = daemon.DaemonContext(
        working_directory='/var/lib/mathmakerd',
        umask=0o002,
        stdout=open(log_dir / 'stdout.log', 'w+'),
        stderr=open(log_dir / 'stderr.log', 'w+'),
    )

    daemon_context.files_preserve = [
        handler.stream.fileno() for handler in main_logger.handlers
        if hasattr(handler, 'stream') and hasattr(handler.stream, 'fileno')
    ]

    with daemon_context:
        main_logger.info('Daemon context initialized')
        server_logger = logging.getLogger('server')
        try:
            server_logger.info(
                f"Test if port {settings['port']} is already in use")
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('', settings['port']))
            test_socket.close()
        except OSError as excinfo:
            if 'Address already in use' in str(excinfo):
                server_logger.error(f"Another process is already listening "
                                    f"to port {settings['port']}. Aborting.")
                sys.exit(1)
            else:
                raise

        server_logger.info('Startup waitress server')
        serve(mmd_app(), host=settings['host'], port=settings['port'])
