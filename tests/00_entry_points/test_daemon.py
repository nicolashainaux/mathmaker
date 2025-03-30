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

import io
import pytest
from unittest.mock import MagicMock
from http.server import HTTPServer
from mathmaker.lib.tools.request_handler import MathmakerHTTPRequestHandler

FAKE_TIMESTAMP_NOW = 1585407600


@pytest.fixture
def mock_dependencies(mocker):
    """Fixture to mock common dependencies"""
    mocks = {
        'manage_daemon_db': mocker.patch(
            'mathmaker.lib.tools.request_handler.manage_daemon_db'),
        'get_all_sheets': mocker.patch(
            'mathmaker.lib.tools.request_handler.get_all_sheets'),
        'block_ip': mocker.patch(
            'mathmaker.lib.tools.request_handler.block_ip'),
        'popen': mocker.patch('mathmaker.lib.tools.request_handler.Popen'),
        'settings': mocker.patch('mathmaker.settings')
    }

    # Setup default values
    mocks['manage_daemon_db'].return_value = FAKE_TIMESTAMP_NOW
    mocks['get_all_sheets'].return_value = {'test_sheet': 'path/to/sheet'}
    mocks['block_ip'].return_value = False

    # Setup Popen
    mock_process = MagicMock()
    mock_process.stdout.read.return_value = b'mock pdf content'
    mocks['popen'].return_value = mock_process

    # Setup parameters
    mocks['settings'].mm_executable = 'mathmaker'
    mocks['settings'].path.daemon_db = '/tmp/daemon.db'
    mocks['settings'].daemon_logger = MagicMock()

    return mocks


@pytest.fixture
def handler_factory():
    """Fixture to create hander instances"""
    def _create_handler(path, address_string):
        handler = MathmakerHTTPRequestHandler.__new__(
            MathmakerHTTPRequestHandler)

        handler.path = path
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.address_string = MagicMock(return_value=address_string)
        handler.requestline = f'GET {path} HTTP/1.1'

        # Prepare output
        output_buffer = io.BytesIO()
        handler.wfile = MagicMock()
        handler.wfile.write = output_buffer.write

        return handler, output_buffer

    return _create_handler


# Testing daemonized.py
def test_entry_point_successful_server_start(mocker):
    mock_httpd = mocker.Mock(spec=HTTPServer)
    mock_httpd_constructor = mocker.patch('mathmaker.daemonized.HTTPServer',
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
    from mathmaker.daemonized import entry_point, DAEMON_PORT
    from mathmaker.daemonized import MathmakerHTTPRequestHandler

    entry_point()

    mock_httpd_constructor.assert_called_once_with(('', DAEMON_PORT),
                                                   MathmakerHTTPRequestHandler)
    mock_httpd.serve_forever.assert_called_once()


def test_entry_point_port_already_in_use(mocker):
    mocker.patch(
        'mathmaker.daemonized.HTTPServer',
        side_effect=OSError('[Errno 98] Address already in use')
    )

    mock_daemon_context = MagicMock()
    mock_daemon_context.__enter__.return_value = mock_daemon_context

    mocker.patch('daemon.DaemonContext', return_value=mock_daemon_context)

    mock_stderr_write = mocker.patch('sys.stderr.write')

    # Import entry_point() after mocks definitions
    from mathmaker.daemonized import entry_point
    from mathmaker.daemonized import DAEMON_PORT

    with pytest.raises(SystemExit) as excinfo:
        entry_point()
    assert str(excinfo.value) == '1'

    mock_stderr_write.assert_called_with(
        f'\nmathmakerd: Another process is already listening to '
        f'port {DAEMON_PORT}. Aborting.\n'
    )


def test_do_GET_200_response(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet',
        address_string='127.0.0.1'
    )

    handler.do_GET()

    mock_dependencies['popen'].assert_called_once_with(
        ['mathmaker', '--pdf', 'test_sheet'], stdout=-1)
    handler.send_response.assert_called_once_with(200)
    handler.send_header.assert_any_call('Content-Type', 'application/pdf')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() == b'mock pdf content'
    mock_dependencies['settings'].daemon_logger.info.assert_called_once_with(
        '127.0.0.1 GET /?sheetname=test_sheet HTTP/1.1 200')


def test_do_GET_200_with_ip_parameter(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1',
        address_string='192.168.1.1',
    )

    handler.do_GET()

    mock_dependencies['block_ip'].assert_called_once()
    args, _ = mock_dependencies['block_ip'].call_args
    assert 'sheetname' in args[0]
    assert 'ip' in args[0]
    assert args[0]['ip'][0] == '192.168.1.1'
    assert args[1] == FAKE_TIMESTAMP_NOW
    assert args[2] == '/tmp/daemon.db'
    handler.send_response.assert_called_once_with(200)


def test_do_GET_200_with_interactive_arg(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet|interactive&ip=192.168.1.1',
        address_string='192.168.1.1',
    )

    handler.do_GET()

    mock_dependencies['popen'].assert_called_once_with(
        ['mathmaker', '--pdf', '--interactive', 'test_sheet'], stdout=-1)

    mock_dependencies['block_ip'].assert_called_once()
    args, _ = mock_dependencies['block_ip'].call_args
    assert 'sheetname' in args[0]
    assert 'ip' in args[0]
    assert args[0]['ip'][0] == '192.168.1.1'
    assert args[1] == FAKE_TIMESTAMP_NOW
    assert args[2] == '/tmp/daemon.db'
    handler.send_response.assert_called_once_with(200)


def test_do_GET_404_with_three_parameters(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1&extraneous=any_value',
        address_string='192.168.1.1'
    )

    handler.do_GET()

    handler.send_response.assert_called_once_with(404)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() \
        == b'Error 404: one or two parameters allowed'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&ip=192.168.1.1'
        '&extraneous=any_value HTTP/1.1 404 '
        '(only one or two parameters allowed)')


def test_do_GET_404_missing_sheetname(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?ip=192.168.1.1&extraneous_parameter=any_value',
        address_string='192.168.1.1',
    )

    handler.do_GET()

    handler.send_response.assert_called_once_with(404)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() \
        == b'Error 404: sheetname must be in parameters. Only ip is accepted '\
           b'as other possible argument.'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?ip=192.168.1.1&extraneous_parameter=any_value '
        'HTTP/1.1 404 '
        '(sheetname not in query or second argument different from ip)')


def test_do_GET_404_unknown_sheetname(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?ip=192.168.1.1&sheetname=unknown',
        address_string='192.168.1.1',
    )

    handler.do_GET()

    handler.send_response.assert_called_once_with(404)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() == b'Error 404: No such sheetname'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?ip=192.168.1.1&sheetname=unknown '
        'HTTP/1.1 404 (no such sheetname)')


def test_do_GET_404_second_arg_not_ip(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet&unknown_arg=value',
        address_string='192.168.1.1',
    )

    handler.do_GET()

    handler.send_response.assert_called_once_with(404)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() \
        == b'Error 404: sheetname must be in parameters. Only ip is accepted '\
           b'as other possible argument.'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&unknown_arg=value '
        'HTTP/1.1 404 '
        '(sheetname not in query or second argument different from ip)')


def test_do_GET_429_block_IP_scenario1(mock_dependencies, handler_factory):
    # Test with regular request
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1',
        address_string='192.168.1.1'
    )

    mock_dependencies['block_ip'].return_value = True

    handler.do_GET()

    handler.send_response.assert_called_once_with(429)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() \
        == b'Error 429: wait at least 10 s between two requests.'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&ip=192.168.1.1 '
        'HTTP/1.1 429 too many requests from 192.168.1.1')


def test_do_GET_429_block_IP_scenario2(mock_dependencies, handler_factory):
    # Test with wrong request should lead to same result
    handler, output_buffer = handler_factory(
        path='/?ip=192.168.1.1&extraneous_parameter=any_value',
        address_string='192.168.1.1',
    )

    mock_dependencies['block_ip'].return_value = True

    handler.do_GET()

    handler.send_response.assert_called_once_with(429)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() \
        == b'Error 429: wait at least 10 s between two requests.'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?ip=192.168.1.1&extraneous_parameter=any_value '
        'HTTP/1.1 429 too many requests from 192.168.1.1')


def test_do_GET_400_unknown_parameter(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=expand_simple|invalid_value&ip=192.168.1.1',
        address_string='192.168.1.1',
    )

    handler.do_GET()

    handler.send_response.assert_called_once_with(400)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() == b'Error 400: unknown parameter.'

    mock_dependencies['settings'].daemon_logger.warning\
        .assert_called_once_with(
        '192.168.1.1 GET /?sheetname=expand_simple|invalid_value'
        '&ip=192.168.1.1 HTTP/1.1 400 (unknown parameter)')


def test_do_GET_500_external_script_failed(mock_dependencies, handler_factory):
    handler, output_buffer = handler_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1',
        address_string='192.168.1.1',
    )
    mock_dependencies['popen'].side_effect = OSError('mathmaker failed')

    handler.do_GET()

    handler.send_response.assert_called_once_with(500)
    handler.send_header.assert_any_call('Content-Type', 'text/html')
    handler.end_headers.assert_called_once()
    assert output_buffer.getvalue() == b'Error 500: something failed'

    mock_dependencies['settings'].daemon_logger.error\
        .assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&ip=192.168.1.1 '
        'HTTP/1.1 500', exc_info=True)
