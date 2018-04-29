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
import errno
import subprocess
import copy
import logging
import xml.etree.ElementTree as XML_PARSER

from mathmaker import settings
from mathmaker.lib.constants import DEFAULT_LAYOUT
from mathmaker.lib.tools import parse_layout_descriptor
from mathmaker.lib.tools.frameworks import parse_qid


# So far, quite useless features, so disabled on august 8th, 2017
# SWAPPABLE_QKINDS_QSUBKINDS = {("rectangle", "area"),
#                               ("rectangle", "perimeter"),
#                               ("square", "area"),
#                               ("square", "perimeter")}
#
# KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE = {
#     ('divi', 'direct', 'area_width_length_rectangle'):
#     ('rectangle', 'length_or_width', 'from_area')}


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


def _read_layout(node, config, layout):
    config.update(node.attrib)
    keep_default_w, keep_default_a = True, True
    spacing = {'spacing_w': 'undefined', 'spacing_a': 'undefined'}
    for part in node:
        s = part.attrib.get('spacing', 'undefined')
        if s != 'jump to next page':
            if part.tag == 'wordings':
                spacing['spacing_w'] = s
            if part.tag == 'answers':
                spacing['spacing_a'] = s
        # part is either wordings or answers
        rowxcol = part.attrib.get('rowxcol', 'none')
        distri = part.attrib.get('print', 'auto')
        if rowxcol == 'none':
            if distri == 'auto':
                distri = 'all'
            else:
                try:
                    distri = int(distri)
                except ValueError:
                    raise ValueError('XMLFileFormatError: a print '
                                     'attribute cannot be turned into int.')
            if not (s == 'jump to next page'
                    and 'rowxcol' not in part.attrib
                    and 'print' not in part.attrib):
                if part.tag == 'wordings':
                    if keep_default_w:
                        layout['exc'] = [None, distri]
                        keep_default_w = False
                    else:
                        layout['exc'] += [None, distri]
                else:
                    if keep_default_a:
                        layout['ans'] = [None, distri]
                        keep_default_a = False
                    else:
                        layout['ans'] += [None, distri]
        else:
            nrow, ncol = parse_layout_descriptor(rowxcol, sep=['×', 'x'],
                                                 special_row_chars=['?'])
            colwidths = part.attrib.get('colwidths', 'auto')
            if colwidths == 'auto':
                colwidths = [int(18 // ncol) for _ in range(ncol)]
            else:
                colwidths = [int(n) for n in colwidths.split(sep=' ')]
                if not len(colwidths) == ncol:
                    raise ValueError(
                        'XMLFileFormatError: in a <layout>, the number of'
                        'columns '
                        'widths does not match the number of cols in '
                        'the rowxcol attribute.')
            if part.tag == 'wordings':
                if keep_default_w:
                    layout['exc'] = [[nrow, ] + colwidths]
                    keep_default_w = False
                else:
                    layout['exc'].append([nrow, ] + colwidths)
            else:
                if keep_default_a:
                    layout['ans'] = [[nrow, ] + colwidths]
                    keep_default_a = False
                else:
                    layout['ans'].append([nrow, ] + colwidths)
            if distri == 'auto':
                distri = ' '.join(['1' for i in range(ncol * nrow)])
            distri = distri.replace(',', ' ').replace(';', ' ')
            distri = tuple(int(n) for n in distri.split())
            if part.tag == 'wordings':
                layout['exc'].append(distri)
            else:
                layout['ans'].append(distri)
        if s == 'jump to next page':
            if part.tag == 'wordings':
                if keep_default_w:
                    layout['exc'] = ['jump', 'next_page']
                    keep_default_w = False
                else:
                    layout['exc'] += ['jump', 'next_page']
            if part.tag == 'answers':
                if keep_default_a:
                    layout['ans'] = ['jump', 'next_page']
                    keep_default_a = False
                else:
                    layout['ans'] += ['jump', 'next_page']
    config.update(spacing)
    return config, layout


def _get_layout_from(node, default_config=None):
    default_layout = copy.deepcopy(DEFAULT_LAYOUT)

    config = default_config

    for child in node:
        if child.tag == 'layout':
            return _read_layout(child, config, default_layout)

    return config, default_layout


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
            raise ValueError(
                '\nXMLFileFormatError: xmllint exited with a return code '
                'of ' + str(returncode) + '\n'
                'xmllint error message is:\n'
                '' + str(call_xmllint.stderr.read().decode(encoding='UTF-8')))

    xml_doc = XML_PARSER.parse(file_name).getroot()

    config, sheet_layout = \
        _get_layout_from(xml_doc, default_config={'type': 'default',
                                                  'unit': 'cm',
                                                  'font_size_offset': '0'})

    return (xml_doc.attrib["header"],
            xml_doc.attrib["title"],
            xml_doc.attrib["subtitle"],
            xml_doc.attrib["text"],
            xml_doc.attrib["answers_title"],
            config["type"],
            int(config["font_size_offset"]),
            config["unit"],
            sheet_layout,
            xml_doc.attrib.get('preset', 'default')
            )


def check_q_consistency(q_attrib, sources):
    """
    (Unfinished) Check the consistency of question's kind, subkind and source.
    """
    q_kind_subkind = '_'.join(parse_qid(q_attrib['id']))
    if (q_kind_subkind == 'intercept_theorem_triangle'
        and sources[0].startswith('ext_proportionality_quadruplet')):
        # __
        mini, maxi = sources[0].split(sep='_')[3].split(sep='to')
        if int(mini) < 11:
            raise ValueError('XMLFileFormatError: for intercept_theorem'
                             '_triangle questions, the minimum number '
                             'should be 11. Here it is only {}.'
                             .format(mini))
        if int(maxi) - int(mini) < 19:
            raise ValueError('XMLFileFormatError: for intercept_theorem'
                             '_triangle questions, the range between '
                             'minimum and maximum should be at '
                             'least 19. Here it is only {}.'
                             .format(str(int(maxi) - int(mini))))
    if (q_kind_subkind == 'intercept_theorem_triangle_formula'
        and not sources[0] == 'nothing'):
        # __
        raise ValueError('XMLFileFormatError: for intercept_theorem'
                         '_triangle_formula questions, the only possible '
                         'source is \'nothing\'. \'{}\' is not correct.'
                         .format(sources[0]))


def _get_q_list_from(exercise_node):
    """
    Retrieves the exercise kind and the questions from one exercise section.

    :param exercise_node: The XML node of the exercise.
    :type exercise_node:
    :rtype: tuple
    """
    questions = []
    # For instance we will get a list of this kind of elements:
    # [{'id': 'multi direct', 'nb': 'int'}, ['table_2_9'], 4]
    # [{'id': 'expand_and_reduce double_expansion'},
    #  ['table_2_9'],
    #  4]

    for child in exercise_node:
        if child.tag == 'question':
            # Useless features, so far, hence disabled on august 8th, 2017
            # If this would be to re-enable, take care attrib has no kind and
            # subkind attributes any more.
            # if ((child.attrib['kind'], child.attrib['subkind'])
            #         in SWAPPABLE_QKINDS_QSUBKINDS):
            #     (child.attrib['kind'], child.attrib['subkind'])\
            #         = (child.attrib['subkind'], child.attrib['kind'])
            #
            # if 'context' in child.attrib:
            #     if ((child.attrib['kind'],
            #         child.attrib['subkind'],
            #         child.attrib['context'])
            #             in KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE):
            #         (child.attrib['kind'],
            #          child.attrib['subkind'],
            #          child.attrib['context']) = \
            #             KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE[
            #             (child.attrib['kind'],
            #              child.attrib['subkind'],
            #              child.attrib['context'])]
            for elt in child:
                o = copy.deepcopy(child.attrib)
                o.update(elt.attrib)
                sources = elt.attrib['source'].split(sep=';;')
                check_q_consistency(o, sources)
                questions += [[o, sources, int(elt.text)]]

    return questions


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
            exercises_list += [(_get_q_list_from(child),
                                _get_layout_from(child, default_config={}),
                                child.attrib, )]
    return exercises_list
