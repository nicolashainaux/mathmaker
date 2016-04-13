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
_("{name1} has {nb1} marbles. {name2} has {nb2} marbles more \
than {name1}. How many marbles has {name2}?"),

# 2: Golden goose
"Golden goose":
random.choice([ _("Yesterday, my golden goose laid {nb1} eggs and today she \
laid {nb2} eggs. How many eggs has she laid?"),
                _("Yesterday, my golden goose laid {nb1} eggs. That's {nb2} \
less than today. How many eggs has she laid today?")
              ]),

# 3: Gardener's vegetables
"Gardener's vegetables":
random.choice([ _("The gardener has planted {nb1} salads last week, and {nb2} \
salads more this week. How many salads did he plant altogether?"),
                _("The gardener has planted {nb1} cabbages last week, and \
{nb2} cabbages more this week. How many cabbages did he plant altogether?")
              ]),


# 4: Candies
"Candies":
random.choice([ _("{name1} ate {nb1} candies and {name2} ate {nb2} \
of them. The bag is empty. How many candies were there in the bag?"),
                _("{name} ate {nb1} candies and there are {nb2} \
candies left in the paperbag. How many candies were there in the paperbag?")
]),

# 5: Ages
"Ages":
_("{name1} is {nb1} years old and {name2} is {nb2} years older \
than {name1}. How old is {name2}? |hint:years|"),

# 6: Can
"Can":
_("I had to fill this can with {nb1} {capacity_unit=L} of water. There was \
{nb2} {capacity_unit} left in it. How much does it contain? \
|hint:capacity_unit|"),

# 7: Book
"Book":
random.choice([ _("{masculine_name} has read {nb1} pages of his \
book this morning and read {nb2} pages more this afternoon. How many pages \
has he read today?"),
                _("{feminine_name} has read {nb1} pages of her \
book this morning and read {nb2} pages more this afternoon. How many pages \
has she read today?")
                 ]),

# 8: Bike ride
"Bike ride":
_("I rode {nb1} {length_unit=km} this morning and still have to ride {nb2} \
{length_unit} until back home. What is the length of my ride? \
|hint:length_unit|"),

# 9: Painted walls
"Painted walls":
random.choice([ _("I have painted {nb1} {area_unit=m} of this wall and still \
have {nb2} {area_unit} to paint it completely. What is the area of the wall? \
|hint:area_unit|"),

                _("{nb1} {area_unit=m} of this wall are already painted. \
{nb2} {area_unit} are still missing to have the wall completely painted. What \
is its area? \
|hint:area_unit|")
              ]),

# 10: Sheep
"Sheep":
random.choice([ _("Our neighbours have {nb1} sheep. We have {nb2} more sheep \
than them. How many sheep do we have?"),
                _("Our neighbours have {nb1} sheep. That's {nb2} less than us. \
How many sheep do we have?")
             ]),

}