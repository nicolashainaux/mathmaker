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


SWAPPABLE_QKINDS_QSUBKINDS = {("rectangle", "area"),
                              ("rectangle", "perimeter"),
                              ("square", "area"),
                              ("square", "perimeter")}

KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE = {
    ('divi', 'direct', 'area_width_length_rectangle'):
    ('rectangle', 'length_or_width', 'from_area')}


def get_xml_schema_path():
    return settings.frameworksdir + 'sheet.xsd'


def get_xml_sheets_paths():
    """
    Returns all paths to default xml frameworks.

    They are returned as a dictionary like:
    {id: path_to_matching_file.xml, ...}
    the id being the filename without its extension.

    :rtype: dict
    """
    # We assume all files are to be found as:
    # frameworks/theme_name/subtheme_name/filename.xml
    files = [settings.frameworksdir + d + '/' + sd + '/' + f
             for d in next(os.walk(settings.frameworksdir))[1]
             for sd in next(os.walk(settings.frameworksdir + d))[1]
             for f in next(os.walk(settings.frameworksdir + d + '/' + sd))[2]]
    return {os.path.splitext(os.path.basename(f))[0]: f
            for f in files
            if os.path.splitext(f)[1] == '.xml'}


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


def check_q_consistency(q_attrib, sources):
    """
    (Unfinished) Check the consistency of question's kind, subkind and source.
    """
    q_kind_subkind = '_'.join([q_attrib['kind'], q_attrib['subkind']])
    if (q_kind_subkind == 'intercept_theorem_triangle'
        and sources[0].startswith('ext_proportionality_quadruplet')):
        # __
        mini, maxi = sources[0].split(sep='_')[3].split(sep='to')
        if int(mini) < 11:
            raise error.XMLFileFormatError('For intercept_theorem_triangle '
                                           'questions, the minimum number '
                                           'should be 11. Here it is only {}.'
                                           .format(mini))
        if int(maxi) - int(mini) < 19:
            raise error.XMLFileFormatError('For intercept_theorem_triangle '
                                           'questions, the range between '
                                           'minimum and maximum should be at '
                                           'least 19. Here it is only {}.'
                                           .format(str(int(maxi) - int(mini))))
    if (q_kind_subkind == 'intercept_theorem_triangle_formula'
        and not sources[0] == 'nothing'):
        # __
        raise error.XMLFileFormatError('For intercept_theorem_triangle_formula'
                                       ' questions, the only possible source '
                                       'is \'nothing\'. \'{}\' is not correct.'
                                       .format(sources[0]))


def get_q_kinds_from(exercise_node):
    """
    Retrieves the exercise kind and the questions from one exercise section.

    :param exercise_node: The XML node of the exercise.
    :type exercise_node:
    :rtype: tuple
    """
    questions = []
    # For instance we will get a list of this kind of elements:
    # [{'kind': 'multi', 'subkind': 'direct', 'nb': 'int'}, 'table_2_9', 4]
    # [{'kind': 'expand_and_reduce', 'subkind': 'double_expansion'},
    #  'table_2_9',
    #  4]

    # if no kind is defined, x_kind will still contain the default '', what
    # will lead to use X_Generic
    x_kind = exercise_node.attrib.get('kind', '')
    for child in exercise_node:
        if child.tag == 'question':
            if ((child.attrib['kind'], child.attrib['subkind'])
                    in SWAPPABLE_QKINDS_QSUBKINDS):
                (child.attrib['kind'], child.attrib['subkind'])\
                    = (child.attrib['subkind'], child.attrib['kind'])

            if 'context' in child.attrib:
                if ((child.attrib['kind'],
                    child.attrib['subkind'],
                    child.attrib['context'])
                        in KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE):
                    (child.attrib['kind'],
                     child.attrib['subkind'],
                     child.attrib['context']) = \
                        KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE[
                        (child.attrib['kind'],
                         child.attrib['subkind'],
                         child.attrib['context'])]
            for elt in child:
                o = copy.deepcopy(child.attrib)
                o.update(elt.attrib)
                sources = [elt.attrib['source']]
                if 'source2' in elt.attrib:
                    sources += [elt.attrib['source2']]
                check_q_consistency(o, sources)
                questions += [[o, sources, int(elt.text)]]

        elif child.tag == 'mix':
            q_temp_list = []
            n_temp_list = []
            for elt in child:
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
                    # So far it's not possible to mix questions
                    # requiring several sources with other questions
                    n_temp_list += [[[elt.attrib['source']],
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
            exercises_list += [(exercise.X_Generic,
                                child.attrib,
                                get_q_kinds_from(child))]
    return exercises_list
