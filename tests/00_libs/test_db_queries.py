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
import pytest
import sqlite3
from collections import namedtuple

from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.tools import database
from mathmaker.lib.document.frames.exercise \
    import get_nb_sources_from_question_info


def test_empty_query_result():
    """Check if an empty result raises an error."""
    with pytest.raises(RuntimeError):
        next(database.source('w3l', ['id', 'word'],
                             language='non-existing-code'))


def test_wnl():
    """Check a request in all languages for wNl databases is never empty."""
    for lang in next(os.walk(settings.localedir))[1]:
        settings.language = lang
        for i in [2, 3, 4, 5, 6, 7]:
            try:
                assert len(next(database.source('w' + str(i) + 'l',
                                                ['id', 'word'],
                                language=lang)))
            except sqlite3.OperationalError as e:
                # We ignore the non-existing tables among the ones that are
                # tested here, because we know there are. Any other exception
                # must be raised again.
                if (len(e.args) == 1
                    and e.args[0].startswith('no such table: ')):
                    pass
                else:
                    raise


def test_intpairs_for_deci1():
    """Check requests for intpairs suitable for decimal1."""
    collected_results = []
    for i in range(4):
        collected_results.append(shared.mc_source.next('intpairs_9to10',
                                                       suits_for_deci1=1))
    assert (10, 10) not in collected_results
    Q_info = namedtuple('Q_info', 'id,kind,subkind,nb_source,options')
    rq = Q_info('division_direct', 'division', 'direct', ['intpairs_9to10'],
                {'nb_variant': 'decimal1'})
    q_list = [rq for i in range(4)]
    for q in q_list:
        (nbsources_xkw_list, extra_infos) = \
            get_nb_sources_from_question_info(q)
        for (nb_source, xkw) in nbsources_xkw_list:
            drawn = shared.mc_source.next(nb_source, **xkw)
            assert drawn in [(9, 9), (9, 10)]


def test_intpairs_for_deci2():
    """Check requests for intpairs suitable for decimal2."""
    collected_results = []
    for i in range(4):
        collected_results.append(shared.mc_source.next('intpairs_9to10',
                                                       suits_for_deci2=1))
    assert (10, 10) not in collected_results
    assert (9, 10) not in collected_results
    Q_info = namedtuple('Q_info', 'id,kind,subkind,nb_source,options')
    rq = Q_info('division_direct', 'division', 'direct', ['intpairs_9to10'],
                {'nb_variant': 'decimal2'})
    q_list = [rq for i in range(4)]
    for q in q_list:
        (nbsources_xkw_list, extra_infos) = \
            get_nb_sources_from_question_info(q)
        for (nb_source, xkw) in nbsources_xkw_list:
            drawn = shared.mc_source.next(nb_source, **xkw)
            assert drawn == (9, 9)
