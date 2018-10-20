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

from time import sleep
from subprocess import Popen
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest

# from mathmaker.lib import shared_daemon


global DAEMON_PROCESS
DAEMON_PROCESS = Popen(['mathmakerd'])


def test_only_wait_to_ensure_daemon_is_started():
    """Just ensure mathmaker daemon is started"""
    sleep(4)


def test_requests():
    """Check a simple correct request."""
    urlopen("http://127.0.0.1:9999/?sheetname=expand_simple&ip=127.0.0.2")


def test_too_many_requests():
    """Check a second request before the minimal interval time is elapsed."""
    with pytest.raises(HTTPError) as excinfo:
        urlopen("http://127.0.0.1:9999/?sheetname=expand_simple&ip=127.0.0.2")
        urlopen("http://127.0.0.1:9999/?sheetname=expand_simple&ip=127.0.0.2")
    assert str(excinfo.value) == 'HTTP Error 429: Too Many Requests'


def test_too_many_parameters():
    """Check a request using too many parameters is rejected."""
    with pytest.raises(HTTPError) as excinfo:
        urlopen("http://127.0.0.1:9999/?sheetname=expand_simple&ip=127.0.0.2"
                "&extraneous_parameter=any_value")
    assert str(excinfo.value) == 'HTTP Error 404: Not Found'


def test_missing_sheetname():
    """Check a request using wrong parameters is rejected."""
    with pytest.raises(HTTPError) as excinfo:
        urlopen("http://127.0.0.1:9999/?ip=127.0.0.2"
                "&extraneous_parameter=any_value")
    assert str(excinfo.value) == 'HTTP Error 404: Not Found'


def test_missing_wrong_second_argument():
    """Check a request using wrong parameters is rejected."""
    with pytest.raises(HTTPError) as excinfo:
        urlopen("http://127.0.0.1:9999/?sheetname=expand_simple"
                "&extraneous_parameter=any_value")
    assert str(excinfo.value) == 'HTTP Error 404: Not Found'


def test_unknown_sheetname_parameter():
    """Check a request using ?sheetname=valid_name|invalid_val is rejected."""
    with pytest.raises(HTTPError) as excinfo:
        urlopen("http://127.0.0.1:9999/?sheetname=expand_simple|invalid_value")
    assert str(excinfo.value) == 'HTTP Error 400: Bad Request'


def test_unknown_sheetname():
    """Check a request using an unknown sheet name is rejected."""
    with pytest.raises(HTTPError) as excinfo:
        urlopen("http://127.0.0.1:9999/?sheetname=expand_simples")
    assert str(excinfo.value) == 'HTTP Error 404: Not Found'


# def test_simulate_internal_error():
#     """Simulate internal_error."""
#     settings.mm_executable += 'WRONG'
#     import sys
#     sys.stderr.write('settings.mm_executable={}\n'
#                      .format(settings.mm_executable))
#     with pytest.raises(HTTPError) as excinfo:
#         urlopen("http://127.0.0.1:9999/?sheetname=expand_simple")
#     assert str(excinfo.value) == 'HTTP Error 500: Not Found'
#     settings.mm_executable = settings.mm_executable[:-len('WRONG')]


# def test_terminate_daemon():
#     """Just terminate mathmaker daemon"""
#     shared_daemon.shutdown()
