# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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
import errno
import subprocess
import copy
import logging
import random

from mathmaker import settings
import xml.etree.ElementTree as XML_PARSER
from mathmaker.lib.sheet import exercise
from mathmaker.lib.sheet.exercise import question
from mathmaker.lib import error


CATALOG = {'mental_calculation': exercise.X_MentalCalculation}
# 'generic': exercise.X_Generic


def get_xml_schema_path():
    return settings.frameworksdir + 'sheet.xsd'


def get_xml_sheets_paths():
    D = settings.frameworksdir
    DM = D + "mental_calculation/"
    L11_1 = "lev11_1/"
    L11_2 = "lev11_2/"
    return {
        'tables2_9': DM + L11_1 + "tables2_9.xml",
        'divisions': DM + L11_1 + "divisions.xml",
        'multi_hole_tables2_9': DM + L11_1 + "multi_hole_tables2_9.xml",
        'multi_hole_any_nb': DM + L11_1 + "multi_hole_any_nb.xml",
        'multi_11_15_25': DM + L11_1 + "multi_11_15_25.xml",
        'multi_decimal': DM + L11_1 + "multi_decimal.xml",
        'multi_reversed': DM + L11_1 + "multi_reversed.xml",
        'ranks': DM + L11_1 + "ranks.xml",
        'mini_problems': DM + L11_1 + "mini_problems.xml",
        'test_11_1': DM + L11_1 + "test_11_1.xml",
        'operations_vocabulary': DM + L11_2 + "operations_vocabulary.xml",
        'multi_divi_10_100_1000': DM + L11_2 + "multi_divi_10_100_1000.xml",
        'rectangles': DM + L11_2 + "rectangles.xml",
        'test_11_2': DM + L11_2 + "test_11_2.xml",
        'polygons_perimeters': DM + L11_2 + "polygons_perimeters.xml",
        'mental_calculation_default': DM + L11_1 + "test_11_1.xml"}


def _get_attributes(node, tag, output=[]):
    """
    Gathers the attributes of all *node*'s children matching *tag*.

    All attributes that match *tag* are recursively added to the output list.
    :param node: The XML Tree node where to start from.
    :type node: :class:`xml.etree.ElementTree.Element` instance
    :param tag: The tag we're looking for.
    :type tag: str
    :param output: The attributes' list.
    :type output: list
    :rtype: list
    """
    for child in node:
        if child.tag == tag:
            output.append(child.attrib)
        for grandchild in child:
            output += _get_attributes(grandchild, tag)
    return output


def get_attributes(filename, tag):
    """
    Gathers the attributes of all *filename*'s '*node*'s matching *tag*.

    :param filename: The XML file name.
    :type filename: str
    :param tag: The tag we're looking for.
    :type tag: str
    :rtype: list
    """
    return _get_attributes(XML_PARSER.parse(filename).getroot(), tag)


def get_sheet_config(file_name):
    """
    Retrieves the sheet configuration values from *file_name*.

    :param file_name: The XML file name.
    :type file_name: str
    :rtype: tuple
    """
    # Validation of the xml file
    # xmllint --noout --schema sheet.xsd file_name
    with open(get_xml_schema_path(), 'r'):
        call_xmllint = subprocess.Popen([settings.xmllint,
                                         "--noout",
                                         "--schema",
                                         get_xml_schema_path(),
                                         file_name],
                                        stderr=subprocess.PIPE)
        returncode = call_xmllint.wait()
        if returncode != 0:
            raise error.XMLFileFormatError(
                "\nxmllint exited with a return code "
                "of " + str(returncode) + "\n"
                "xmllint error message is:\n"
                "" + str(call_xmllint.stderr.read().decode(encoding='UTF-8')))

    xml_doc = XML_PARSER.parse(file_name).getroot()

    sheet_layout = {'exc': [],
                    'ans': []}

    config = {'layout_type': 'std',
              'layout_unit': 'cm',
              'font_size_offset': '0'}

    for child in xml_doc:
        if child.tag == 'layout':
            if 'type' in child.attrib:
                config['layout_type'] = child.attrib['type']
            if 'unit' in child.attrib:
                config['layout_unit'] = child.attrib['unit']
            if 'font_size_offset' in child.attrib:
                config['font_size_offset'] = child.attrib['font_size_offset']

            for exc_or_ans in child:
                for line in exc_or_ans:
                    if line.attrib['nb'] == 'None':
                        sheet_layout[exc_or_ans.tag] += [None]
                        for ex_nb in line:
                            if ex_nb.text == 'all':
                                sheet_layout[exc_or_ans.tag] += ['all']
                            else:
                                ##
                                #   @todo   when we need to read a list of
                                #           numbers
                                pass
                else:
                    ##
                    #   @todo   when we need to read the col_widths
                    pass

    return (xml_doc.attrib["header"],
            xml_doc.attrib["title"],
            xml_doc.attrib["subtitle"],
            xml_doc.attrib["text"],
            xml_doc.attrib["answers_title"],
            config["layout_type"],
            int(config["font_size_offset"]),
            config["layout_unit"],
            sheet_layout
            )


def get_exercises_list(file_name):
    """
    Retrieves the exercises' list from *file_name*.

    :param file_name: The XML file name.
    :type file_name: str
    :rtype: list
    """
    mainlogger = logging.getLogger("__main__")
    try:
        xml_doc = XML_PARSER.parse(file_name).getroot()
    except FileNotFoundError:
        mainlogger.error('FileNotFoundError: ' + file_name)
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                str(file_name))

    exercises_list = []

    for child in xml_doc:
        if child.tag == 'exercise':
            if 'id' not in child.attrib:
                exercises_list += [CATALOG['generic']]
            else:
                exercises_list += [CATALOG[child.attrib['id']]]

    return exercises_list


def get_q_kinds_from(file_name, sw_k_s={}, k_s_ctxt_tr={}):
    """
    Retrieves the exercise kind and the questions from *file_name*.

    :param file_name: The XML file name.
    :type file_name: str
    :param sw_k_s: The swappable qkinds and qsubkinds dict.
    :type sw_k_s: dict
    :param k_s_ctxt_tr: The kind-subkind_contexts to translate.
    :type k_s_ctxt_tr: dict
    :rtype: tuple
    """
    mainlogger = logging.getLogger("__main__")
    try:
        xml_config = XML_PARSER.parse(file_name).getroot()
    except FileNotFoundError:
        mainlogger.error('FileNotFoundError: ' + str(file_name))
        raise error.UnreachableData("the file named: " + str(file_name))

    questions = []

    # For instance we will get a list of this kind of elements:
    # [ {'kind': 'multi', 'subkind': 'direct', 'nb': 'int'}, 'table_2_9', 4]

    x_kind = 'tabular'  # default

    for child in xml_config:
        if child.tag == 'exercise':
            if 'kind' in child.attrib:
                x_kind = child.attrib['kind']
            for subchild in child:
                if subchild.tag == 'question':
                    if ((subchild.attrib['kind'], subchild.attrib['subkind'])
                            in sw_k_s):
                        (subchild.attrib['kind'], subchild.attrib['subkind'])\
                            = (subchild.attrib['subkind'],
                               subchild.attrib['kind'])

                    if 'context' in subchild.attrib:
                        if ((subchild.attrib['kind'],
                            subchild.attrib['subkind'],
                            subchild.attrib['context'])
                                in k_s_ctxt_tr):
                            (subchild.attrib['kind'],
                             subchild.attrib['subkind'],
                             subchild.attrib['context']) = \
                                k_s_ctxt_tr[(subchild.attrib['kind'],
                                             subchild.attrib['subkind'],
                                             subchild.attrib['context'])]
                    for elt in subchild:
                        o = copy.deepcopy(subchild.attrib)
                        o.update(elt.attrib)
                        questions += [[o, elt.attrib['source'], int(elt.text)]]

                elif subchild.tag == 'mix':
                    q_temp_list = []
                    n_temp_list = []
                    for elt in subchild:
                        if elt.tag == 'question':
                            q_temp_list += [elt.attrib]
                        elif elt.tag == 'nb':
                            # We don't check that 'source' is in elt.attrib,
                            # this should have been checked by the xml schema,
                            # nor we don't check if the source tag is valid.
                            # This would be best done by the xml schema
                            # (requires to use xsd1.1 but lxml validates only
                            # xsd1.0). So far, it is done partially and later,
                            # in lib/tools/tags.py
                            n_temp_list += [[elt.attrib['source'],
                                             elt.attrib,
                                             1] for i in range(int(elt.text))]
                        else:
                            raise error.XMLFileFormatError(
                                "Unknown element found in the xml file: "
                                '' + elt.tag)

                    if len(q_temp_list) != len(n_temp_list):
                        raise error.XMLFileFormatError(
                            "Incorrect mix section: the number of sources "
                            "of numbers (" + str(len(n_temp_list)) + ") "
                            "does not match the number of questions "
                            "(" + str(len(q_temp_list)) + ").")

                    # So far, we only check if all of the numbers' sources
                    # may be attributed to any of the questions, in order
                    # to just distribute them all randomly.
                    for n in n_temp_list:
                        for q in q_temp_list:
                            if (not question.match_qtype_sourcenb(
                                q['kind'] + "_" + q['subkind'], n[0])):
                                # __
                                raise error.XMLFileFormatError(
                                    "This source: " + str(n[0]) + " cannot "
                                    "be attributed to this question:"
                                    " " + str(q['kind'] + "_" + q['subkind']))

                    random.shuffle(q_temp_list)
                    random.shuffle(n_temp_list)

                    for (q, n) in zip(q_temp_list, n_temp_list):
                        q.update(n[1])
                        questions += [[q, n[0], 1]]

    return (x_kind, questions)
