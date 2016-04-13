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
random.choice([  _("{name1} has {nb1} marbles. {name2} \
has {nb2} marbles less than {name1}. How many marbles has {name2}?"),
                    _("{name2} has {nb2} marbles less \
than {name1}, who has {nb1} of them. How many marbles has {name2}?")
]),

# 2: Golden goose
"Golden goose":
_("Yesterday, my golden goose laid {nb1} eggs we used {nb2} of them to \
make an omelet. How many eggs left are there?"),

# 3: Gardener's vegetables
"Gardener's vegetables":
random.choice([ _("The gardener had {nb1} salads in his vegetable garden, \
and harvested {nb2} of them last week. How many salads are still in the \
garden?"),
                _("The gardener had {nb1} cabbages in his vegetable garden, \
and harvested {nb2} of them last week. How many cabbages are still in the \
garden?")
              ]),

# 4: Candies
"Candies":
_("Some friends shared {nb2} of the {nb1} candies of the packet. How many \
candies are there left?"),

# 5: Ages
"Ages":
random.choice([ _("{name1} is {nb1} years old and {name2} is {nb2} \
years younger than {name1}. How old is {name2}? |hint:years|"),
                _("{name2} is {nb2} years younger than {name1}, \
who is {nb1} years old. How old is {name2}? |hint:years|")
              ]),

# 6: Can
"Can":
random.choice([ _("I had to fill this can with {nb2} {capacity_unit=L} of \
water. It contains now {nb1} {capacity_unit}. How much water was left in it? \
|hint:capacity_unit|"),

                _("This can contains altogether {nb1} {capacity_unit=L} of \
water. I had to refill it with {nb2} {capacity_unit}. How much water was left \
in it? \
|hint:capacity_unit|")
              ]),

# 7: Book
"Book":
random.choice([ random.choice([\
                _("{masculine_name} read his book from page {nb2} \
this morning until page {nb1} this afternoon. How many pages has he read \
today?"),
                _("{feminine_name} read her book from page {nb2} \
this morning until page {nb1} this afternoon. How many pages has she read \
today?")
                              ]),

                random.choice([\
                _("Today, {masculine_name} has read his book until \
page {nb1}. This morning he started at page {nb2}. How many pages has he \
read today?"),
                _("Today, {feminine_name} has read her book until \
page {nb1}. This morning she started at page {nb2}. How many pages has she \
read today?")
                              ]),
]),

# 8: Bike ride
"Bike ride":
random.choice([ _("My bike ride is {nb1} {length_unit=km} long and I already \
rode {nb2} {length_unit}. How long do I still have to go cycling? \
|hint:length_unit|"),

                _("I already rode {nb2} {length_unit=km} out of {nb1} \
{length_unit}. How long do I still have to go cycling? \
|hint:length_unit|")
]),

# 9: Painted walls
"Painted walls":
random.choice([ _("I have painted {nb2} {area_unit=m} out of the {nb1} \
{area_unit} of this wall. How much is still left to paint? \
|hint:area_unit|"),

                _("This wall is altogether {nb1} {area_unit=m} wide. I have \
already painted {nb2} {area_unit} of it, how much is there still left to \
paint? \
|hint:area_unit|")
              ]),

# 10: Sheep
"Sheep":
random.choice([ _("Our neighbours have {nb1} sheep. That's {nb2} more than \
us. How many sheep do we have?"),
                _("Our neighbours have {nb1} sheep. We have {nb2} less than \
them. How many sheep do we have?")
             ]),

}