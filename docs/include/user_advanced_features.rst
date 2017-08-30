.. _user_advanced_features:

Advanced features
=================

User settings
-------------

The default settings are following:

.. code-block:: yaml

  PATHS:
      EUKTOEPS: euktoeps
      XMLLINT: xmllint
      LUALATEX: lualatex
      LUAOTFLOAD_TOOL: luaotfload-tool
      MSGFMT: msgfmt
      # OUTPUT_DIR *must* be relative (to user's home)
      OUTPUT_DIR: .mathmaker/outfiles/

  LOCALES:
      # Available values can be checked in the locale directory.
      LANGUAGE: en_US
      ENCODING: UTF-8
      # Values can be 'euro', 'sterling', 'dollar'
      CURRENCY: dollar

  LATEX:
      FONT:
      ROUND_LETTERS_IN_MATH_EXPR: False

  DOCUMENT:
      # Double quotes around the template strings are mandatory.
      # {n} will be replaced by the successive numbering items (1, 2, 3... or
      # a, b, c... etc.)
      QUESTION_NUMBERING_TEMPLATE: "{n}."
      # nothing; bold; italics; underlined
      QUESTION_NUMBERING_TEMPLATE_WEIGHT: bold
      QUESTION_NUMBERING_TEMPLATE_SLIDESHOWS: "{n}."
      QUESTION_NUMBERING_TEMPLATE_SLIDESHOWS_WEIGHT: regular

  DAEMON:
      MATHMAKER_EXECUTABLE: mathmaker


Some explanations:

* The ``PATHS:`` section is here to provide a mean to change the paths to ``euktoeps``, ``lualatex`` and ``xmllint`` mainly. In case one of them is not reachable the way it is set in this section, you can change that easily.

* The ``PATHS:`` section contains also an ``OUTPUT_DIR:`` entry. This is the directory where ``mathmaker`` will store the possible picture files (.euk and .eps). Change it at your liking, but as it must be a subdirectory of user's own directory, it must be a relative path.

* The entries under ``LOCALES:`` allow to change the language, encoding, and default currency used.

* The ``LATEX:`` section contains an entry to set the font to use (be sure it is available on your system). The ``ROUND_LETTERS_IN_MATH_EXPR:`` entry is disabled by default (set to False). If you set it to True, a special font will be used in math expressions, that will turn all letters (especially the 'x') into a rounded version. This is actually the ``lxfonts`` LaTeX package. It doesn't fit well with any font. Using "Ubuntu" as font and setting ``ROUND_LETTERS_IN_MATH_EXPR:`` to True gives a nice result though.

* The entries under ``DOCUMENT:`` allow to change some values to format the output documents.

Your settings file must be ``~/.config/mathmaker/user_config.yaml``.

Command-line options
--------------------

Several command-line options correspond to settings that are defined in ``~/.config/mathmaker/user_config.yaml``. Any option redefined in command-line options will override the setting from the configuration file.

Type ``mathmaker --help`` to get information on these command-line options.

.. _http_server:

http server (mathmakerd)
------------------------

Once everything is installed, it's possible to run a server to communicate with mathmaker through a web browser.

Run the server:

::

    $ mathmakerd start

Then go to your web browser and as url, you can enter:

::

    http://127.0.0.1:9999/?sheetname=<sheetname>

and replace ``<sheetname>`` by an available sheet's name (from ``mathmaker list``), for instance:

::

    http://127.0.0.1:9999/?sheetname=pythagorean-theorem-short-test

``mathmaker`` will create the new sheet, compile it and return the pdf result to be displayed in the web browser.

At the moment, ``mathmakerd stop`` doesn't work correctly, you'll have to ``kill`` it directly (``ps aux | grep mathmakerd`` then ``kill`` with the appropriate pid).

It's possible to pass an IP address in an extra parameter named ``ip``, like:

    http://127.0.0.1:9999/?sheetname=pythagorean-theorem-short-test&ip=127.0.0.1

In this case, ``mathmakerd`` will check if the last request is older than 10 seconds (this is hardcoded, so far) and if not, then a http status 429 will be returned. In order to do that, ``mathmakerd`` uses a small database that it erases when the last request is older than one hour (also hardcoded, so far).


YAML sheets
-----------

As a directive to mathmaker it is possible to give a path to yaml file.

Creating a new yaml file that can be used as a model by ``mathmaker`` is more for advanced users, though it's not that difficult.

Example
^^^^^^^

Let's have a look at ``mathmaker/data/frameworks/algebra/expand.yaml``, where four sheets are defined:

.. code-block:: yaml

  simple: !!omap
    - title: "Algebra: expand simple brackets"
    - exercise: !!omap
      - details_level: medium
      - text_exc: "Expand and reduce the following expressions:"
      - questions: expand simple -> inttriplets_2to9 (5)

  simple_detailed_solutions: !!omap
    - title: "Algebra: expand simple brackets"
    - exercise: !!omap
      - text_exc: "Expand and reduce the following expressions:"
      - questions: expand simple -> inttriplets_2to9 (5)

  double: !!omap
    - title: "Algebra: expand and reduce double brackets"
    - exercise: !!omap
      - details_level: medium
      - text_exc: "Expand and reduce the following expressions:"
      - questions: expand double -> intpairs_2to9;;intpairs_2to9 (5)

  double_detailed_solutions: !!omap
    - title: "Algebra: expand and reduce double brackets"
    - exercise: !!omap
      - text_exc: "Expand and reduce the following expressions:"
      - question: expand double -> intpairs_2to9;;intpairs_2to9 (5)

The four top-level keys are the sheets' names. These names must not contain spaces (not supported).

A list of keys is defined below each sheet's name. No one is mandatory. If you do not define the ``title``, then the default value will be used (for titles, this is an empty string).

Sheet's keys
^^^^^^^^^^^^

Possible keys for sheets, at the moment, are:

- ``preset`` allows to preset a number of other keys. Possible values: ``default``, ``mental_calculation``. Default is ``default``. The ``mental_calculation`` value will remove the exercise's titles and the exercises layout.
- ``header``, ``title``, ``subtitle``, ``text`` allow to customize the header, title, subtitle and text of the sheet. Default value is an empty string for each of them.
- ``answers_title`` allows to customize the title for the answers' sheet. It defaults to ``Answers``.
- ``layout`` contains the layout description of the sheet, if necessary (see below).
- Any key starting with ``exercise`` will contain the list of questions of one exercise. It is not possible to use the same key several times (YAML forbids it), so if you want to define several exercises, say two, for instance, you'll have to use ``exercise`` and ``exercise2``, for instance (if you use numbers, it will have no effect on the order of exercises in the output).

Sheet's layout
^^^^^^^^^^^^^^

.. image:: pics/layout_sheet.png

If a sheet contains no ``layout`` key (or if its value is left empty), then the default layout will be used (all exercises printed one after the other, unlike the 3×2 grid in the figure above).

The ``layout`` key can list a ``unit`` key, whose value will be used for columns widths (see below). ``unit`` defaults to ``cm``.

The ``layout`` key can list a ``font_size_offset`` key, whose value is a relatively small integer allowing to change the font size (for instance, set it at ``+1`` or ``+2`` to enlarge all fonts, or ``-1`` or ``-2`` to reduce all fonts' size)

So far, no ``spacing`` key is available for sheets' ``layout``, but the spacing between exercises can be set in the properties.

Finally, the ``layout`` key can list one ``wordings`` key and/or one ``answers`` key. They allow to define different settings for wordings and answers, but both work the same way.

The properties are defined as key=value pairs separated by commas (actually a comma and a space). For instance: ``rowxcol=?×2, print=3 3``

* ``rowxcol`` can contain ``none`` (default: no layout) or the number of rows and columns as a multiplication of two integers: ``r×c``, for instance: ``3×2``. This would mean 3 rows and 2 columns, what would define 6 "cells", like in the figure above. As a convenience, you can use a x instead of a ×, like this: ``3x2``.

* ``colwidths`` is ignored if ``rowxcol`` contains ``none``. If ``rowxcol`` contains a ``r×c`` definition, then ``colwidths`` defaults to ``auto``: the width of all columns will be calculated automatically (all equal). Otherwise, you can set the values you like, separated by spaces, like: ``4.5 4.5 9`` what would make the two first columns 4.5 units wide and the last, 9 units wide (See ``unit`` key description above). Note that there must be as many values as the number of columns defined in the ``"r×c"`` definition.

* ``print`` is the number of exercises to print, either one after the other, or per "cell". It defaults to ``auto``. If ``rowxcol`` contains ``none``, then ``print`` can either be a natural number (how many exercises/questions to print), or ``auto``, and then all exercises (left) will be printed, without distributing them among columns. If ``rowxcol`` contains a ``r×c`` definition, then an ``auto`` value would mean that each "cell" will contain one question. Otherwise, you can tell how many questions you want in each cell, row after row, as integers separated by spaces, like: ``2 1 1 3 1 1`` what would put (with ``rowxcol=2×3``) 2 questions (or exercises) in the first cell, then 1 question in each other cell of the first row, then 3 questions in the first cell of the second row, and 1 question in each cell left. There must be as many numbers as cells. As a convenience, you can add a ``.`` or a ``/`` to separate the rows, like: ``2 1 1 / 3 1 1`` (These two signs will simply be ignored). Each row must contain as many numbers as defined in the ``r×c`` definition. If the number of rows is left undefined (``?``) then only the first row has to be defined (extra rows will be ignored) as a pattern for all rows (the default still being ``auto``, i.e. 1 question per cell).

* ``newpage`` can be turned to true in order to insert a jump to next page.


Examples of sheet's layouts:
""""""""""""""""""""""""""""

Say you have 4 exercises and you want to put the answers of the two first ones in 2 two columns, and then print the left ones one after another:

.. code-block:: yaml

  layout:
    answers: rowxcol=1×2, print=1 1,
             print=2


ex 1            ex 2

ex 3

ex 4

.. note::

    YAML allows to write the same string ("scalar") on several lines. This is practical for readability. In the example above, we could have written ``rowxcol=1×2, print=1 1, print=2`` all on the same line.

If you have 3 exercises and you want to print 2 answers on a first page, then jump to next page and print the answer of the third one, then your sheet's layout may be:

.. code-block:: yaml

  layout:
    answers: print=2,
             newpage=true,
             print=1


The !!omap label
^^^^^^^^^^^^^^^^

The sheets' names keys as well as the ``exercise`` keys are labeled ``!!omap``. This is required in order to ensure the order of the created sheets will be the same as the one defined in the sheet. Forgetting these labels won't prevent ``mathmaker`` from running, but the final order may be changed (what does not mean it will be randomly reorganized at each run). In this example, this wouldn't have any consequence as there's only one ``exercise`` key in each sheet and only one ``question`` key in each exercise.

Exercise's keys
^^^^^^^^^^^^^^^
Possible keys for sheets, at the moment, are:

* ``preset`` (same as for sheets)

* ``layout_variant`` can be ``default``, ``tabular`` or ``slideshow``.

* ``layout_unit`` defaults to ``cm``.

* ``shuffle`` can be ``true`` or ``false``. It defaults to ``false``, except for ``mental_calculation`` preset. If set to true, then the questions will be shuffled.

* ``details_level`` can be ``maximum`` (default), ``medium`` or ``none`` (default for ``mental_calculation`` preset). Some types of questions can be configured to output the answer with different levels of details.

* ``q_numbering`` defines the numbering of the questions of the exercise. It can be ``default``, ``alphabet``, ``alphabetical``, ``numeric`` or ``disabled``. The three first values are synonyms.

* ``start_number`` defines the first number, when numbering the questions. Must be an integer greater or equal to ``1``.

* ``spacing`` defines the spacing between two consecutive exercises. It defaults to ``''`` (i.e. nothing). Otherwise, you can set it at  ``newline``, ``newline_twice``, or a value that will be inserted in a LaTeX ``addvspace{}`` command, for instance ``spacing=40.0pt`` will result in a ``addvspace{40.0pt}`` inserted at the end of each exercise. ``spacing`` can be overriden in the ``layout`` key (in either or both ``wordings`` and ``answers`` keys) of the exercise, in order to set different spacings for the wordings and the answers.

* ``newpage`` can be turned to true in order to insert a jump to next page.

* ``q_spacing`` can be used to set a default value for the spacing between two consecutive questions.

* ``text_exc`` and ``text_ans`` allow to customize the wording of the exercise and of its answer. ``text_exc`` defaults to nothing (empty string). ``text_ans`` defaults to ``"Example of detailed solutions:"`` with ``default`` preset, but also to an empty string with ``mental_calculation`` preset.

* The ``question`` and ``mix`` keys allow to define the exercise's questions. As YAML does not allow to use the same key, if you want to define several ``question`` keys, nor several ``mix`` keys, you'll have to use the same trick for them as for the ``exercise`` key: ``question1``, ``question2`` etc. or ``mix1``, ``mix2``, etc. See below the paragraphs about ``question`` and ``mix``.

Exercise's layout
^^^^^^^^^^^^^^^^^

It works the same way as a Sheet's layout, with some differences:

* In ``rowxcol``, the first number can be replaced by a ``?``. In that case, the number of rows will be automatically calculated, depending on the number of questions and the number of columns.

Examples of exercise's layouts:
"""""""""""""""""""""""""""""""

.. code-block:: yaml

  layout:
    wordings: rowxcol=4×3
    answers: rowxcol=4×3

will basically distribute the questions in 4 rows of 3 columns. Same for wordings and for answers.

.. code-block:: yaml

  layout:
    wordings: rowxcol=?×3, colwidths=5 5 8, print=1 1 2

will distribute, only for wordings, the questions in 3 columns of widths 5 cm, 5 cm and 8 cm. There will be 1 question in the left cell of each row, 1 question in the middle cell of each row and 2 questions in the right cell of each row.

If you have 6 expressions, say A, B, C, D, E and F to distribute:

.. code-block:: yaml

  layout:
    wordings: rowxcol=?×2

will distribute the questions in 2 columns of 3 rows, 1 question per row, i.e.:

A = ....            B = ....

C = ....            D = ....

E = ....            F = ....

whereas:

.. code-block:: yaml

  layout:
    wordings: rowxcol=?×2,  print=3 / 3

will distribute the questions in 2 columns of 1 row, 3 questions per row, i.e.:

A = ....            D = ....

B = ....            E = ....

C = ....            F = ....

The ``question`` key
^^^^^^^^^^^^^^^^^^^^

Example of a simple question:

.. code-block:: yaml

    question: expand simple -> inttriplets_2to9 (5)

This question says: "I want 5 questions about expand a simple braces expression, the numbers being integers between 2 and 9".

It is actually divided in two parts, separated by this arrow ``->``. The first part concerns the kind of question and possibly its specific attributes, the second part concerns the numbers' source to be used to create the question.

The question's ``id`` and attributes
""""""""""""""""""""""""""""""""""""

The left part of the scalar (string) matching a ``question`` key **must start** with two parts (words or several_words) separated by a space. This is the ``id`` of the question. Possible extra attributes can follow it, separated by commas (actually a comma and a space). Each extra attribute will be written as a pair ``key=value``.

For instance:

.. code:: yaml

  question: calculation order_of_operations, subvariant=only_positive, spacing=15.0pt -> singleint_5to20;;intpairs_2to9, variant=5 (1)

In this example, a question of kind "calculation order_of_operations" will be created, with only positive numbers, spaced of 15.0pt.

The question's ``nb`` and its attributes
""""""""""""""""""""""""""""""""""""""""

The right part (after ``->``) starts with the name of the numbers' source (``intpairs_*to*``, ``singleint_*to*`` etc. see the already existing questions to know what to use, so far there's no doc about them. Some questions require multiple sources, like the one in the example above, they're written in row, joined by ``;;``). It may be followed by attributes, just like the left part, and **must end** with an integer between braces, what is the number of questions to create with this numbers' source.

The example above will create 1 question, variant number ``5``, and use the sources ``singleint_5to20`` and ``intpairs_2to9``.

Note that you can put several different numbers' sources inside one ``question``. For instance:

.. code:: yaml

  questions: calculation order_of_operations, subvariant=only_positive, spacing=15.0pt -> singleint_5to20;;intpairs_2to9, variant=5 (1)
                                                                                       -> singleint_5to20;;intpairs_2to9, variant=7 (1)

or:

.. code-block:: yaml

    questions: expand simple -> inttriplets_2to9 (3)
                             -> inttriplets_5to15 (3)

This means there will be six questions, all being of "expand simple" kind, but the three first ones will use integers between 2 and 9; and the three last ones will use integers between 5 and 15.

The ``mix`` key
^^^^^^^^^^^^^^^

"Mixes" are primarily meant to allow to distribute numbers' sources randomly on several questions types. This will only work if all numbers' sources match all the questions of the same ``mix``.

They can also be used to control the randomness of questions in an exercise. For instance, you want that the 3 first questions of an exercise are in random order, and then the 3 next ones too, but not all the 6 questions in random order. Then you can set two ``mix`` keys, say ``mix1`` and ``mix2`` and put 3 questions inside each mix.

The questions and numbers' sources inside ``mix`` are not displayed as in simple ``question``, but under different keys, the ones starting by ``question``, the others by ``nb``.

.. code-block:: yaml

  - mix0:
    - question: calculation order_of_operations, subvariant=only_positive, pick=4, nb_variant=decimal1, spacing=15.0pt
    - nb: singleint_5to20;;intpairs_2to9, variant=0, required=true (1)
          singleint_5to20;;intpairs_2to9, variant=1,3,5,7, required=true (1)
          singleint_5to20;;intpairs_2to9, variant=2,3,6,7, required=true (1)
          singleint_5to20;;intpairs_2to9, variant=0-7, required=true (1)
  - mix1:
    - question: calculation order_of_operations, subvariant=only_positive, pick=6, nb_variant=decimal1, spacing=15.0pt
    - nb: singleint_3to12;;intpairs_2to9, variant=8-23, required=true (2)
          singleint_3to12;;intpairs_2to9, variant=116-155, required=true (1)
          singleint_3to12;;intpairs_2to9, variant=156-187, required=true (1)
          singleint_3to12;;intpairs_2to9, variant=8-23,100-187 (2)

.. note::

    Inside a ``mix``, the ``<question>``'s ``pick`` attribute tells how many times to create such a question. If unspecified, default value is ``1``. This attribute has no effect outside ``mix`` keys.

The rules to follow in a ``mix`` list are:

* Any numbers' source must be assignable to any of the questions of the section.

* Put at least as many numbers' sources as there are questions.

If you put more number's sources as there are questions, the extraneous ones will be ignored. This is useful when there are a lot of possibilities to pick from and you want to define special features to each of them, if chosen (like different number sources depending on variant or subvariant).

If among the sources you want to ensure there will be at least one of a certain type, you can set the ``required`` attribute of ``nb`` to ``true``.

Also, note that the question's variant can be redefined as ``nb``'s attribute (it overrides the one defined in ``question``, if any).

Conclusion
^^^^^^^^^^

Now the question is: how to know about the questions kinds and subkinds, and the possible contexts, variants or whatever other attributes? Well it is planned to add an easy way to know that (like a special directive) but there's nothing yet. The better, so far, may be to look at the provided sheets in ``mathmaker/data/frameworks/`` and see what's in there.
