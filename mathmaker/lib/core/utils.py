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


# --------------------------------------------------------------------------
##
#   @brief Returns the reduced Product made from the given literals list
#   For example, [x, x², x**6] would return [x**9].
#   Notice that the Items' sign isn't managed here
#   @param provided_list The literal Items list
def reduce_literal_items_product(provided_list):
    from mathmaker.lib.core.base_calculus import Item, Product
    aux_dict = {}

    if not isinstance(provided_list, list):
        raise TypeError('A list is expected, not a '
                        + str(type(provided_list)))

    for i in range(len(provided_list)):
        if isinstance(provided_list[i], Item):
            if provided_list[i].is_literal():
                if provided_list[i].raw_value not in aux_dict:
                    aux_dict[provided_list[i].raw_value] = \
                        provided_list[i].exponent.raw_value
                else:
                    aux_dict[provided_list[i].raw_value] += \
                        provided_list[i].exponent.raw_value
        elif isinstance(provided_list[i], Product):
            if len(provided_list[i].factor) == 1:
                if isinstance(provided_list[i].factor[0], Item):
                    if provided_list[i].factor[0].is_literal():
                        if (provided_list[i].factor[0].raw_value
                            not in aux_dict):
                            # __
                            aux_dict[provided_list[i].factor[0].raw_value] = \
                                provided_list[i].exponent \
                                * provided_list[i].factor[0].exponent
                        else:
                            aux_dict[provided_list[i].factor[0].raw_value] += \
                                provided_list[i].exponent \
                                * provided_list[i].factor[0].exponent
                    else:
                        raise TypeError('A literal Item was expected, not '
                                        'a numeric one.')
                else:
                    raise TypeError('Expected an Item, not a '
                                    + str(type(provided_list[i].factor[0])))
            else:
                raise ValueError('A list of length 1 was expected, not a '
                                 'list of length '
                                 + str(len(provided_list[i].factor)))
        else:
            raise TypeError('A Product was expected, not a '
                            + str(type(provided_list[i])))

    reduced_list = []

    for key in aux_dict:
        reduced_list.append(Item(('+', key, aux_dict[key])))

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
    from mathmaker.lib.core.base_calculus import Sum
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
        new_coeff_sum = Sum([associated_coeff])
        lexi[provided_key] = new_coeff_sum


def gather_literals(xpr):
    """
    Return all literal Values|AngleItems of an expression.

    :param xpr: the expression to iter over
    :type xpr: Calculable
    """
    from mathmaker.lib.core.root_calculus import Value, Calculable
    from mathmaker.lib.core.base_calculus import AngleItem

    if not isinstance(xpr, Calculable):
        raise TypeError('Expected a Calculable, not a ' + str(type(xpr)))

    if (isinstance(xpr, Value) or isinstance(xpr, AngleItem)):
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
#   @brief Checks if the literals of a *Equality|*Expression can be replaced
#   @param objcts The list of literal expressions (or a list of lists of such)
#   @param subst_dict The dictionnary to use
#   @param how_many To tell if all the literals must be replaced
#                   ('all'|'all_but_one'|'at_least_one'|int)
#   @return True|False
def check_lexicon_for_substitution(objcts, subst_dict, how_many):
    from mathmaker import settings
    from mathmaker.lib.core.root_calculus import Value, Calculable
    from mathmaker.lib.core.base_calculus import AngleItem

    log = settings.dbg_logger.getChild('Utils.check_lexicon_for_substitution')
    literals_list = []

    if not (how_many == 'all' or how_many == 'all_but_one'
            or how_many == 'at_least_one' or type(how_many) == int):
        # __
        raise ValueError('Argument how_many should contain '
                         "'all'|'all_but_one'|'at_least_one' or an int, "
                         'not ' + str(how_many))

    if not type(objcts) == list:
        raise TypeError('Expected a list, not a ' + str(type(objcts)))

    # If objcts is a list of lists of Calculables, we "unpack" it before
    # checking its elements.
    if all(isinstance(elt, list) for elt in objcts):
        objcts = [e for elt in objcts for e in elt]

    for elt in objcts:
        if not isinstance(elt, Calculable):
            raise TypeError('Expected a Calculable, not a ' + str(type(elt)))

    if not type(subst_dict) == dict:
        raise TypeError('Expected a dict, not a ' + str(type(subst_dict)))

    for elt in subst_dict:
        if not ((isinstance(elt, Value) or isinstance(elt, AngleItem))
                and elt.is_literal()
                and isinstance(subst_dict[elt], Value)
                and subst_dict[elt].is_numeric()):
            # __
            raise TypeError('{{key: value}} pairs should be of type '
                            '{{literal Value|AngleItem: numeric Value}}, '
                            'got instead: '
                            '{kv}: {vv}'
                            .format(kv=str(type(elt)),
                                    vv=str(type(subst_dict[elt]))
                                    ))

    # Make the list of all literals
    for xpr in objcts:
        literals_list += gather_literals(xpr)
    literals_list = list(set(literals_list))

    log.debug('literals_list= ' + repr(literals_list))
    log.debug('subst_dict= ' + repr(subst_dict))

    subst_dict_copy = {}
    for key in subst_dict:
        subst_dict_copy[key] = subst_dict[key].clone()

    # Now check if the literals of the expressions are all in the lexicon
    n = 0
    N = len(literals_list)
    for i in range(len(literals_list)):
        collected_keys = []
        for key in subst_dict_copy:
            if key == literals_list[i]:
                n += 1
                collected_keys += [key]
        for k in collected_keys:
            subst_dict_copy.pop(k)

    if len(subst_dict_copy) != 0:
        log.debug('return False because len(subst_dict_copy) != 0 '
                  'what means that some of the literals of subst_dict are not '
                  'found in the expression.')
        return False

    if how_many == 'all':
        log.debug('Case all, return {r}'.format(r=(n == N)))
        return n == N
    elif how_many == 'all_but_one':
        log.debug('Case all_but_one, return {r}'.format(r=(n == N - 1)))
        return n == N - 1
    elif how_many == 'at_least_one':
        log.debug('Case at_least_one, return {r}'.format(r=(n >= 1)))
        return n >= 1
    else:
        log.debug('Case fixed number, return {r}'.format(r=(n == how_many)))
        return n == how_many
