# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import random
from lib.common import shared

def init():
    global CONTENT

    CONTENT = {
# Rules: see mini_problems_wordings_rules

# 1: Marbles
"Marbles":
random.choice([ _("{masculine_name} has {nb1} marbles. He gives \
out them to {nb2} friends. How many marbles will get each friend?"),

                _("{feminine_name} has {nb1} marbles. She gives \
out them to {nb2} friends. How many marbles will get each friend?")
                 ]),

# 2: Golden goose
"Golden goose":
_("It took {nb2} days to my golden goose to lay {nb1} eggs. How many eggs \
did she lay everyday?"),

# 3: Gardener's vegetables
"Gardener's vegetables":
random.choice([ _("The gardener has planted {nb1} salads, splitted in \
{nb2} rows. How many salads is there in a row?"),
                _("The gardener has planted {nb1} cabbages, splitted in \
{nb2} rows. How many cabbages is there in a row?"),
              ]),

# 4: Candies
"Candies":
_("I will give out {nb1} candies to the {nb2} friends that I invited at \
my birthday's party. How many candies will receive each of my friends?"),

# 5: Pencils boxes
"Pencils boxes":
_("{name} put {nb1} pencils away in {nb2} boxes. How many pencils \
are there in each box?"),

# 6: Pens purchase
"Pens purchase":
_("{name} paid {nb1} £ for {nb2} pens. How much does cost one pen?"),

# 7: Pocket money
"Pocket money":
random.choice([ _("{masculine_name} has received altogether \
{nb1} £ pocket money in {nb2} months. How much did he receive every month? \
|hint:£|"),
                _("{feminine_name} has received altogether \
{nb1} £ pocket money in {nb2} months. How much did she receive every month? \
|hint:£|")
              ]),

# 8: Sheep
"Sheep":
_("Our neighbours have {nb1} sheep. That's {nb2} times more than us. \
How many sheep do we have?"),

# 9: Truffles packets
"Truffles packets":
_("{name} has prepared {nb1} truffles splitted in {nb2} packets. \
How many truffles is there in one packet?"),

# 10: Flour packets
"Flour packets":
_("We have loaded {nb1} {mass_unit=kg} of flour, shared in {nb2} packets. \
How heavy is one packet? |hint:mass_unit|"),

}