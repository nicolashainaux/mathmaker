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

import pytest
from unittest.mock import MagicMock
import socket
import logging
from pathlib import Path


def test_configure_logging(mocker):
    """Test that logging is configured correctly"""
    # Mock Path operations
    mock_path = mocker.patch('pathlib.Path')
    mock_path_instance = mock_path.return_value
    mock_path_instance.mkdir.return_value = None

    # Mock config loading
    mock_config = {
        'logging': {
            'log_dir': '/var/log/mathmakerd',
            'log_level': 'INFO',
            'use_syslog': False,
            'max_bytes': 10,
            'backup_count': 5
        },
        'settings': {
            'host': '127.0.0.1',
            'port': 8090
        }
    }
    mocker.patch('mathmaker.mmd.load_config', return_value=mock_config)

    # Mock logger and handlers
    mock_logger = mocker.patch('logging.getLogger')
    mock_file_handler = mocker.patch('logging.handlers.RotatingFileHandler')
    mock_console_handler = mocker.patch('logging.StreamHandler')

    # Import after mocking
    from mathmaker.mmd import configure_logging

    logger, log_dir, settings = configure_logging()

    # Verify logger was configured correctly
    mock_logger.assert_called()
    mock_logger.return_value.setLevel.assert_called_with(logging.INFO)
    mock_file_handler.assert_called()
    mock_console_handler.assert_called()

    # Check settings were returned correctly
    assert settings == mock_config['settings']


def test_configure_logging_with_permissions_error(mocker):
    """Test logging configuration with permission error fallback"""
    # Mock Path operations with permission error on first mkdir
    mock_path = mocker.patch('pathlib.Path')
    mock_primary_dir = MagicMock()
    mock_fallback_dir = MagicMock()

    # Configure mocks to simulate permission error on primary dir
    mock_primary_dir.mkdir.side_effect = PermissionError("Permission denied")
    mock_fallback_dir.mkdir.return_value = None

    # Make Path return different mocks depending on the argument
    def path_side_effect(arg):
        if str(arg) == '/var/log/mathmakerd':
            return mock_primary_dir
        else:
            return mock_fallback_dir

    mock_path.side_effect = path_side_effect
    mock_path.home.return_value = Path('/home/user')

    # Mock config loading
    mock_config = {
        'logging': {
            'log_dir': '/var/log/mathmakerd',
            'log_level': 'INFO',
            'use_syslog': False,
            'max_bytes': 10,
            'backup_count': 5
        },
        'settings': {
            'host': '127.0.0.1',
            'port': 8090
        }
    }
    mocker.patch('mathmaker.mmd.load_config', return_value=mock_config)

    # Mock print to check fallback message
    mock_print = mocker.patch('builtins.print')

    # Mock handlers
    mocker.patch('logging.getLogger')
    mocker.patch('logging.handlers.RotatingFileHandler')
    mocker.patch('logging.StreamHandler')

    # Import after mocking
    from mathmaker.mmd import configure_logging

    configure_logging()

    # Verify fallback path was used
    mock_primary_dir.mkdir.assert_called_once()
    mock_fallback_dir.mkdir.assert_called_once()
    mock_print.assert_called_once()


def test_configure_logging_with_syslog(mocker):
    """Test that syslog is configured when enabled"""
    # Mock config with syslog enabled
    mock_config = {
        'logging': {
            'log_dir': '/var/log/mathmakerd',
            'log_level': 'INFO',
            'use_syslog': True,
            'max_bytes': 10,
            'backup_count': 5
        },
        'settings': {
            'host': '127.0.0.1',
            'port': 8090
        },
        'syslog_facility': 'local0'
    }
    mocker.patch('mathmaker.mmd.load_config', return_value=mock_config)

    # Mock Path and platform
    mock_path = mocker.patch('pathlib.Path')
    mock_path_instance = mock_path.return_value
    mock_path_instance.mkdir.return_value = None

    mocker.patch('platform.system', return_value='Linux')

    # Mock handlers
    mock_logger = mocker.patch('logging.getLogger')
    mocker.patch('logging.handlers.RotatingFileHandler')
    mocker.patch('logging.StreamHandler')
    mock_syslog = mocker.patch('logging.handlers.SysLogHandler')

    # Import after mocking
    from mathmaker.mmd import configure_logging

    configure_logging()

    # Verify syslog was configured
    mock_syslog.assert_called_once()
    # File, console, syslog
    assert mock_logger.return_value.addHandler.call_count >= 3


def test_entry_point_successful_server_start(mocker):
    """Test successful daemon startup with logging configured"""
    # Mock logger with fileno() compatible handlers
    mock_logger = MagicMock()
    mock_handlers = []

    # Create handlers that have streams with fileno()
    for i in range(2):  # Simulate two handlers (file and console)
        mock_handler = MagicMock()
        mock_stream = MagicMock()
        mock_stream.fileno.return_value = i + 10  # A fake file descriptor
        mock_handler.stream = mock_stream
        mock_handlers.append(mock_handler)

    # Configurer le logger avec ces handlers
    mock_logger.handlers = mock_handlers

    # Autres mocks nécessaires
    mock_settings = {'host': '127.0.0.1', 'port': 8090}
    mock_log_dir = Path('/var/log/mathmakerd')

    mocker.patch('mathmaker.mmd.configure_logging',
                 return_value=(mock_logger, mock_log_dir, mock_settings))

    # Mock socket operations
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value

    # Mock waitress serve
    mock_serve = mocker.patch('mathmaker.mmd.serve')
    mock_mmd_app = mocker.patch('mathmaker.mmd.mmd_app')

    # Mock file operations for stdout/stderr
    mocker.patch('builtins.open', MagicMock())

    # Mock daemon context
    mock_context = MagicMock()
    mock_daemon_context = mocker.patch('daemon.DaemonContext',
                                       return_value=mock_context)

    # Import entry_point after mocking
    from mathmaker.mmd import entry_point

    # Run the function to test
    entry_point()

    # Verify DaemonContext was initialized with correct params
    mock_daemon_context.assert_called_once()
    kwargs = mock_daemon_context.call_args[1]
    assert kwargs['working_directory'] == '/var/lib/mathmakerd'
    assert kwargs['umask'] == 0o002

    # Check that files_preserve contains the expected file descriptors
    assert mock_context.files_preserve == [10, 11]  # Our fake descriptors

    # Verify the daemon context was used as a context manager
    mock_context.__enter__.assert_called_once()
    mock_context.__exit__.assert_called_once()

    # Verify socket operations
    mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
    mock_socket_instance.bind.assert_called_once_with(
        ('', mock_settings['port']))
    mock_socket_instance.close.assert_called_once()

    # Verify server was started
    mock_serve.assert_called_once_with(mock_mmd_app.return_value,
                                       host=mock_settings['host'],
                                       port=mock_settings['port'])

    # Verify logging calls
    # At least startup and daemon context logs
    assert mock_logger.info.call_count >= 2


def test_entry_point_port_already_in_use(mocker):
    """Test logging and exit when port is already in use"""
    mock_logger = MagicMock()
    mock_server_logger = MagicMock()

    # Configurer des handlers avec fileno()
    mock_handlers = []
    for i in range(2):
        mock_handler = MagicMock()
        mock_stream = MagicMock()
        mock_stream.fileno.return_value = i + 10
        mock_handler.stream = mock_stream
        mock_handlers.append(mock_handler)

    mock_logger.handlers = mock_handlers

    mock_settings = {'host': '127.0.0.1', 'port': 8090}
    mock_log_dir = Path('/var/log/mathmakerd')

    mocker.patch('mathmaker.mmd.configure_logging',
                 return_value=(mock_logger, mock_log_dir, mock_settings))

    # Mock logger to return our mock_server_logger
    def get_logger(name):
        if name == 'server':
            return mock_server_logger
        return mock_logger

    mocker.patch('logging.getLogger', side_effect=get_logger)

    # Mock socket with 'Address already in use' error
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.bind.side_effect = \
        OSError('[Errno 98] Address already in use')

    # Mock file operations for stdout/stderr
    mocker.patch('builtins.open', MagicMock())

    # Mock sys.exit to avoid test termination
    mock_exit = mocker.patch('sys.exit')

    # Mock daemon context
    mock_context = MagicMock()
    mocker.patch('daemon.DaemonContext', return_value=mock_context)

    # Import entry_point after mocking
    from mathmaker.mmd import entry_point

    # Run the function to test
    entry_point()

    # Verify the error was logged
    mock_server_logger.error.assert_called_once()
    assert "Address already in use" in str(mock_server_logger.error.call_args)
    assert str(mock_settings['port']) \
        in str(mock_server_logger.error.call_args)

    # Verify program exit
    mock_exit.assert_called_once_with(1)


def test_entry_point_other_socket_error(mocker):
    """Test propagation of unexpected socket errors"""
    mock_logger = MagicMock()
    mock_server_logger = MagicMock()

    # Configurer des handlers avec fileno()
    mock_handlers = []
    for i in range(2):
        mock_handler = MagicMock()
        mock_stream = MagicMock()
        mock_stream.fileno.return_value = i + 10
        mock_handler.stream = mock_stream
        mock_handlers.append(mock_handler)

    mock_logger.handlers = mock_handlers

    mock_settings = {'host': '127.0.0.1', 'port': 8090}
    mock_log_dir = Path('/var/log/mathmakerd')

    mocker.patch('mathmaker.mmd.configure_logging',
                 return_value=(mock_logger, mock_log_dir, mock_settings))

    # Mock logger for server logger
    def get_logger(name):
        if name == 'server':
            return mock_server_logger
        return mock_logger

    mocker.patch('logging.getLogger', side_effect=get_logger)

    # Mock socket with different error
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.bind.side_effect = \
        OSError('[Errno 13] Permission denied')

    # Mock file operations for stdout/stderr
    mocker.patch('builtins.open', MagicMock())

    # Mock daemon context
    mock_context = MagicMock()
    mocker.patch('daemon.DaemonContext', return_value=mock_context)

    # Import entry_point after mocking
    from mathmaker.mmd import entry_point

    # Run the function and expect the error to be raised
    with pytest.raises(OSError) as excinfo:
        entry_point()

    assert 'Permission denied' in str(excinfo.value)
