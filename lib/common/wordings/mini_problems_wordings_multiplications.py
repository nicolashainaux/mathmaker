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
_("{name1} has {nb1} marbles. {name2} has {nb2} times more \
marbles than {name1}. How many marbles has {name2}?"),

# 2: Golden goose
"Golden goose":
_("My golden goose laid {nb1} eggs each day during {nb2} days. How \
many eggs has she laid?"),

# 3: Gardener's vegetables
"Gardener's vegetables":
random.choice([ _("The gardener has planted {nb1} rows of {nb2} salads. \
How many salads did he plant altogether?"),
                _("The gardener has planted {nb1} rows of {nb2} cabbages. \
How many cabbages did he plant altogether?")
              ]),

# 4: Candies
"Candies":
_("I invited {nb1} friends at my birthday's party and want give {nb2} \
candies to each of them. How many candies should I buy?"),

# 5: Pencils boxes
"Pencils boxes":
random.choice([ _("{masculine_name} bought {nb1} boxes of {nb2} \
pencils. How many pens did he buy?"),
                _("{feminine_name} bought {nb1} boxes of {nb2} \
pencils. How many pens did she buy?")
]),

# 6: Pens purchase
"Pens purchase":
random.choice([ _("{masculine_name} bought {nb1} pens at {nb2} £. \
How much did he pay? |hint:£|"),
                _("{feminine_name} bought {nb1} pens at {nb2} £. \
How much did she pay? |hint:£|")
]),

# 7: Pocket money
"Pocket money":
random.choice([ _("{masculine_name} gets {nb1} £ pocket money \
every month. If he doesn't spend it during {nb2} months, how much will \
he spare? |hint:£|"),
                _("{feminine_name} gets {nb1} £ pocket money \
every month. If she doesn't spend it during {nb2} months, how much will she \
spare? |hint:£|")
]),

# 8: Sheep
"Sheep":
_("We have {nb1} sheep. Our neighbours have {nb2} times more sheep than \
us. How many sheep do they have?"),

# 9: Truffles packets
"Truffles packets":
random.choice([ _("{masculine_name} has prepared {nb1} packets \
of {nb2} truffles. How many truffles has he prepared?"),
                _("{feminine_name} has prepared {nb1} packets \
of {nb2} truffles. How many truffles has she prepared?")
]),

# 10: Flour packets
"Flour packets":
_("We have loaded {nb1} flour packets, each weighting {nb2} {mass_unit=kg}. \
How heavy are they altogether? \
|hint:mass_unit|"),

}