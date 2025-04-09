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
from pathlib import Path
from datetime import datetime

from ruamel.yaml import YAML


def daemon_db_path():
    daemon_db_dir = Path.home() / '.local/share/mathmakerd'
    daemon_db_dir.mkdir(parents=False, exist_ok=True)
    return daemon_db_dir / 'db.sqlite3'


def load_config():
    """Load configuration file"""

    loader = YAML(typ='safe', pure=True)
    config = loader.load(Path(__file__).parent.parent.parent
                         / 'settings/default/mathmakerd.yaml')

    # Paths to check for configuration file
    config_paths = [
        Path('/etc/mathmaker/mathmakerd.yaml'),
        Path.home() / '.config/mathmaker/mathmakerd.yaml',
    ]

    # Update config with user redefined settings, if any
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config.update(loader.load(f))
            except Exception as e:
                print(f'Error reading {config_path}: {e}')

    return config


def manage_daemon_db():
    db_path = daemon_db_path()
    # If the db is too old (more than 1 hour, hardcoded), we delete it.
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_timestamp = time.mktime(datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
                                .timetuple())
    if os.path.isfile(db_path):
        t = time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(os.path.getmtime(db_path)))
        last_access_timestamp = time.mktime(datetime.strptime(t,
                                            "%Y-%m-%d %H:%M:%S")
                                            .timetuple())
        if now_timestamp - last_access_timestamp >= 3600:
            os.remove(db_path)

    # If there's no db, a brand new one is created
    if not os.path.isfile(db_path):
        open(db_path, 'a').close()
        db = sqlite3.connect(db_path)
        db.execute('''CREATE TABLE ip_addresses
                    (id INTEGER PRIMARY KEY,
                    ip_addr TEXT, timeStamp TEXT)''')
        db.close()
    return now_timestamp


def get_all_sheets():
    from mathmaker.lib import old_style_sheet
    from mathmaker.lib.tools.xml import get_xml_sheets_paths
    from mathmaker.lib.tools.frameworks import read_index
    all_sheets = get_xml_sheets_paths()
    all_sheets.update(old_style_sheet.AVAILABLE)
    all_sheets.update(read_index())
    return all_sheets


def block_ip(query, now_timestamp):
    db_path = daemon_db_path()
    if 'ip' not in query:
        return False

    settings = load_config()['settings']

    db = sqlite3.connect(db_path)
    ip = query['ip'][0]
    cmd = f"SELECT id,timeStamp FROM ip_addresses "\
        f"WHERE ip_addr = '{ip}' ORDER BY timeStamp DESC LIMIT 1;"
    qr = tuple(db.execute(cmd))
    most_recent_request_timestamp = 0
    if len(qr):
        most_recent_request_timestamp = \
            time.mktime(datetime.strptime(qr[0][1], "%Y-%m-%d %H:%M:%S")
                        .timetuple())
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd = f"INSERT INTO ip_addresses VALUES(null, '{ip}', '{ts}');"
    db.execute(cmd)
    db.commit()
    db.close()
    if (len(qr)
        and (now_timestamp - most_recent_request_timestamp
             <= settings['timeout'])):
        return True

    return False
