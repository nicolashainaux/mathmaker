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

import xml.etree.ElementTree as xml_tree

##
#   @brief  Returns the attributes dictionary of node's child whose tag is
#           matching the tag given as param. Recursively add the results for
#           grandchildren too.
#   @param  tag: the tag we're looking for
def _get_attributes(node, tag, output=[]):
    for child in node:
        if child.tag == tag:
            output.append(child.attrib)
        for grandchild in child:
            output += _get_attributes(grandchild, tag)
    return output

##
#   @brief  Will return a list of all attributes dictionaries of all nodes
#           whose tag matches the param tag, in filename.
def get_attributes(filename, tag):
    return _get_attributes(xml_tree.parse(filename).getroot(), tag)



