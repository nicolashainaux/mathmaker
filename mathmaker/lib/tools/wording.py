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

"""Use these functions to process sentences or objects containing a wording."""

import random
import copy
import re

from mathmaker import settings
from mathmaker.lib import error
from mathmaker.lib import shared
from mathmaker.lib.core.root_calculus import Unit, Value
from mathmaker.lib.common.cst import (UNIT_KINDS, COMMON_LENGTH_UNITS,
                                      CURRENCIES_DICT)


def wrap(word: str, braces='{}', o_str=None, e_str=None) -> str:
    """
    Return the word wrapped between the two given strings.

    Using o_str and e_str (e.g. opening str and ending str) will override
    braces content. It's interesting when one want to wrap the word with
    something longer than a char.

    :param word: the chunk of text to be wrapped
    :type word: str
    :param braces: the pair of braces that will wrap the word
    :type braces: str
    :param o_str: prefix the word.
    :type o_str: str
    :param e_str: suffix the word
    :type e_str: str
    :rtype: str

    :Examples:

    >>> wrap('wonderful')
    '{wonderful}'
    >>> wrap('wonderful', braces='<>')
    '<wonderful>'
    >>> wrap('wonderful', o_str='<<', e_str='>>')
    '<<wonderful>>'
    >>> wrap('wonderful', e_str='}*')
    '{wonderful}*'
    """
    opening_str, ending_str = braces
    if o_str not in [None, '']:
        opening_str = o_str
    if e_str not in [None, '']:
        ending_str = e_str
    return opening_str + word + ending_str


def unwrapped(word: str) -> str:
    """
    Remove first and last char plus possible punctuation of word.

    :Examples:

    >>> unwrapped('{word}')
    'word'
    >>> unwrapped('{word},')
    'word'
    >>> unwrapped('{word}:')
    'word'
    """
    if (word.endswith('.') or word.endswith(',')
        or word.endswith(':') or word.endswith(';')
        or word.endswith('?') or word.endswith('!')):
        return word[1:-2]
    else:
        return word[1:-1]


def is_wrapped(word: str, braces='{}', extra_braces='') -> bool:
    """
    Return True if word is wrapped between braces.

    :param word: the word to inspect
    :param braces: to change the default {} braces to something else,
    like [] or <>
    :param extra_braces: to add extra braces around the usual ones. Like in
    ({tag}) or [{tag}]
    :Examples:

    >>> is_wrapped('{word}')
    True
    >>> is_wrapped('{word},')
    False
    >>> is_wrapped('<word>')
    False
    >>> is_wrapped('<word>', braces='<>')
    True
    >>> is_wrapped('({word})')
    False
    >>> is_wrapped('({word})', extra_braces='()')
    True
    >>> is_wrapped('[{word}]', extra_braces='()')
    False
    """
    opening_str, ending_str = braces
    if len(extra_braces) == 2:
        left, right = extra_braces
    else:
        left = right = ''
    return (word.startswith(left + opening_str)
            and word.endswith(ending_str + right))


def is_wrapped_p(word: str, braces='{}', extra_braces='') -> bool:
    """
    Return True if word is wrapped between braces. Punctuation has no effect.

    :param word: the word to inspect
    :param braces: to change the default {} braces to something else,
    like [] or <>
    :param extra_braces: to add extra braces around the usual ones. Like in
    ({tag}) or [{tag}]

    :Examples:

    >>> is_wrapped_p('{word}')
    True
    >>> is_wrapped_p('{word},')
    True
    >>> is_wrapped_p('<word>')
    False
    >>> is_wrapped_p('<word>', braces='<>')
    True
    >>> is_wrapped_p('<word>:', braces='<>')
    True
    >>> is_wrapped_p('({word}).')
    False
    >>> is_wrapped_p('({word}).', extra_braces='()')
    True
    >>> is_wrapped_p('[{word}]?', extra_braces='[]')
    True
    """
    opening_str, ending_str = braces
    if len(extra_braces) == 2:
        left, right = extra_braces
    else:
        left = right = ''
    return (word.startswith(left + opening_str)
            and (word.endswith(ending_str + right)
                 or word.endswith(ending_str + right + ".")
                 or word.endswith(ending_str + right + ",")
                 or word.endswith(ending_str + right + ":")
                 or word.endswith(ending_str + right + ";")
                 or word.endswith(ending_str + right + "?")
                 or word.endswith(ending_str + right + "!")))


def is_wrapped_P(word: str, braces='{}', extra_braces='') -> bool:
    """
    Return True if word is wrapped between braces & followed by a punctuation.

    :param word: the word to inspect
    :param braces: to change the default {} braces to something else,
    like [] or <>
    :param extra_braces: to add extra braces around the usual ones. Like in
    ({tag}) or [{tag}]

    :Examples:

    >>> is_wrapped_P('{word}')
    False
    >>> is_wrapped_P('{word},')
    True
    >>> is_wrapped_P('<word>')
    False
    >>> is_wrapped_P('<word>', braces='<>')
    False
    >>> is_wrapped_P('<word>:', braces='<>')
    True
    >>> is_wrapped_P('({word})', extra_braces='()')
    False
    >>> is_wrapped_P('({word}).', extra_braces='()')
    True
    >>> is_wrapped_P('[{word}]?', extra_braces='[]')
    True
    """
    opening_str, ending_str = braces
    if len(extra_braces) == 2:
        left, right = extra_braces
    else:
        left = right = ''
    return (word.startswith(left + opening_str)
            and (word.endswith(ending_str + right + ".")
                 or word.endswith(ending_str + right + ",")
                 or word.endswith(ending_str + right + ":")
                 or word.endswith(ending_str + right + ";")
                 or word.endswith(ending_str + right + "?")
                 or word.endswith(ending_str + right + "!")))


def is_unit(word: str) -> bool:
    """
    Return True if word is a "unit" tag (e.g. ends with _unit}).

    Punctuation has no effect.

    :param word: the word to inspect
    """
    return (is_wrapped(word) and word[1:-1].endswith("_unit")) \
        or (is_wrapped_P(word) and word[1:-2].endswith("_unit"))


def is_unitN(word):
    """
    Return True if word is a "unitN" tag (e.g. ends with _unitN}).

    Punctuation has no effect.

    :param word: the word to inspect
    """
    return (is_wrapped(word) and word[1:-2].endswith("_unit")) \
        or (is_wrapped_P(word) and word[1:-3].endswith("_unit"))


def cut_off_hint_from(sentence: str) -> tuple:
    """
    Return the sentence and the possible hint separated.

    Only one hint will be taken into account.

    :param sentence: the sentence to inspect
    :type sentence: str
    :rtype: tuple

    :Examples:

    >>> cut_off_hint_from("This sentence has no hint.")
    ('This sentence has no hint.', '')
    >>> cut_off_hint_from("This sentence has a hint: |hint:length_unit|")
    ('This sentence has a hint:', 'length_unit')
    >>> cut_off_hint_from("Malformed hint:|hint:length_unit|")
    ('Malformed hint:|hint:length_unit|', '')
    >>> cut_off_hint_from("Malformed hint: |hint0:length_unit|")
    ('Malformed hint: |hint0:length_unit|', '')
    >>> cut_off_hint_from("Two hints: |hint:unit| |hint:something_else|")
    ('Two hints: |hint:unit|', 'something_else')
    """
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


def handle_valueless_names_tags(arg: object, sentence: str):
    """
    Each {name} tag found triggers an arg.name attribute to be randomly set.

    All concerned tags are: {name}, {nameN}, {masculine_name},
    {masculine_nameN}, {feminine_name}, {feminine_nameN}.

    If the tag embbeds a value, like in {name=John}, then it's ignored by this
    function. If arg already has an attribute matching the tag, then it's also
    ignored by this function.

    Now, say arg has no attributes like name, name1, etc. then, if sentence
    contains:

    * "{name}" then arg.name will receive a random name.
    * "{name1}", then arg.name1 will receive a random name.
    * "{name=Michael}", then this function ignores it.
    * "{feminine_name}", then arg.feminine_name will get a random feminine
      name.

    :param arg: the object that attributes must be checked and possibly set
    :param sentence: the sentence where to look for "name" tags.
    """
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


def handle_valueless_unit_tags(arg: object, sentence: str):
    r"""
    Each {\*_unit} tag triggers an arg.\*_unit attribute to be randomly set.

    For instance, if {length_unit} is found, then arg.length_unit will get a
    random length unit.
    Moreover, if {area_unit} or {volume_unit} are found, arg.length_unit is
    set accordingly too. If arg.length_unit does already exist,
    then arg.area_unit will be set accordingly (and not randomly any more).

    {\*_unitN}, <\*_unit> and <\*_unitN> tags will be handled the same way
    by this function.

    If the tag embbeds a value, like in {capacity_unit=dL}, then it's ignored
    by this function. If arg already has an attribute matching the tag, then
    it's also ignored by this function.

    :param arg: the object that attributes must be checked and possibly set
    :type arg: object
    :param sentence: the sentence where to look for "unit" tags.
    :type sentence: str
    :rtype: None
    """
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


def process_attr_values(sentence: str) -> tuple:
    """
    Build a dict with all {key=val} occurrences in sentence. Update such tags.

    All {key=val} occurrences will be replaced by {key}.

    :param sentence: the sentence to process
    :return: this couple: (transformed_sentence, {key:val, ...})
    """
    attr_values = {}
    key_val_blocks = [w for w in sentence.split()
                      if ((is_wrapped_p(w)
                           or is_wrapped_p(w, braces='<>')
                           or is_wrapped_p(w, extra_braces='()')
                           or is_wrapped_p(w, extra_braces='[]'))
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


def merge_nb_unit_pairs(arg: object, w_prefix=''):
    r"""
    Merge all occurences of {nbN} {\*_unit} in arg.wording into {nbN\_\*_unit}.

    In the same time, the matching attribute arg.nbN\_\*_unit is set with
    Value(nbN, unit=Unit(arg.\*_unit)).into_str(display_SI_unit=True)
    (the possible exponent is taken into account too).

    :param arg: the object whose attribute wording will be processed. It must
      have a wording attribute as well as nbN and \*_unit attributes.
    :type arg: object
    :rtype: None

    :Example:

    >>> class Object(object): pass
    ...
    >>> arg = Object()
    >>> arg.wording = 'I have {nb1} {capacity_unit} of water.'
    >>> arg.nb1 = 2
    >>> arg.capacity_unit = 'L'
    >>> merge_nb_unit_pairs(arg)
    >>> arg.wording
    'I have {nb1_capacity_unit} of water.'
    >>> arg.nb1_capacity_unit
    '\\SI{2}{L}'
    """
    w_object_wording = getattr(arg, w_prefix + 'wording')
    logger = settings.dbg_logger.getChild('wording.merge_nb_unit_pairs')
    logger.debug("Retrieved wording: " + w_object_wording + "\n")
    new_words_list = []
    words = w_object_wording.split()
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
            logger.debug(" setattr: name=" + str(new_attr_name) + "; val= "
                         + str(new_val) + "\n")
            setattr(arg, new_attr_name, new_val)
            skip_next_w = True
        elif skip_next_w:
            skip_next_w = False
        else:
            new_words_list += [w]
    new_wording = " ".join(new_words_list)
    logger.debug(" setattr: name=" + w_prefix + 'wording' + "; val= "
                 + new_wording + "\n")
    setattr(arg, w_prefix + 'wording', new_wording)


def extract_formatting_tags_from(s: str):
    """
    Return all tags found wrapped in {}. Punctuation has no effect.

    :param s: the sentence where to look for {tags}.
    """
    return [w[1:-1] for w in s.split() if is_wrapped(w)] \
        + [w[1:-2] for w in s.split() if is_wrapped_P(w)] \
        + [w[2:-2] for w in s.split() if is_wrapped(w, extra_braces='()')] \
        + [w[2:-3] for w in s.split() if is_wrapped_P(w, extra_braces='()')] \
        + [w[2:-2] for w in s.split() if is_wrapped(w, extra_braces='[]')] \
        + [w[2:-3] for w in s.split() if is_wrapped_P(w, extra_braces='[]')]


def wrap_latex_keywords(s: str) -> str:
    """
    Replace some {kw} by {{kw}}, to prevent format() from using them as keys.
    """
    # First, we replace the {numbers} by {{numbers}}
    p = re.compile(r'{(\d{1,}\.?\,?\d*(?:pt|em|cm)*)}', re.LOCALE)
    s = p.sub(r'{{\1}}', s)
    for w in ['multicols', 'multicols*', 'tabular', 'tikzpicture',
              '\centering']:
        s = s.replace('{' + w + '}', '{{' + w + '}}')
    return s


def setup_wording_format_of(w_object: object, w_prefix=''):
    r"""
    Set w_object's attributes according to the tags found in w_object.wording.

    This is the complete process of the wording.
    w_object.wording will also be modified in the process.

    For instance, if w_object.wording is:
    "Here are one {name}, {nb1} {length_unit1} of roads, and a square of
    {nb2} {volume_unit=cm}. What is the side's length of the
    cube? \|hint:length_unit\|"

    Then w_object.wording becomes:
    "Here are one {name}, {nb1_length_unit1} of roads, and a square of
    {nb2_volume_unit}. What is the side's length of the
    cube?"

    w_object.name will be set with a random name,

    w_object.nb1_length_unit1 will be set with:
    '\\SI{<value of nb1>}{<random length unit>}'

    w_object.length_unit will be set to centimeters

    w_object.nb2_volume_unit will be set with:
    '\\SI{<value of nb2>}{cm^{3}}'

    w_object.hint will be set with: 'cm'

    If w_prefix is set, the "wording" processed attributes will be
    w_object.<prefix>wording and w_object.<prefix>wording_format. This allows
    to process several different wordings.

    :param w_object: The object having a 'wording' attribute to process.
    :param w_prefix: The possible prefix of the "wording" attributes to
    process.
    """
    logger = settings.dbg_logger.getChild('wording.setup_wording_format_of')
    w_object_wording = getattr(w_object, w_prefix + 'wording')
    logger.debug("---- NEW RAW WORDING\n" + str(w_object_wording) + "\n")
    w_object_wording, hint = cut_off_hint_from(w_object_wording)
    setattr(w_object, w_prefix + 'wording', w_object_wording)
    logger.debug("---- same wording, but hintless:\n"
                 + str(w_object_wording) + "\n")
    logger.debug("---- the hint is:\n" + str(hint) + "\n")
    w_object_wording, attr_dict = process_attr_values(w_object_wording)
    setattr(w_object, w_prefix + 'wording', w_object_wording)
    logger.debug("---- same wording, but {k=v} have been processed:\n"
                 + str(w_object_wording) + "\n")
    for key in attr_dict:
        setattr(w_object, key, attr_dict[key])
    handle_valueless_names_tags(w_object, w_object_wording)
    handle_valueless_unit_tags(w_object, w_object_wording)
    logger.debug("---- same wording, but {valueless_units} "
                 "have been processed:\n" + str(w_object_wording) + "\n")
    if hint.startswith('area_unit') or hint.startswith('volume_unit'):
        unit_kind, unit_id = hint.split(sep="_")
        if hasattr(w_object, 'length_' + unit_id):
            setattr(w_object, hint, getattr(w_object, 'length_' + unit_id))
        else:
            raise error.ImpossibleAction("display " + hint + " as hint while "
                                         "no length_" + unit_id + " has "
                                         "been defined already.")

    merge_nb_unit_pairs(w_object)
    w_object_wording = getattr(w_object, w_prefix + 'wording')

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

    w_object_wording_format = {}
    for attr in extract_formatting_tags_from(w_object_wording):
        logger.debug("Found attr: " + attr + "\n")
        w_object_wording_format.update({attr: getattr(w_object, attr)})
    setattr(w_object, w_prefix + 'wording_format', w_object_wording_format)

    setattr(w_object, w_prefix + 'wording',
            wrap_latex_keywords(w_object_wording))

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


def insert_nonbreaking_spaces(sentence: str):
    """
    Replace spaces by nonbreaking ones between a number and the next word.

    :param sentence: the sentence to process
    """
    logger = settings.dbg_logger.getChild('wording.insert_nonbreaking_spaces')
    nb_space = shared.markup['nonbreaking_space']
    p = re.compile(r'(\d)(\s)(\w+)', re.LOCALE)
    logger.debug(sentence + "\n")
    sentence = p.sub(r'\1' + nb_space + r'\3', sentence)
    logger.debug("--> " + sentence + "\n")
    return sentence


def post_process(sentence: str):
    """
    Apply all desired post processes to a sentence without {tags}.

    So far, this is only the replacement of spaces following a number and
    preceding a word by nonbreaking spaces.

    :param sentence: the sentence to post process
    """
    return insert_nonbreaking_spaces(sentence)
