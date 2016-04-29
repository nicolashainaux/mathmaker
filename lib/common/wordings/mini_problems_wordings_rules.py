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


#        Each key of CONTENT should match one context, even if it can be
#        stated in several formulations (for instance a masculine and a
#        feminine versions; or different ways of wording the same problem).
#
# Rules: {These_words} must be kept separated from other words by spaces.
#        So, do not write "{nb1}{length_unit}" but "{nb1} {length_unit}".
#
#        {any_key=value} will be replaced by {any_key} and the value kept in
#        memory (stored in the attribute "any_key", what will be created if it
#        doesn't exist, and replaced if it does).
#
#        Apart from the special handlings (see below), any single {key} what
#        does not match an attribute of the question's object will lead to an
#        exception. {nb1} and {nb2} are usually defined.
#
#        A special handing will be applied to {name}, {nameN}, {masculine_name},
#        {masculine_nameN}, {feminine_name} and {feminine_nameN}: if no
#        matching attribute is set yet, then a random name (respectively
#        masculine name or feminine name) will be attributed automatically.
#
#        A special handling will be applied to {*_unit} keys ("undefined units")
#        (where * can be length, capacity, mass, area or volume): if no
#        matching *_unit attribute is already set, it will receive a random
#        value depending on its kind (length, capacity, mass, area, volume).
#
#        Same handling applies to {*_unitN} keys, where N is any single char
#        usable in a python attribute's name. This allows to create questions
#        with several different units of the same kind, like in:
#        "Convert {nb1} {length_unit1} into {length_unit2}. |hint:length_unit2|"
#
#        Moreover, any undefined area_unit will always match length_unit (if
#        defined), and area_unitN will always match length_unitN (if defined).
#        Same applies to volume_unit and volume_unitN.
#        For areas and volume, simply write the related length's unit name:
#        {area_unit=m} --> this will be turned into m²
#        {volume_unit=dm}  --> this will be turned into dm³
#
#        One could write wordings like:
#        a.
#        "Calculate the volume of a cube whose side's length is {nb1} \
#        {length_unit=cm}. \
#        |hint:volume_unit|"   --> volume_unit will automatically be cm³
#        b.
#        "How much is {nb1} {length_unit1=dm} + {nb2} {length_unit2=cm}? \
#        |hint:length_unit1|"
#        c.
#        "What's the area of the side of a cube whose volume is {nb1} \
#        {volume_unit=cm}? |hint:area_unit|"
#        --> volume_unit will be cm³ and area_unit will be cm²
#
#        After the special handling has been applied to *_unit and *_unitN keys,
#        any {key} present in the sentence will be included in the formatting
#        dictionary of the sentence, the matching attribute value being used
#        in this key, value pair.
#
#        To tell mathmaker a "hint" should be displayed in the answer cell
#        (like "........ km"), it's possible to use this:
#        |hint:length_unit| (will match attribute 'length_unit' of the question)
#        or:
#        |hint:km|
#        This |hint:something| will be removed from the sentence.
#        Take care, if the value provided after "hint:" doesn't match an
#        already existing attribute, it will be handled as is (hence if
#        you write |hint:area_unit| and no length_unit or area_unit does exist,
#        mathmaker will display "....... area_unit" in the cell.).
#        ALSO, THE HINT HAS TO BE PLACED at the end of the sentence, separated
#        by a space, with no punctuation close to it, its content must start
#        with "hint:" and there must be at least one char between : and |
#        (otherwise it won't have any effect and won't be removed from the
#        sentence).
#        Only one hint (the one at the very end of the sentence) will be taken
#        into account. All other possible ones will be ignored (and not
#        removed).