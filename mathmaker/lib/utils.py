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

from decimal import Decimal

import lib.core.base_calculus
from . import error





# --------------------------------------------------------------------------
##
#   @brief Returns the reduced Product made from the given literals list
#   For example, [x, x², x**6] would return [x**9].
#   Notice that the Items' sign isn't managed here
#   @param provided_list The literal Items list
def reduce_literal_items_product(provided_list):
    aux_dict = {}

    if not isinstance(provided_list, list):
        raise error.UncompatibleType(provided_list, "A list")

    for i in range(len(provided_list)):
        if isinstance(provided_list[i], lib.core.base_calculus.Item):
            if provided_list[i].is_literal():
                if not provided_list[i].raw_value in aux_dict:
                    aux_dict[provided_list[i].raw_value] =         \
                                    provided_list[i].exponent.raw_value
                else:
                    aux_dict[provided_list[i].raw_value] +=        \
                                    provided_list[i].exponent.raw_value
        elif isinstance(provided_list[i], lib.core.base_calculus.Product):
            if len(provided_list[i].factor) == 1:
                if isinstance(provided_list[i].factor[0],
                              lib.core.base_calculus.Item):
                    if provided_list[i].factor[0].is_literal():
                        if not provided_list[i].factor[0].raw_value in aux_dict:
                            aux_dict[provided_list[i].factor[0].raw_value] =  \
                                          provided_list[i].exponent           \
                                          * provided_list[i].factor[0].exponent
                        else:
                            aux_dict[provided_list[i].factor[0].raw_value] += \
                                           provided_list[i].exponent          \
                                          * provided_list[i].factor[0].exponent
                    else:
                        raise error.UncompatibleType(                         \
                                              provided_list[i].factor[0],     \
                                              "This Item should be a literal")
                else:
                    raise error.UncompatibleType(provided_list[i].factor[0],  \
                                               "This object should be an Item")
            else:
                raise error.UncompatibleType(provided_list[i],                \
                                          "This Product should contain exactly\
                                          one object (and this should be a \
                                          literal Item)")
        else:
            raise error.UncompatibleType(provided_list[i],                    \
                                       "A literal Item or a Product \
                                       containing only one literal Item")

    reduced_list = []

    for key in aux_dict:
        aux_item = lib.core.base_calculus.Item(('+', key, aux_dict[key]))
        reduced_list.append(aux_item)

    return sorted(reduced_list, key=lambda elt: elt.get_first_letter())





# --------------------------------------------------------------------------
##
#   @brief A substitute for append() in a special case, for dictionaries
#   This method checks if a "provided_key" is already in the lexicon.
#   If yes, then the associated_coeff term is added to the matching Sum.
#   If not, the key is created and a Sum is associated which will contain
#   associated_coeff as only term.
#   @param  provided_key The key to use
#   @param  associated_coeff The value to save in the or add to the Sum
#   @param  lexi The dictionary where to put the couple key/coeff
def put_term_in_lexicon(provided_key, associated_coeff, lexi):
    # This flag will remain False as long as the key isn't found in the lexicon
    key_s_been_found = False

    # We check the lexicon's keys one after the other
    # IMPORTANT NOTICE: the 'in' operator can't be used because it returns
    # True ONLY if the SAME OBJECT has been used as a key (and will return
    # False if another object of same kind and content is already there)
    for key in lexi:
        if provided_key == key:
            # it is important to use the key that was already there to put the
            # new coefficient in the lexicon
            lexi[key].append(associated_coeff)
            key_s_been_found = True

    if not key_s_been_found:
        new_coeff_sum = lib.core.base_calculus.Sum([associated_coeff])
        lexi[provided_key] = new_coeff_sum





# --------------------------------------------------------------------------
##
#   @brief Gather all literal Values of an expression
#   @param xpr The (Calculable) expression to iter over
#   @return [literal Values]
def gather_literals(xpr):
    if not isinstance(xpr, lib.core.base_calculus.Calculable):
        raise error.UncompatibleType(xpr, " Calculable ")

    if isinstance(xpr, lib.core.base_calculus.Value):
        if xpr.is_literal():
            return [xpr]
        else:
            return []
    else:
        result = []
        for elt in xpr:
            result += gather_literals(elt)
        return result





# --------------------------------------------------------------------------
##
#   @brief Purges the given list from duplicates elements
#   @param l The list
#   @return [list purged from duplicates elements]
def purge_from_duplicates(l):
    result = []

    for elt in l:
        if not elt in result:
            result += [elt]

    return result




# --------------------------------------------------------------------------
##
#   @brief Checks if the literals of a *Equality|*Expression can be replaced
#   @param objcts The list of literal expressions
#   @param subst_dict The dictionnary to use
#   @param how_many To tell if all the literals must be replaced
#                   ('all'|'all_but_one'|'at_least_one'|int)
#   @return True|False
def check_lexicon_for_substitution(objcts, subst_dict, how_many):
    literals_list = []

    if not (how_many == 'all' or how_many == 'all_but_one' \
            or how_many == 'at_least_one' or type(how_many) == int):
    #___
        raise error.UncompatibleType(how_many, " 'all'|'all_but_one'" \
                                               + "|'at_least_one'|int ")

    if not type(objcts) == list:
        raise error.UncompatibleType(objcts, " list ")

    for elt in objcts:
        if not isinstance(elt, lib.core.base_calculus.Calculable):
            raise error.UncompatibleType(elt, " Calculable ")

    if not type(subst_dict) == dict:
        raise error.UncompatibleType(subst_dict, " dict ")

    for elt in subst_dict:
        if not (isinstance(elt, lib.core.base_calculus.Value) \
                and elt.is_literal() \
                and isinstance(subst_dict[elt], lib.core.base_calculus.Value) \
                and subst_dict[elt].is_numeric()
                ):
        #___
            raise error.WrongArgument(subst_dict, " this dict should contain " \
                                            + "only " \
                                            + "literal Value: numeric Value")

    # Make the list of all literals
    for xpr in objcts:
        literals_list += gather_literals(xpr)

    #debug_str = ""
    #for l in literals_list:
    #    debug_str += repr(l) + " "
    #print "debug: literals_list = " + debug_str + "\n"

    literals_list = purge_from_duplicates(literals_list)
    #literals_list_bis = []
    #for elt in literals_list:
    #    literals_list_bis += [elt.clone()]

    #debug_str = ""
    #for l in literals_list:
    #    debug_str += repr(l) + " "
    #print "debug: literals_list after purging = " + debug_str + "\n"

    subst_dict_copy = {}
    for key in subst_dict:
        subst_dict_copy[key] = subst_dict[key].clone()

    #for k in subst_dict_copy:
    #    print "debug: subst_dict_copy[" + repr(k) + "] = " + repr(subst_dict_copy[k]) + "\n"

    # Now check if the literals of the expressions are all in the lexicon
    n = 0
    N = len(literals_list)
    #collected_is= []
    for i in range(len(literals_list)):
        #print "debug: literals_list[" + str(i) + "] = " + repr(literals_list[i]) + " is in subst_dict_copy ? " + str(literals_list[i] in subst_dict_copy) + "\n"
        #if i >= 1:
            #print "debug: checking the keys... "
        collected_keys = []
        for key in subst_dict_copy:
            #print "debug: key = " + repr(k) + " key == literals_list[" + str(i) + "] ? " + str(k == literals_list[i])
            if key == literals_list[i]:
                n += 1
                #collected_is += [i]
                collected_keys += [key]
        for k in collected_keys:
            subst_dict_copy.pop(k)

    #for i in collected_is:
    #    literals_list.pop(i)


        #if literals_list[i] in subst_dict_copy:
        #    print "debug: found one elt \n"
        #    n += 1
        #    literals_list.pop(i)
        #    subst_dict_copy.pop(literals_list[i])

    if not len(subst_dict_copy) == 0:
        #print "debug: quitting here\n"
        return False

    #print "debug: how_many = " + str(how_many) + "\n"

    if how_many == 'all':
        return n == N
    elif how_many == 'all_but_one':
        return n == N - 1
    elif how_many == 'at_least_one':
        #print "debug: n = " + str(n) + "\n"
        return n >= 1
    else:
        return n == how_many

