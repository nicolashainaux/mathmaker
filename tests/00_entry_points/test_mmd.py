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
from http.server import HTTPServer

FAKE_TIMESTAMP_NOW = 1585407600


def test_entry_point_successful_server_start(mocker):
    mock_httpd = mocker.Mock(spec=HTTPServer)
    mock_httpd_constructor = mocker.patch('mathmaker.mmd.HTTPServer',
                                          return_value=mock_httpd)

    from contextlib import contextmanager

    @contextmanager
    def mock_daemon_context(stdout=None, stderr=None):
        yield

    mocker.patch('daemon.DaemonContext', mock_daemon_context)

    mocker.patch('sys.stdout', new_callable=MagicMock)
    mocker.patch('sys.stderr', new_callable=MagicMock)

    # Mock serve_forever() to avoid to block the tests series
    mock_httpd.serve_forever = mocker.Mock()

    # Import entry_point() after mocks definitions
    from mathmaker.mmd import entry_point, DAEMON_PORT
    from mathmaker.mmd import MathmakerHTTPRequestHandler

    entry_point()

    mock_httpd_constructor.assert_called_once_with(('', DAEMON_PORT),
                                                   MathmakerHTTPRequestHandler)
    mock_httpd.serve_forever.assert_called_once()


def test_entry_point_port_already_in_use(mocker):
    mocker.patch(
        'mathmaker.mmd.HTTPServer',
        side_effect=OSError('[Errno 98] Address already in use')
    )

    mock_daemon_context = MagicMock()
    mock_daemon_context.__enter__.return_value = mock_daemon_context

    mocker.patch('daemon.DaemonContext', return_value=mock_daemon_context)

    mock_stderr_write = mocker.patch('sys.stderr.write')

    # Import entry_point() after mocks definitions
    from mathmaker.mmd import entry_point
    from mathmaker.mmd import DAEMON_PORT

    with pytest.raises(SystemExit) as excinfo:
        entry_point()
    assert str(excinfo.value) == '1'

    mock_stderr_write.assert_called_with(
        f'\nmathmakerd: Another process is already listening to '
        f'port {DAEMON_PORT}. Aborting.\n'
    )
