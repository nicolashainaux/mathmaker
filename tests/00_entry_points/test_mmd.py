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


FAKE_TIMESTAMP_NOW = 1585407600


def test_entry_point_successful_server_start(mocker):
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value
    mock_serve = mocker.patch('mathmaker.mmd.serve')
    mock_mmd_app = mocker.patch('mathmaker.mmd.mmd_app')

    from contextlib import contextmanager

    @contextmanager
    def mock_daemon_context(working_directory=None, umask=None,
                            stdout=None, stderr=None):
        yield

    mocker.patch('daemon.DaemonContext', mock_daemon_context)

    mocker.patch('sys.stdout', new_callable=MagicMock)
    mocker.patch('sys.stderr', new_callable=MagicMock)

    # Import entry_point() after mocks definitions
    from mathmaker.mmd import entry_point
    from mathmaker.lib.tools.mmd_tools import load_config
    daemon_port = load_config()['settings']['port']
    daemon_host = load_config()['settings']['host']

    entry_point()

    mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
    mock_socket_instance.bind.assert_called_once_with(('', daemon_port))
    mock_socket_instance.close.assert_called_once()
    mock_serve.assert_called_once_with(mock_mmd_app.return_value,
                                       host=daemon_host, port=daemon_port)


def test_entry_point_port_already_in_use(mocker):
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.bind.side_effect = OSError(
        '[Errno 98] Address already in use')

    mock_daemon_context = MagicMock()
    mock_daemon_context.__enter__.return_value = mock_daemon_context

    mocker.patch('daemon.DaemonContext', return_value=mock_daemon_context)

    mock_stderr_write = mocker.patch('sys.stderr.write')

    # Import entry_point() after mocks definitions
    from mathmaker.mmd import entry_point
    from mathmaker.lib.tools.mmd_tools import load_config
    daemon_port = load_config()['settings']['port']

    with pytest.raises(SystemExit) as excinfo:
        entry_point()
    assert str(excinfo.value) == '1'

    mock_stderr_write.assert_called_with(
        f'\nmathmakerd: Another process is already listening to '
        f'port {daemon_port}. Aborting.\n'
    )
