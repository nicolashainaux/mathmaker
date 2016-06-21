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
import copy
import re

from mathmaker import settings
from mathmaker.lib import error
from mathmaker.lib import shared
from mathmaker.lib.core.root_calculus import Unit, Value
from mathmaker.lib.common.cst import (UNIT_KINDS, COMMON_LENGTH_UNITS,
                                      CURRENCIES_DICT)


# --------------------------------------------------------------------------
##
#   @brief Returns the word wrapped between the two given strings.
def wrap(word, braces='{}', o_str=None, e_str=None):
    opening_str, ending_str = braces
    if o_str not in [None, '']:
        opening_str = o_str
    if e_str not in [None, '']:
        ending_str = e_str
    return opening_str + word + ending_str


# --------------------------------------------------------------------------
##
#   @brief Returns the word but with removed first and last char, plus
#          possibly following punctuation.
def unwrapped(word):
    if (word.endswith('.') or word.endswith(',')
        or word.endswith(':') or word.endswith(';')
        or word.endswith('?') or word.endswith('!')):
        return word[1:-2]
    else:
        return word[1:-1]


# --------------------------------------------------------------------------
##
#   @brief Returns True if word is wrapped by opening_str and ending_str
def is_wrapped(word, braces='{}'):
    opening_str, ending_str = braces
    return word.startswith(opening_str) and word.endswith(ending_str)


# --------------------------------------------------------------------------
##
#   @brief Returns True if word is wrapped by opening_str and ending_str or
#          ending_str plus a punctuation.
def is_wrapped_p(word, braces='{}'):
    opening_str, ending_str = braces
    return (word.startswith(opening_str)
            and (word.endswith(ending_str)
                 or word.endswith(ending_str + ".")
                 or word.endswith(ending_str + ",")
                 or word.endswith(ending_str + ":")
                 or word.endswith(ending_str + ";")
                 or word.endswith(ending_str + "?")
                 or word.endswith(ending_str + "!")))


# --------------------------------------------------------------------------
##
#   @brief Returns True if word is wrapped by opening_str and ending_str plus
#          a punctuation.
def is_wrapped_P(word, braces='{}'):
    opening_str, ending_str = braces
    return (word.startswith(opening_str)
            and (word.endswith(ending_str + ".")
                 or word.endswith(ending_str + ",")
                 or word.endswith(ending_str + ":")
                 or word.endswith(ending_str + ";")
                 or word.endswith(ending_str + "?")
                 or word.endswith(ending_str + "!")))


# --------------------------------------------------------------------------
##
#   @brief Returns True if word is a "unit" tag (e.g. ends with _unit})
def is_unit(word):
    return (is_wrapped(word) and word[1:-1].endswith("_unit")) \
        or (is_wrapped_P(word) and word[1:-2].endswith("_unit"))


# --------------------------------------------------------------------------
##
#   @brief Returns True if word is a "unit" tag (e.g. ends with _unitN})
def is_unitN(word):
    return (is_wrapped(word) and word[1:-2].endswith("_unit")) \
        or (is_wrapped_P(word) and word[1:-3].endswith("_unit"))


# --------------------------------------------------------------------------
##
#   @brief Returns a couple (sentence_without_hint, hint). Take care, only
#          one hint will be taken into account.
def cut_off_hint_from(sentence):
    last_word = sentence.split()[-1:][0]
    hint_block = ""
    if (is_wrapped(last_word, braces='||')
        and last_word[1:-1].startswith('hint:')):
        # __
        hint_block = last_word
    if len(hint_block):
        new_s = " ".join(w for w in sentence.split() if w != hint_block)
        hint = hint_block[1:-1].split(sep=':')[1]
        return (new_s, hint)
    else:
        return (sentence, "")


# --------------------------------------------------------------------------
##
#   @brief  Will set a random name to all {name}, {nameN}, {masculine_name},
#           {masculine_nameN}, {feminine_name} and {feminine_nameN} tags.
#   @param  arg The object to check (whether it has these attributes or not)
def handle_valueless_names_tags(arg, sentence):
    valueless_nameblocks = [w[1:-1] for w in sentence.split()
                            if ('=' not in w
                                and is_wrapped(w)
                                and (w[1:].startswith('name')
                                     or w[1:].startswith('masculine_name')
                                     or w[1:].startswith('feminine_name')))] \
        + [w[1:-2] for w in sentence.split()
           if ('=' not in w
               and is_wrapped_P(w)
               and (w[1:].startswith('name')
                    or w[1:].startswith('masculine_name')
                    or w[1:].startswith('feminine_name')))]
    for vn in valueless_nameblocks:
        if not hasattr(arg, vn):
            val = ""
            if vn.startswith('name'):
                val = next(shared.names_source)
            elif vn.startswith('masculine_name'):
                val = shared.names_source.next(gender="masculine")
            elif vn.startswith('feminine_name'):
                val = shared.names_source.next(gender="feminine")
            setattr(arg, vn, val)


# --------------------------------------------------------------------------
##
#   @brief  Will set missing attributes matching the {*_unit} and {*_unitN}
#           tags. <*_unit> and <*_unitN> are also handled by this function.
#   @param  arg The object to check (whether it has the attributes or not)
def handle_valueless_unit_tags(arg, sentence):
    valueless_unitblocks = [w[1:-1] for w in sentence.split()
                            if ('=' not in w
                                and (is_wrapped(w)
                                     or is_wrapped(w, braces='<>'))
                                and (w[:-1].endswith('_unit')
                                     or w[:-2].endswith('_unit')))] \
        + [w[1:-2] for w in sentence.split()
           if ('=' not in w
               and (is_wrapped_P(w) or is_wrapped_P(w, braces='<>'))
               and (w[:-2].endswith('_unit') or w[:-3].endswith('_unit')))]
    d = copy.deepcopy(UNIT_KINDS)
    d.update({'area': COMMON_LENGTH_UNITS, 'volume': COMMON_LENGTH_UNITS})
    area_or_volume_tags = []
    for vu in valueless_unitblocks:
        unit_kind, unit_id = vu.split(sep="_")
        if not hasattr(arg, vu):
            if unit_kind == 'currency':
                val = CURRENCIES_DICT[settings.currency]
                setattr(arg, vu, val)
            elif unit_kind in ['length', 'mass', 'capacity']:
                val = random.choice(d[unit_kind])
                setattr(arg, vu, val)
            elif unit_kind in ['area', 'volume']:
                area_or_volume_tags.append(vu)
            else:
                raise error.OutOfRangeArgument(unit_kind, str(d.keys()))
    for vu in area_or_volume_tags:
        unit_kind, unit_id = vu.split(sep="_")
        val = random.choice(d['length'])
        if hasattr(arg, 'length_' + unit_id):
            val = getattr(arg, 'length_' + unit_id)
        else:
            setattr(arg, 'length_' + unit_id, val)
        setattr(arg, vu, val)


# --------------------------------------------------------------------------
##
#   @brief  Builds a dictionary from all {key=val} occurrences found in
#           sentence. All {key=val} occurrences are then replaced by {key} in
#           the sentence. All <key=val> occurrences will be handled in the same
#           way (and replaced by a single {key} too).
#   @return A couple: (transformed_sentence, {key:val, ...}).
def process_attr_values(sentence):
    attr_values = {}
    key_val_blocks = [w for w in sentence.split()
                      if ((is_wrapped_p(w)
                           or is_wrapped_p(w, braces='<>'))
                          and '=' in w)]
    for kv in key_val_blocks:
        [key, val] = unwrapped(kv).split(sep='=')
        attr_values.update({key: val})
    pairs_to_add = {}
    for key in attr_values:
        if key.startswith('area_unit') or key.startswith('volume_unit'):
            _, unit_id = key.split(sep="_")
            if not 'length_' + unit_id in attr_values:
                pairs_to_add.update({'length_' + unit_id: attr_values[key]})
    attr_values.update(pairs_to_add)
    transformed_sentence = " ".join([wrap(w[1:-1].split(sep='=')[0])
                                     if ((is_wrapped(w)
                                          or is_wrapped(w, braces='<>'))
                                         and '=' in w)
                                     else w
                                     for w in sentence.split()])
    transformed_sentence = " ".join([wrap(w[1:-2].split(sep='=')[0],
                                          e_str='}' + w[-1:])
                                     if ((is_wrapped_P(w)
                                          or is_wrapped_P(w, braces='<>'))
                                         and '=' in w)
                                     else w
                                     for w in transformed_sentence.split()])
    return (transformed_sentence, attr_values)


# --------------------------------------------------------------------------
##
#   @brief  Turn all occurences of {nbN} {*_unit} into single {nbN_*_unit} and
#           sets as matching attribute 'nbN_*_unit' with the resulting string
#           of Item(nbN, unit=*_unit)
def merge_nb_unit_pairs(arg):
    logger = settings.dbg_logger.getChild('wording.merge_nb_unit_pairs')
    logger.debug("Retrieved wording: " + arg.wording + "\n")
    new_words_list = []
    words = arg.wording.split()
    skip_next_w = False
    for i, w in enumerate(words):
        next_w = words[i + 1] if i <= len(words) - 2 else None
        logger.debug("w= " + w + " next_w= " + str(next_w))
        next_w_is_a_unit = False
        if next_w is not None and (is_unit(next_w) or is_unitN(next_w)):
            next_w_is_a_unit = True
        logger.debug(" next_w_is_a_unit: " + str(next_w_is_a_unit) + "\n")
        if is_wrapped(w) and w[1:3] == "nb" and next_w_is_a_unit:
            n = w[1:-1]
            u = ""
            if is_wrapped(next_w):
                u = next_w[1:-1]
                p = ""
            elif is_wrapped_P(next_w):
                u = next_w[1:-2]
                p = next_w[-1]
            new_attr_name = n + "_" + u
            expnt = 1
            if u.startswith('area'):
                expnt = 2
            elif u.startswith('volume'):
                expnt = 3
            new_val = Value(getattr(arg, n),
                            unit=Unit(getattr(arg, u),
                                      exponent=Value(expnt)))\
                .into_str(display_SI_unit=True)
            new_words_list += ["{" + new_attr_name + "}" + p]
            setattr(arg, new_attr_name, new_val)
            skip_next_w = True
        elif skip_next_w:
            skip_next_w = False
        else:
            new_words_list += [w]
    arg.wording = " ".join(new_words_list)
    logger.debug("Turned into: " + arg.wording + "\n")


# --------------------------------------------------------------------------
##
#   @brief  Returns all values found wrapped in {}.
def extract_formatting_tags_from(s):
    return [w[1:-1] for w in s.split() if is_wrapped(w)] \
        + [w[1:-2] for w in s.split() if is_wrapped_P(w)]


# --------------------------------------------------------------------------
##
#   @brief  Sets or resets the object's attributes according to its 'wording'
#           attribute. Also process the 'wording' attribute.
#   @param  w_object The object having a 'wording' attribute to process.
def setup_wording_format_of(w_object):
    logger = settings.dbg_logger.getChild('wording.setup_wording_format_of')
    logger.debug("---- NEW RAW WORDING\n" + str(w_object.wording) + "\n")
    w_object.wording, hint = cut_off_hint_from(w_object.wording)
    logger.debug("---- same wording, but hintless:\n"
                 + str(w_object.wording) + "\n")
    logger.debug("---- the hint is:\n" + str(hint) + "\n")
    w_object.wording, attr_dict = process_attr_values(w_object.wording)
    logger.debug("---- same wording, but {k=v} have been processed:\n"
                 + str(w_object.wording) + "\n")
    for key in attr_dict:
        setattr(w_object, key, attr_dict[key])
    handle_valueless_names_tags(w_object, w_object.wording)
    handle_valueless_unit_tags(w_object, w_object.wording)
    logger.debug("---- same wording, but {valueless_units} "
                 "have been processed:\n" + str(w_object.wording) + "\n")
    if hint.startswith('area_unit') or hint.startswith('volume_unit'):
        unit_kind, unit_id = hint.split(sep="_")
        if hasattr(w_object, 'length_' + unit_id):
            setattr(w_object, hint, getattr(w_object, 'length_' + unit_id))
        else:
            raise error.ImpossibleAction("display " + hint + " as hint while "
                                         "no length_" + unit_id + " has "
                                         "been defined already.")

    merge_nb_unit_pairs(w_object)

    for attr in vars(w_object):
        logger.debug("attr: " + str(attr) + "\n")
        if ((attr.endswith('_unit') or attr[:-1].endswith('_unit'))
            and not (attr.startswith('nb') or attr.startswith('currency'))):
            # __
            logger.debug("(re)defining: " + attr + "\n")
            n = 1
            if attr.startswith('area'):
                n = 2
            elif attr.startswith('volume'):
                n = 3
            setattr(w_object, attr,
                    Unit(getattr(w_object, attr), exponent=n)
                    .into_str(display_SI_unit=True))

    setattr(w_object, 'wording_format', {})
    for attr in extract_formatting_tags_from(w_object.wording):
        logger.debug("Found attr: " + attr + "\n")
        w_object.wording_format.update({attr: getattr(w_object, attr)})

    # If the extracted hint refers to another attribute of the question,
    # then this attribute's content will be put in self.hint, otherwise
    # the raw hint content will be taken into account.
    # For instance, if the block was |hint:length_unit| AND there is
    # a self.length_unit defined, then self.hint will get the same
    # value as self.length_unit.
    if len(hint):
        if hasattr(w_object, hint):
            logger.debug("Retrieving as hint value: "
                         + getattr(w_object, hint) + "\n")
            w_object.hint = getattr(w_object, hint)
        else:
            logger.debug("Setting as hint value: " + hint + "\n")
            w_object.hint = hint


# --------------------------------------------------------------------------
##
#   @brief  Insert nonbreaking spaces instead of spaces between a number and
#           the following word.
def insert_nonbreaking_spaces(sentence):
    logger = settings.dbg_logger.getChild('wording.insert_nonbreaking_spaces')
    nb_space = shared.markup['nonbreaking_space']
    p = re.compile(r'(\d)(\s)(\w+)', re.LOCALE)
    logger.debug(sentence + "\n")
    sentence = p.sub(r'\1' + nb_space + r'\3', sentence)
    logger.debug("--> " + sentence + "\n")
    return sentence


# --------------------------------------------------------------------------
##
#   @brief  Applies post process on a sentence (without {tags}).
def post_process(sentence):
    return insert_nonbreaking_spaces(sentence)
