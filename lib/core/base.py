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

import subprocess
from lib import error
from lib.common import software
from _version import __version__
from settings import CONFIG

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Clonable
# @brief All objects that are used must be able to be copied deeply
# Any Clonable are provided the clone() method, no need to reimplement it
class Clonable(object):





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a deep copy of the object
    def clone(self):
        result = object.__new__(type(self))
        result.__init__(self)
        return result






# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class NamedObject
# @brief Abstract mother class of objects having a name
class NamedObject(Clonable):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @warning Must be redefined
    def __init__(self):
        raise error.MethodShouldBeRedefined(self, "__init__")





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the name of the object
    @property
    def name(self):
        return self._name





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the name of the object
    @name.setter
    def name(self, arg):
        if not (type(arg) == str or type(arg) == int):
            raise error.WrongArgument(str(type(arg)), "str|int")

        self._name = str(arg)





# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Printable
# @brief All Printable objects: Exponenteds & others (Equations...)
# Any Printable must reimplement the into_str() method
class Printable(NamedObject):





    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        raise error.MethodShouldBeRedefined(self, 'into_str')





# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Drawable
# @brief All Drawable objects. Any Drawable must reimplement into_euk()
# Drawable are not renamable
class Drawable(NamedObject):





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the eukleides filename associated to the triangle
    @property
    def euk_filename(self):
        return self.filename + ".euk"





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the eps filename associated to the triangle
    @property
    def eps_filename(self):
        return self.filename + ".eps"





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the name of the object
    @property
    def name(self):
        return self._name





    # --------------------------------------------------------------------------
    ##
    #   @brief Prevents Drawable objects from being renamed, since they get
    #          their name from other properties inside them.
    @name.setter
    def name(self, arg):
        raise error.ImpossibleAction("rename this object")





    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the euk string to put in the file
    #   @param options Any options
    #   @return The string to put in the picture file
    def into_euk(self, **options):
        raise error.MethodShouldBeRedefined(self, 'into_euk')




    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the picture of the drawable object
    #   @return Nothing, just creates the picture file
    def into_pic(self, **options):
        header_comment = "% " + _(\
                    "{document_format} document generated by {software_ref}")\
                    .format(document_format='eukleides',
                            software_ref=software.NAME_PRINTABLE + " " \
                                         + __version__) + "\n"

        header_comment += "% "+ _(\
                    "{software_ref} is free software. Its license is \
{software_license}.")\
                    .format(software_ref=software.NAME_PRINTABLE,
                            software_license=software.LICENSE) + "\n"

        header_comment += "% " + _(\
                    "Further details on {software_website}")\
                    .format(software_website=software.WEBSITE) + "\n"

        header_comment += "% " + software.COPYRIGHT \
                          + " " + software.AUTHOR +"\n\n"


        if 'create_pic_files' in options \
            and not options['create_pic_files'] in YES:
        #___
            pass

        else:
            f = open(self.euk_filename, 'w')
            f.write(header_comment + self.into_euk(**options))
            f.close()

        path_to_euktoeps = CONFIG["PATHS"]["EUKTOEPS"]
        options_of_euktoeps = CONFIG["PATHS"]["EUKTOEPS_OPTIONS"]

        if 'create_pic_files' in options \
            and not options['create_pic_files'] in YES:
        #___
            pass

        else:
            call_euktoeps = subprocess.Popen([path_to_euktoeps,
                                              options_of_euktoeps,
                                              self.euk_filename
                                              ]
                                             )
