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

FAKE_TIMESTAMP_NOW = 1585407600


@pytest.fixture
def mock_dependencies(mocker):
    """Fixture to mock common dependencies"""
    mocks = {
        'manage_daemon_db': mocker.patch(
            'mathmaker.lib.tools.mmd_app.manage_daemon_db'),
        'get_all_sheets': mocker.patch(
            'mathmaker.lib.tools.mmd_app.get_all_sheets'),
        'block_ip': mocker.patch(
            'mathmaker.lib.tools.mmd_app.block_ip'),
        'popen': mocker.patch('mathmaker.lib.tools.mmd_app.Popen')
    }

    # Setup default values
    mocks['manage_daemon_db'].return_value = FAKE_TIMESTAMP_NOW
    mocks['get_all_sheets'].return_value = {'test_sheet': 'path/to/sheet'}
    mocks['block_ip'].return_value = False

    # Setup Popen
    mock_process = MagicMock()
    mock_process.stdout.read.return_value = b'mock pdf content'
    mocks['popen'].return_value = mock_process

    return mocks


@pytest.fixture
def wsgi_app_factory(mock_dependencies):
    """Fixture to create and run WSGI app"""
    from mathmaker.lib.tools.mmd_app import request_handler

    def _create_and_run_app(path, client_ip='127.0.0.1'):
        # Prepare WSGI environ
        if '?' in path:
            path_info, query_string = path.split('?', 1)
        else:
            path_info, query_string = path, ''

        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'REMOTE_ADDR': client_ip,
        }

        # Prepare start_response callback
        start_response_status = [None]
        start_response_headers = [None]

        def start_response(status, headers):
            start_response_status[0] = status
            start_response_headers[0] = headers

        # Run the app
        response_body = request_handler(environ, start_response)

        return {
            'status': start_response_status[0],
            'headers': start_response_headers[0],
            'body': b''.join(response_body)
        }

    return _create_and_run_app


def test_wsgi_app_200_response(mocker, mock_dependencies, wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(path='/?sheetname=test_sheet')

    mock_dependencies['popen'].assert_called_once_with(
        ['mathmaker', '--pdf', 'test_sheet'], stdout=-1)
    assert response['status'] == '200 OK'
    assert ('Content-Type', 'application/pdf') in response['headers']
    assert response['body'] == b'mock pdf content'
    mock_logger.return_value.info.assert_called_once_with(
        '127.0.0.1 GET /?sheetname=test_sheet 200')


def test_wsgi_app_200_with_ip_parameter(mocker,
                                        mock_dependencies,
                                        wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1',
        client_ip='192.168.1.1',
    )

    mock_dependencies['block_ip'].assert_called_once()
    args, _ = mock_dependencies['block_ip'].call_args
    assert 'sheetname' in args[0]
    assert 'ip' in args[0]
    assert args[0]['ip'][0] == '192.168.1.1'
    assert args[1] == FAKE_TIMESTAMP_NOW
    assert response['status'] == '200 OK'


def test_wsgi_app_200_with_interactive_arg(mocker,
                                           mock_dependencies,
                                           wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?sheetname=test_sheet|interactive&ip=192.168.1.1',
        client_ip='192.168.1.1',
    )

    mock_dependencies['popen'].assert_called_once_with(
        ['mathmaker', '--pdf', '--interactive', 'test_sheet'], stdout=-1)

    mock_dependencies['block_ip'].assert_called_once()
    args, _ = mock_dependencies['block_ip'].call_args
    assert 'sheetname' in args[0]
    assert 'ip' in args[0]
    assert args[0]['ip'][0] == '192.168.1.1'
    assert args[1] == FAKE_TIMESTAMP_NOW
    assert response['status'] == '200 OK'


def test_wsgi_app_404_with_three_parameters(mocker,
                                            mock_dependencies,
                                            wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1&extraneous=any_value',
        client_ip='192.168.1.1'
    )

    assert response['status'] == '404 Not Found'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] == b'Error 404: one or two parameters allowed'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&ip=192.168.1.1'
        '&extraneous=any_value 404 '
        '(only one or two parameters allowed)')


def test_wsgi_app_404_missing_sheetname(mocker,
                                        mock_dependencies,
                                        wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?ip=192.168.1.1&extraneous_parameter=any_value',
        client_ip='192.168.1.1',
    )

    assert response['status'] == '404 Not Found'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] \
        == b'Error 404: sheetname must be in parameters. Only ip is accepted '\
           b'as other possible argument.'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?ip=192.168.1.1&extraneous_parameter=any_value '
        '404 '
        '(sheetname not in query or second argument different from ip)')


def test_wsgi_app_404_unknown_sheetname(mocker,
                                        mock_dependencies,
                                        wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?ip=192.168.1.1&sheetname=unknown',
        client_ip='192.168.1.1',
    )

    assert response['status'] == '404 Not Found'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] == b'Error 404: No such sheetname'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?ip=192.168.1.1&sheetname=unknown '
        '404 (no such sheetname)')


def test_wsgi_app_404_second_arg_not_ip(mocker,
                                        mock_dependencies,
                                        wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?sheetname=test_sheet&unknown_arg=value',
        client_ip='192.168.1.1',
    )

    assert response['status'] == '404 Not Found'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] \
        == b'Error 404: sheetname must be in parameters. Only ip is accepted '\
           b'as other possible argument.'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&unknown_arg=value '
        '404 '
        '(sheetname not in query or second argument different from ip)')


def test_wsgi_app_429_block_IP_scenario1(mocker,
                                         mock_dependencies,
                                         wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    # Test with regular request
    mock_dependencies['block_ip'].return_value = True

    response = wsgi_app_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1',
        client_ip='192.168.1.1'
    )

    assert response['status'] == '429 Too Many Requests'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] \
        == b'Error 429: wait at least 10 s between two requests.'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&ip=192.168.1.1 '
        '429 too many requests from 192.168.1.1')


def test_wsgi_app_429_block_IP_scenario2(mocker,
                                         mock_dependencies,
                                         wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    # Test with wrong request should lead to same result
    mock_dependencies['block_ip'].return_value = True

    response = wsgi_app_factory(
        path='/?ip=192.168.1.1&extraneous_parameter=any_value',
        client_ip='192.168.1.1',
    )

    assert response['status'] == '429 Too Many Requests'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] \
        == b'Error 429: wait at least 10 s between two requests.'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?ip=192.168.1.1&extraneous_parameter=any_value '
        '429 too many requests from 192.168.1.1')


def test_wsgi_app_400_unknown_parameter(mocker,
                                        mock_dependencies,
                                        wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    response = wsgi_app_factory(
        path='/?sheetname=expand_simple|invalid_value&ip=192.168.1.1',
        client_ip='192.168.1.1',
    )

    assert response['status'] == '400 Bad Request'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] == b'Error 400: unknown parameter.'

    mock_logger.return_value.warning.assert_called_once_with(
        '192.168.1.1 GET /?sheetname=expand_simple|invalid_value'
        '&ip=192.168.1.1 400 (unknown parameter)')


def test_wsgi_app_500_external_script_failed(mocker,
                                             mock_dependencies,
                                             wsgi_app_factory):
    mock_logger = mocker.patch('mathmaker.lib.tools.mmd_app.logging.getLogger',
                               autospec=True)
    mock_logger.return_value = MagicMock()
    mock_dependencies['popen'].side_effect = OSError('mathmaker failed')

    response = wsgi_app_factory(
        path='/?sheetname=test_sheet&ip=192.168.1.1',
        client_ip='192.168.1.1',
    )

    assert response['status'] == '500 Internal Server Error'
    assert ('Content-Type', 'text/html') in response['headers']
    assert response['body'] == b'Error 500: something failed'

    mock_logger.return_value.error.assert_called_once_with(
        '192.168.1.1 GET /?sheetname=test_sheet&ip=192.168.1.1 '
        '500', exc_info=True)


def test_mmd_app():
    from mathmaker.lib.tools.mmd_app import mmd_app, request_handler
    app = mmd_app()
    assert app == request_handler
