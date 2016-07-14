# -*- coding: utf-8 -*-

# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# import time
# start_time = time.time()
import sys
import os
import argparse
import locale

from mathmaker import __info__, __software_name__
from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib import startup_actions
from mathmaker.lib import sheet
from mathmaker.lib import list_sheets
from mathmaker.lib.tools.xml_sheet import get_xml_sheets_paths


def entry_point():
    settings.init()
    XML_SHEETS = get_xml_sheets_paths()
    log = settings.mainlogger
    startup_actions.check_dependencies(euktoeps=settings.euktoeps,
                                       xmllint=settings.xmllint,
                                       lualatex=settings.lualatex,
                                       luaotfload_tool=settings
                                       .luaotfload_tool)
    parser = argparse.ArgumentParser(description='Creates maths exercices '
                                                 'sheets and their solutions.')
    parser.add_argument('-l', '--language', action='store', dest='lang',
                        default=settings.language,
                        help='force the language of the output to LANGUAGE. '
                             'This will override any value you may have set '
                             'in ~/.config/mathmaker/user_config.yaml')
    parser.add_argument('--pdf', action='store_true', dest='pdf_output',
                        help='the output will be in pdf format instead '
                             'of LaTeX')
    parser.add_argument('-d', '--output-directory', action='store',
                        dest='outputdir',
                        default=settings.outputdir,
                        help='where to put the possible output files, like '
                             'pictures. '
                             'This will override any value you may have set '
                             '~/.config/mathmaker/user_config.yaml. '
                             'Left undefined, the default will be current '
                             'directory.')
    parser.add_argument('-f', '--font', action='store',
                        dest='font',
                        default=settings.font,
                        help='The font to use. If it\'s not installed on '
                             'your system, lualatex will not be able '
                             'to compile the document. '
                             'This will override any value you may have set '
                             'in ~/.config/mathmaker/user_config.yaml')
    parser.add_argument('--encoding', action='store',
                        dest='encoding',
                        default=settings.encoding,
                        help='The encoding to use. Take care it\'s available '
                             'on your system, otherwise lualatex will not be '
                             'able to compile the document. '
                             'This will override any value you may have set '
                             'in ~/.config/mathmaker/user_config.yaml')
    parser.add_argument('main_directive', metavar='[DIRECTIVE|FILE]',
                        help='this can either match a sheetname included in '
                             'mathmaker, or a mathmaker xml file, or it may '
                             'be the special directive "list", that will '
                             'print the complete list and exit.')
    parser.add_argument('--version', '-v',
                        action='version',
                        version=__info__)
    args = parser.parse_args()
    startup_actions.install_gettext_translations(language=args.lang)
    # From now on, settings.language has its definitive value
    settings.outputdir = args.outputdir
    settings.font = args.font
    settings.encoding = args.encoding
    settings.locale = settings.language + '.' + settings.encoding
    locale.setlocale(locale.LC_ALL, settings.locale)
    startup_actions.check_settings_consistency()
    shared.init()

    if args.main_directive == 'list':
        sys.stdout.write(list_sheets.list_all_sheets())
        shared.db.close()
        sys.exit(0)
    elif args.main_directive in sheet.AVAILABLE:
        sh = sheet.AVAILABLE[args.main_directive][0]()
    elif args.main_directive in XML_SHEETS:
        sh = sheet.S_Generic(filename=XML_SHEETS[args.main_directive])
    elif os.path.isfile(args.main_directive):
        sh = sheet.S_Generic(filename=args.main_directive)
    else:
        log.error(args.main_directive
                  + " is not a correct directive for " + __software_name__
                  + ", you can run `mathmaker list` to get the complete "
                  "list of directives.")
        # print("--- {sec} seconds ---"\
        #      .format(sec=round(time.time() - start_time, 3)))
        shared.db.close()
        sys.exit(1)

    try:
        shared.machine.write_out(str(sh), pdf_output=args.pdf_output)
    except Exception:
        log.error("An exception occured during the creation of the sheet.",
                  exc_info=True)
        shared.db.close()
        sys.exit(1)

    shared.db.commit()
    shared.db.close()
    log.info("Done.")
    sys.exit(0)


if __name__ == '__main__':
    entry_point()
    # print("--- {sec} seconds ---".format(sec=time.time() - start_time))
