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

import copy
import random
from collections import namedtuple

from intspan import intspan
from intspan.core import ParseError

from mathmaker.lib import shared, error
from mathmaker.lib.common import alphabet
from .X_Structure import X_Structure
from . import question
from .question import Q_Generic

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'': ['default'],
     'std': ['default'],
     'tabular': ['default'],  # reserved to mental calculation
     'slideshow': ['default'],  # reserved to mental calculation
     'bypass': ['']
     }

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']
              }
             }

LAYOUTS = {'default': [None, 'all'],
           '2cols': [['?', 9, 9], 'all'],
           }

to_unpack = copy.deepcopy(question.SUBKINDS_TO_UNPACK)
# In Q_Info below, id is actually kind_subkind
Q_info = namedtuple('Q_info', 'id,kind,subkind,nb_source,options')

MIN_ROW_HEIGHT = 0.8


def get_common_nb_from_pairs_pair(pair):
    """
    Return the common number found in a pair of pairs.

    :param pair: the pair of pairs
    :type pair: a tuple or a list (of two elements)
    :rtype: number
    """
    if pair[0][0] in pair[1]:
        return pair[0][0]
    elif pair[0][1] in pair[1]:
        return pair[0][1]
    else:
        raise ValueError('One of the numbers of the first pair is expected '
                         'to be found in the second pair, but hasn\'nt been.')


def merge_pair_to_tuple(n_tuple, pair, common_nb):
    """
    Add one number from the pair to the n_tuple.

    It is assumed n_tuple and pair both contain common_nb.
    If n_tuple has more than 2 elements, it is also assumed that the first one
    is common_nb. If it has 2 elements, then it might need to get reordered.
    :param n_tuple: a tuple of 2 or more elements
    :type n_tuple: tuple
    :param pair: a tuple of 2 elements. One of them (at least) is common_nb,
    and will be removed, the other one will be added to n_tuple
    :type pair: tuple
    :param common_nb: the number contained in both n_tuple and pair
    :type common_nb: a number
    :rtype: tuple
    """
    if not ((common_nb in n_tuple) and (common_nb in pair)):
        raise ValueError('The number in common ({}) should be present at '
                         'least once in both n_tuple ({}) and pair ({}).'
                         .format(str(common_nb), str(n_tuple), str(pair)))
    elif len(n_tuple) == 2:
        if common_nb != n_tuple[0]:
            # In the case the first number was not the common number, now it is
            n_tuple = (n_tuple[1], n_tuple[0])

    if pair[0] != common_nb:
        n_tuple += (pair[0], )
    else:
        n_tuple += (pair[1], )

    return n_tuple


# --------------------------------------------------------------------------
##
#   @brief Will reorganize the raw questions lists into a dictionary
#   @param  q_list          The questions' list
#   @return (q_dict, q_nb)  The questions' dictionary + the total number of
#                           questions
def build_q_dict(q_list):
    # In q_list, each element is like this:
    # [{'kind':'multi', 'subkind':'direct', 'nb':'int'}, ['table_2_9'], 4]
    # [q[0],                                             q[1],          q[2]]
    q_dict = {}
    already_unpacked = set()
    q_nb = 0
    for q in q_list:
        q_nb += q[2]

        for n in range(q[2]):
            q_id = q[0]['kind']
            q_id += "_"

            # Here we 'unpack' some special subkinds.
            subk = q[0]['subkind']
            if subk in question.UNPACKABLE_SUBKINDS:
                already_unpacked |= {subk}
            elif subk in to_unpack:
                subk_left = to_unpack[subk] - already_unpacked
                if not subk_left:
                    already_unpacked -= copy.deepcopy(
                        question.SUBKINDS_TO_UNPACK[subk])
                    to_unpack[subk] = copy.deepcopy(
                        question.SUBKINDS_TO_UNPACK[subk])
                    subk_left = to_unpack[subk] - already_unpacked
                s = list(subk_left)
                random.shuffle(s)
                subk = s.pop()
                already_unpacked |= {subk}

            q_id += subk
            q_options = copy.deepcopy(q[0])
            q_dict.setdefault(q_id, [])
            q_dict[q_id] += [(q[1], q_options['kind'], subk, q_options)]
            del q_options['kind']
            del q_options['subkind']

    return q_dict, q_nb


# --------------------------------------------------------------------------
##
#   @brief Will create a complete and mixed questions' list from q_dict
#   @param  q_dict  The questions' dictionary
#   @return q_list  The new mixed questions' list
def build_mixed_q_list(q_dict):
    # q_dict is organized like this:
    # { 'multi_direct':   [(['table_2_9'], 'multi', 'direct', {'nb':'int'}),
    #                      (['table_2_9'], 'multi', 'direct', {'nb':'int'})],
    #   'multi_reversed': [(['table_2_9'], 'multi', 'reversed', {options})],
    #   'divi_direct':    [(['table_2_9'], 'divi', 'direct', {options})],
    #   'multi_hole':     [(['table_2_9'], 'multi', 'hole', {options})],
    #   'q_id':           [(['table_15'], 'kind', 'subkind', {options})],
    #   'q_id:            [(['table_25'], 'kind', 'subkind', {options})],
    #   'etc.'
    # }
    mixed_q_list = []
    q_id_box = [key for key in q_dict.keys()
                for i in range(len(q_dict[key]))]
    random.shuffle(q_id_box)
    for q_id in q_id_box:
        info = q_dict[q_id].pop(0)
        mixed_q_list += [Q_info(q_id, info[1], info[2], info[0], info[3])]
    return mixed_q_list


def preprocess_variant(q_i):
    """
    Preprocess question's variant (if necessary)

    :param q_i: the Q_info object, whose fields are
                'id,kind,subkind,nb_source,options'
    :type q_i: Q_info (named tuple)
    """
    if q_i.id in ['priorities_in_calculation_without_parentheses',
                  'priorities_in_calculation_with_parentheses']:
        default_variant = {
            'priorities_in_calculation_without_parentheses':
                {'variant': '0-23'},
            'priorities_in_calculation_with_parentheses':
                {'variant': '100-187'}
        }
        if ('variant' not in q_i.options
            or ('variant' in q_i.options and q_i.options['variant'] == '')):
            q_i.options.update(default_variant[q_i.id])
        try:
            variants_to_pick_from = intspan(q_i.options['variant'])
        except ParseError:
            raise ValueError('Incorrect variant in xml file: {}'
                             .format(q_i.options['variant']))
        raw_query = '('
        last = len(variants_to_pick_from.ranges()) - 1
        for i, r in enumerate(variants_to_pick_from.ranges()):
            if r[0] == r[1]:
                raw_query += 'nb1 = ' + str(r[0])
            else:
                raw_query += '(nb1 >= {} AND nb1 <= {})'.format(r[0], r[1])
            if i < last:
                raw_query += ' OR '
        raw_query += ')'
        q_i.options.update(
            {'variant':
             int(shared
                 .priorities_in_calculation_variants_source
                 .next(**{'raw': raw_query}))})


def auto_adjust_nb_sources(nb_sources: list, q_i: namedtuple):
    """
    Automatically adjust nb_sources for certains questions.

    :param nb_sources: the provided numbers sources
    :param q_i: the Q_info object (namedtuple), whose fields are
                'id,kind,subkind,nb_source,options'
    """
    if q_i.id in ['priorities_in_calculation_without_parentheses',
                  'priorities_in_calculation_with_parentheses']:
        if not len(nb_sources) == 2:
            raise ValueError('There must be two sources for '
                             'priorities_in_calculation_with(out)_parentheses '
                             'questions.')
        if nb_sources[0].startswith('single') and 'pairs' in nb_sources[1]:
            single_nb_source, pairs_nb_source = nb_sources
        elif nb_sources[1].startswith('single') and 'pairs' in nb_sources[0]:
            pairs_nb_source, single_nb_source = nb_sources
        else:
            raise ValueError('One of the two sources for '
                             'priorities_in_calculation_with(out)_parentheses '
                             'questions must be for single numbers, '
                             'the other one for pairs.')
        v = q_i.options['variant']
        if 0 <= v <= 3:
            nb_sources = [single_nb_source, pairs_nb_source]
        elif 4 <= v <= 7:
            nb_sources = [pairs_nb_source, single_nb_source]
        elif 8 <= v <= 15:
            nb_sources = [pairs_nb_source, pairs_nb_source]
        elif 16 <= v <= 23:
            nb_sources = [single_nb_source, pairs_nb_source, single_nb_source]
        elif 100 <= v <= 107:
            nb_sources = [pairs_nb_source]
        elif 108 <= v <= 115:
            nb_sources = [single_nb_source, pairs_nb_source]
        elif 116 <= v <= 147:
            nb_sources = [pairs_nb_source, pairs_nb_source]
        elif 148 <= v <= 155:
            nb_sources = [pairs_nb_source]
        elif 156 <= v <= 187:
            nb_sources = [single_nb_source, pairs_nb_source]
    return nb_sources


# --------------------------------------------------------------------------
##
#   @brief  Determine the
#   @param  q_i     The Q_info object
def get_nb_sources_from_question_info(q_i):
    nb_sources = []
    extra_infos = {'merge_sources': False}
    questions_sources = q_i.nb_source
    if len(q_i.nb_source) == 1:
        if q_i.nb_source[0].startswith('inttriplets_'):
            chunks = q_i.nb_source[0].split(sep='_')
            if not len(chunks) >= 2:
                raise ValueError('Incorrect numbers\' source value in xml '
                                 'file: {}'.format(q_i.nb_source[0]))
            bounds = chunks[1]
            questions_sources = ['intpairs_' + bounds, 'intpairs_' + bounds]
            extra_infos.update({'merge_sources': True})
        elif q_i.nb_source[0].startswith('ext_'):
            chunks = q_i.nb_source[0][4:].split(sep='_')
            if chunks[0] == 'proportionality':
                if chunks[1] == 'quadruplet':
                    questions_sources = ['intpairs_' + chunks[2],
                                         'intpairs_' + chunks[2],
                                         'intpairs_' + chunks[2]]
                    extra_infos.update({'merge_sources': True,
                                        'triangle_inequality': True})
        elif ';;' in q_i.nb_source[0]:
            questions_sources = q_i.nb_source[0].split(sep=';;')
    questions_sources = auto_adjust_nb_sources(questions_sources, q_i)
    for nb_sce in questions_sources:
        tag_to_unpack = nb_source = nb_sce
        extra_kwargs = {}
        if nb_source in question.SOURCES_TO_UNPACK:
            s = ''
            stu = copy.copy(question.SOURCES_TO_UNPACK)
            if nb_source in ['decimal_and_10_100_1000',
                             'decimal_and_one_digit']:
                # __
                s = stu[nb_source][q_i.id]
            else:
                s = stu[nb_source][q_i.subkind]
            s = list(s)
            random.shuffle(s)
            nb_source = s.pop()
            if (tag_to_unpack == 'auto_vocabulary'
                and q_i.subkind in ['addi', 'subtr']
                and nb_source == 'intpairs_2to200'):
                # __
                extra_kwargs.update({'suits_for_deci2': 1})
        if (nb_source.startswith('intpairs')
            and q_i.options.get('nb_variant', '').startswith('decimal1')):
            extra_kwargs.update({'suits_for_deci1': 1})
        if (nb_source.startswith('intpairs')
            and q_i.options.get('nb_variant', '').startswith('decimal2')):
            extra_kwargs.update({'suits_for_deci2': 1})
        nb_sources += [(nb_source, extra_kwargs)]
    return nb_sources, extra_infos


# --------------------------------------------------------------------------
##
#   @brief Increases the disorder of the questions' list
#   @param  l           The list
#   @param  sort_key    The list's objects' attribute that will be used to
#                       determine whether the order should be changed or not
def increase_alternation(l, sort_key):
    if len(l) >= 3:
        for i in range(len(l) - 2):
            if getattr(l[i], sort_key) == getattr(l[i + 1], sort_key):
                if getattr(l[i + 2], sort_key) != getattr(l[i], sort_key):
                    l[i + 1], l[i + 2] = l[i + 2], l[i + 1]

    return l


def numbering_device(numbering_kind='disabled'):
    """
    This generator provides "limitless" new items for numbering questions.

    Possible values of the argument are:
    - 'disabled': an empty string will be returned
    - 'numeric': an integer is returned (until the maximal value is reached,
    but let's consider there won't be that long exercises!)
    - 'alphabetic': a letter is returned (once the alphabet is over, as a
    security, the letter is returned doubled, tripled, etc., thought it is not
    expected to need more than 26 questions in the same exercise.)
    """
    if numbering_kind == 'disabled':
        while True:
            yield ''
    elif numbering_kind == 'numeric':
        i = 0
        while True:
            yield i + 1
            i += 1
    elif numbering_kind in ['alphabet', 'alphabetical', 'default']:
        i = 0
        while True:
            yield alphabet.lowercase[i % 26] * ((i // 26 + 1))
            i += 1


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Generic
# @brief A default 'void' exercise (will get its questions from...)
class X_Generic(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #          - x_kind=<string>
    #                         see AVAILABLE_X_KIND_VALUES to check the
    #                         possible values to use and their matching
    #                         x_subkind options
    #   @return One instance of exercise.Generic
    def __init__(self, **options):
        self.derived = True
        (x_kind, q_list) = options.get('q_list')
        self.q_numbering = options.get('q_numbering', 'disabled')
        self.layout = options.get('layout', 'default')
        if self.layout != 'default':
            l = self.layout.split(sep='_')
            if not len(l) == 2:
                raise error.XMLFileFormatError('A \'layout\' attribute in an '
                                               'exercise should have two '
                                               'parts linked with a _. This '
                                               'is not the case of \'{}\'.'
                                               .format(str(self.layout)))
            exc_l, ans_l = l
            if exc_l not in LAYOUTS:
                raise error.XMLFileFormatError('The first part of the layout '
                                               'value (\'{}\') is not correct.'
                                               ' It should belong to: {}. '
                                               .format(str(exc_l),
                                                       str(
                                                       list(LAYOUTS.keys()))))
            if ans_l not in LAYOUTS:
                raise error.XMLFileFormatError('The second part of the layout '
                                               'value (\'{}\') is not correct.'
                                               ' It should belong to: {}. '
                                               .format(str(ans_l),
                                                       str(
                                                       list(LAYOUTS.keys()))))
            X_LAYOUTS.update({self.layout: {'exc': LAYOUTS[exc_l],
                                            'ans': LAYOUTS[ans_l]}})
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # TEXTS OF THE EXERCISE
        self.text = {'exc': options.get('text_exc', ''),
                     'ans': options.get('text_ans', '')}

        if self.text['exc'] != '':
            self.text['exc'] = _(self.text['exc'])

        if self.text['ans'] != '':
            self.text['ans'] = _(self.text['ans'])

        # From q_list, we build a dictionary and then a complete questions'
        # list:
        q_dict, self.q_nb = build_q_dict(q_list)
        # in case of mental calculation exercises we shuffle the questions
        if self.x_kind in ['tabular', 'slideshow']:
            for key in q_dict:
                random.shuffle(q_dict[key])
        mixed_q_list = build_mixed_q_list(q_dict)
        # in case of mental calculation exercises we shuffle the questions
        if self.x_kind in ['tabular', 'slideshow']:
            mixed_q_list = increase_alternation(mixed_q_list, 'id')
            mixed_q_list.reverse()
            mixed_q_list = increase_alternation(mixed_q_list, 'id')

        # mixed_q_list is organized like this:
        # [('id', 'kind', 'subkind', 'nb_source', 'options'),
        #  ('q_id', 'q', 'id', 'table_15', {'nb':}),
        #  ('multi_direct', 'multi', 'direct', ['table_2_9'], {'nb':}),
        #  etc.
        # ]

        # Now, we generate the numbers & questions, by type of question first
        self.questions_list = []
        last_draw = [0, 0]
        numbering = numbering_device(self.q_numbering)
        for q in mixed_q_list:
            preprocess_variant(q)
            (nbsources_xkw_list, extra_infos) = \
                get_nb_sources_from_question_info(q)
            nb_to_use = tuple()
            common_nb = None
            for (i, (nb_source, xkw)) in enumerate(nbsources_xkw_list):
                if i == 1 and extra_infos['merge_sources']:
                    second_couple_drawn = shared.mc_source\
                        .next(nb_source,
                              either_nb1_nb2_in=last_draw,
                              **question.get_modifier(q.id, nb_source),
                              **xkw)
                    common_nb = get_common_nb_from_pairs_pair(
                        (nb_to_use, second_couple_drawn))
                    nb_to_use = merge_pair_to_tuple(nb_to_use,
                                                    second_couple_drawn,
                                                    common_nb)
                elif i > 1 and extra_infos['merge_sources']:
                    if (i == 2
                        and extra_infos.get('triangle_inequality', False)):
                        # __
                        new_couple_drawn = shared.mc_source\
                            .next(nb_source,
                                  triangle_inequality=nb_to_use,
                                  **question.get_modifier(q.id, nb_source),
                                  **xkw)
                    else:
                        new_couple_drawn = shared.mc_source\
                            .next(nb_source,
                                  either_nb1_nb2_in=[common_nb],
                                  **question.get_modifier(q.id, nb_source),
                                  **xkw)
                    nb_to_use = merge_pair_to_tuple(nb_to_use,
                                                    new_couple_drawn,
                                                    common_nb)
                else:
                    drawn = shared.mc_source.next(nb_source,
                                                  not_in=last_draw,
                                                  **question
                                                  .get_modifier(
                                                      q.id, nb_source),
                                                  **xkw)
                    if isinstance(drawn, int):
                        nb_to_use += (drawn, )
                    else:
                        nb_to_use += drawn
                last_draw = [str(n) for n in set(nb_to_use)
                             if (isinstance(n, int) or isinstance(n, str))]
                if nb_source in ['decimal_and_10_100_1000_for_divi',
                                 'decimal_and_10_100_1000_for_multi']:
                    # __
                    q.options['10_100_1000'] = True
            self.questions_list += \
                [Q_Generic(q.id,
                           q.options,
                           numbers_to_use=nb_to_use,
                           number_of_the_question=next(numbering),)]

        shared.number_of_the_question = 0
