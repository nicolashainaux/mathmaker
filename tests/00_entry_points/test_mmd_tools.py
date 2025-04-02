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
from http.server import HTTPServer
from unittest.mock import MagicMock
from datetime import datetime, timedelta

import pytest

from mathmaker.lib.tools.mmd_tools import MINIMUM_DAEMON_TIME_INTERVAL
from mathmaker.lib.tools.mmd_tools import get_all_sheets, block_ip
from mathmaker.lib.tools.mmd_tools import manage_daemon_db


@pytest.fixture
def setup_db():
    """Create temporary database for tests"""
    db_path = "test_daemon.db"

    # Check that the file does not already exist
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create the database
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE ip_addresses
                (id INTEGER PRIMARY KEY,
                ip_addr TEXT, timeStamp TEXT)''')
    conn.close()

    yield db_path

    # Clean up after tests
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def temp_db_path(tmp_path):
    """Fixture to provide a temporary path for the database"""
    db_file = tmp_path / "test_daemon.db"
    return str(db_file)


def create_existing_db(db_path, hours_old=2):
    """Utility for creating an old database for tests"""
    # Create a database
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE ip_addresses
                (id INTEGER PRIMARY KEY,
                ip_addr TEXT, timeStamp TEXT)''')
    conn.close()

    # Modify the date on which the file was last modified
    old_time = datetime.now() - timedelta(hours=hours_old)
    old_timestamp = time.mktime(old_time.timetuple())
    os.utime(db_path, (old_timestamp, old_timestamp))


def test_create_new_db_if_not_exists(temp_db_path):
    """Test that the function creates a new database if it does not exist"""
    assert not os.path.isfile(temp_db_path)

    timestamp = manage_daemon_db(temp_db_path)

    assert os.path.isfile(temp_db_path)

    # Check that the timestamp returned is close to the current time
    now_timestamp = time.mktime(datetime.now().timetuple())
    assert abs(timestamp - now_timestamp) < 2  # Two seconds tolerance

    # Check that the database has the expected structure
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('ip_addresses',) in tables

    # Check the table structure
    cursor.execute("PRAGMA table_info(ip_addresses);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    assert 'id' in column_names
    assert 'ip_addr' in column_names
    assert 'timeStamp' in column_names
    conn.close()


def test_remove_old_db(mocker, temp_db_path):
    """Test que la fonction supprime une base de données trop vieille"""
    create_existing_db(temp_db_path)

    # Add some data to the database to check that it has been deleted
    conn = sqlite3.connect(temp_db_path)
    conn.execute("INSERT INTO ip_addresses VALUES "
                 "(1, '192.168.1.1', '2023-01-01 12:00:00')")
    conn.execute("INSERT INTO ip_addresses VALUES "
                 "(2, '10.0.0.1', '2023-01-01 12:30:00')")
    conn.commit()
    conn.close()

    # Configure mocks to simulate it being over an hour old
    now = datetime.now()
    old_time = now - timedelta(hours=2)

    # Calculate return values before mocking
    old_timestamp = time.mktime(old_time.timetuple())
    now_timestamp = time.mktime(now.timetuple())

    # Mock datetime.now to return a fixed value
    mock_datetime = mocker.patch(
        'mathmaker.lib.tools.mmd_tools.datetime')
    mock_now = mock_datetime.now.return_value
    mock_now.strftime.return_value = now.strftime('%Y-%m-%d %H:%M:%S')

    # Mock time.mktime to return expected values
    mock_mktime = mocker.patch(
        'mathmaker.lib.tools.mmd_tools.time.mktime')
    # First call for now_timestamp
    # Second call for last_access_timestamp
    mock_mktime.side_effect = [now_timestamp, old_timestamp]

    # Mock for os.path.getmtime
    mocker.patch('mathmaker.lib.tools.mmd_tools.os.path.getmtime',
                 return_value=old_timestamp)

    # Mock for time.strftime et time.localtime
    mocker.patch('mathmaker.lib.tools.mmd_tools.time.localtime',
                 return_value=old_time.timetuple())
    mocker.patch('mathmaker.lib.tools.mmd_tools.time.strftime',
                 return_value=old_time.strftime('%Y-%m-%d %H:%M:%S'))

    # Check that the file exists before making the call
    assert os.path.isfile(temp_db_path)

    manage_daemon_db(temp_db_path)

    # Check that the old database has been deleted and a new one created
    assert os.path.isfile(temp_db_path)

    # Check that the new database has the expected structure
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('ip_addresses',) in tables

    # Check the new database is empty
    cursor.execute("SELECT COUNT(*) FROM ip_addresses;")
    count = cursor.fetchone()[0]
    assert count == 0
    conn.close()


def test_keep_recent_db(temp_db_path):
    """Test that the function keeps a recent database"""
    # Create a recent database (less than an hour)
    create_existing_db(temp_db_path, hours_old=0.5)

    # Add some data to the database to check that it has been retained
    conn = sqlite3.connect(temp_db_path)
    conn.execute("INSERT INTO ip_addresses VALUES "
                 "(1, '192.168.1.1', '2023-01-01 12:00:00')")
    conn.execute("INSERT INTO ip_addresses VALUES "
                 "(2, '10.0.0.1', '2023-01-01 12:30:00')")
    conn.execute("INSERT INTO ip_addresses VALUES "
                 "(3, '172.16.0.1', '2023-01-01 13:00:00')")
    conn.commit()
    conn.close()

    # Obtain the initial modification date
    initial_mtime = os.path.getmtime(temp_db_path)

    manage_daemon_db(temp_db_path)

    # Check that the file still exists
    assert os.path.isfile(temp_db_path)

    # Check that the modification date has not changed significantly
    # (it may change slightly due to the opening/closing of the DB)
    current_mtime = os.path.getmtime(temp_db_path)
    assert abs(current_mtime - initial_mtime) < 2  # Two seconds tolerance

    # Check that the data is still present
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Check the total number of records
    cursor.execute("SELECT COUNT(*) FROM ip_addresses;")
    count = cursor.fetchone()[0]
    assert count == 3, \
        f"The table should contain 3 records, but contains {count}"

    # Check that the specific IPs are present
    cursor.execute("SELECT ip_addr FROM ip_addresses ORDER BY id;")
    ips = [row[0] for row in cursor.fetchall()]
    assert ips == ['192.168.1.1', '10.0.0.1', '172.16.0.1'], \
        f"The IPs do not match: {ips}"

    # Check that timestamps are retained
    cursor.execute("SELECT timeStamp FROM ip_addresses WHERE id = 1;")
    timestamp = cursor.fetchone()[0]
    assert timestamp == '2023-01-01 12:00:00', \
        f"The timestamp has been changed: {timestamp}"

    conn.close()


def test_return_value_is_current_timestamp(mocker, temp_db_path):
    """Test that the function returns the current timestamp"""
    # Configure the mock to have a fixed value for datetime.now()
    fixed_now = datetime(2023, 5, 15, 12, 0, 0)
    mock_datetime = mocker.patch(
        'mathmaker.lib.tools.mmd_tools.datetime')
    mock_datetime.now.return_value = fixed_now

    # Preparing the return value before mock time.mktime
    expected_timestamp = time.mktime(fixed_now.timetuple())

    # Mock time.mktime to return an expected value
    mock_mktime = mocker.patch(
        'mathmaker.lib.tools.mmd_tools.time.mktime')
    mock_mktime.return_value = expected_timestamp

    result = manage_daemon_db(temp_db_path)

    # Check that the result is the expected timestamp
    assert result == expected_timestamp


def test_block_ip_no_ip_in_query(setup_db):
    """Check that the function returns False if ‘ip’ is not in query"""
    query = {}
    now_timestamp = time.time()

    result = block_ip(query, now_timestamp, setup_db)

    assert result is False


def test_block_ip_first_request(setup_db):
    """Check that the function returns False for the first request for an IP"""
    query = {'ip': ['192.168.1.1']}
    now_timestamp = time.time()

    result = block_ip(query, now_timestamp, setup_db)

    assert result is False

    # Check that the IP has been registered
    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ip_addresses WHERE ip_addr = '192.168.1.1'")
    records = cursor.fetchall()
    conn.close()

    assert len(records) == 1


def test_block_ip_request_after_timeout(setup_db):
    """
    Check that the function returns False if the previous request is old enough
    """
    # Insert an entry older than the timeout
    ip_addr = '192.168.1.2'
    past_time = (datetime.now()
                 - timedelta(seconds=MINIMUM_DAEMON_TIME_INTERVAL + 5))\
        .strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(setup_db)
    conn.execute("INSERT INTO ip_addresses VALUES(null, ?, ?)",
                 (ip_addr, past_time))
    conn.commit()
    conn.close()

    query = {'ip': [ip_addr]}
    now_timestamp = time.mktime(datetime.now().timetuple())

    result = block_ip(query, now_timestamp, setup_db)

    assert result is False

    # Check that a new entry has been added
    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM ip_addresses WHERE ip_addr = '{ip_addr}'")
    records = cursor.fetchall()
    conn.close()

    assert len(records) == 2


def test_block_ip_request_within_timeout(setup_db):
    """
    Checks that the function returns True if the previous query is too recent
    """
    # Insert a recent entry (less than 10 seconds old)
    ip_addr = '192.168.1.3'
    recent_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(setup_db)
    conn.execute("INSERT INTO ip_addresses VALUES(null, ?, ?)",
                 (ip_addr, recent_time))
    conn.commit()
    conn.close()

    query = {'ip': [ip_addr]}
    now_timestamp = time.mktime(datetime.now().timetuple())

    result = block_ip(query, now_timestamp, setup_db)

    assert result is True

    # Check that a new entry has still been added
    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM ip_addresses WHERE ip_addr = '{ip_addr}'")
    records = cursor.fetchall()
    conn.close()

    assert len(records) == 2


def test_block_ip_different_ips(setup_db):
    """Checks that different IPs are processed independently"""
    # Insert a recent entry for a first IP
    ip_addr1 = '192.168.1.4'
    recent_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(setup_db)
    conn.execute("INSERT INTO ip_addresses VALUES(null, ?, ?)",
                 (ip_addr1, recent_time))
    conn.commit()
    conn.close()

    # Test with another IP
    ip_addr2 = '192.168.1.5'
    query = {'ip': [ip_addr2]}
    now_timestamp = time.mktime(datetime.now().timetuple())

    result = block_ip(query, now_timestamp, setup_db)

    assert result is False


# Test with mocking to avoid real delays
def test_block_ip_with_mocked_time(setup_db, mocker):
    """
    Tests operation with mocked-up times to avoid real delays
    """
    ip_addr = '192.168.1.6'

    # Mock datetime.now() mocker for controlling timestamps
    mock_now = datetime(2023, 1, 1, 12, 0, 0)
    mocker.patch('mathmaker.lib.tools.mmd_tools.datetime', autospec=True)
    from mathmaker.lib.tools.mmd_tools import datetime as mocked_datetime
    mocked_datetime.now.return_value = mock_now
    mocked_datetime.strptime.side_effect = datetime.strptime

    # First request
    query = {'ip': [ip_addr]}
    now_timestamp = time.mktime(mock_now.timetuple())

    result1 = block_ip(query, now_timestamp, setup_db)
    assert result1 is False

    # Second request immediately after
    result2 = block_ip(query, now_timestamp, setup_db)
    assert result2 is True

    # Advancing time beyond the minimum
    mock_now_later = datetime(2023, 1, 1, 12, 0,
                              MINIMUM_DAEMON_TIME_INTERVAL + 1)
    mocked_datetime.now.return_value = mock_now_later
    now_timestamp_later = time.mktime(mock_now_later.timetuple())

    # Third request after the deadline
    result3 = block_ip(query, now_timestamp_later, setup_db)
    assert result3 is False


# Testing mmd.py
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


def test_get_all_sheets(mocker):
    mocker.patch('mathmaker.lib.old_style_sheet.AVAILABLE',
                 new={'theme1': 'old1', 'theme2': 'old2'})
    mocker.patch('mathmaker.lib.tools.xml.get_xml_sheets_paths',
                 return_value={'theme3': 'xml3', 'theme4': 'xml4'})
    mocker.patch('mathmaker.lib.tools.frameworks.read_index',
                 return_value={'theme5': 'yaml5', 'theme6': 'yaml6'})
    assert get_all_sheets() == {'theme1': 'old1', 'theme2': 'old2',
                                'theme3': 'xml3', 'theme4': 'xml4',
                                'theme5': 'yaml5', 'theme6': 'yaml6'}
