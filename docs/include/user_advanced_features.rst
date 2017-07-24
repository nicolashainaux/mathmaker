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
        OUTPUT_DIR: ./

    LOCALES:
        # Available values can be checked in the locale directory.
        LANGUAGE: en_US
        ENCODING: UTF-8
        # Values can be 'euro', 'sterling', 'dollar'
        CURRENCY: dollar

    LATEX:
        FONT:
        ROUND_LETTERS_IN_MATH_EXPR: False

Some explanations:

* The ``PATHS:`` section is here to provide a mean to change the paths to ``euktoeps``, ``lualatex`` and ``xmllint`` mainly. In case one of them is not reachable the way it is set in this section, you can change that easily.

* The ``PATHS:`` section contains also an ``OUTPUT_DIR:`` entry. This is the directory where ``mathmaker`` will store the possible picture files (.euk and .eps). Default value is "current directory". You can set another value, at your liking.

* The entries under ``LOCALES:`` allow to change the language, encoding, and default currency used.

* The ``LATEX:`` section contains an entry to set the font to use (be sure it is available on your system). The ``ROUND_LETTERS_IN_MATH_EXPR:`` entry is disabled by default (set to False). If you set it to True, a special font will be used in math expressions, that will turn all letters (especially the 'x') into a rounded version. This is actually the ``lxfonts`` LaTeX package. It doesn't fit well with any font. Using "Ubuntu" as font and setting ``ROUND_LETTERS_IN_MATH_EXPR:`` to True gives a nice result though.

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


xml sheets
----------
As a directive to mathmaker it is possible to give a path to an xml file.

Creating a new xml file that can be used as a model by ``mathmaker`` is more for advanced users, though it's not that difficult.

Example
^^^^^^^

Let's have a look at ``mathmaker/data/frameworks/mental_calculation/lev11_1/divisions.xml``:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>

    <sheet header="" title="Mental calculation" subtitle="Divisions" text="" answers_title="Answers">

    	<layout type="mental" font_size_offset="-1" />

    	<!-- Default value: id='generic'
    		 No default for kind and subkind, they must be given -->
    	<!-- Available kinds for mental calculation: tabular, slideshow -->
    	<exercise id="mental_calculation" kind="tabular" shuffle="true">

    		<!-- Default value (planned): context="none"
    			 No default for kind and subkind, they must be given -->
    		<question kind="divi" subkind="direct">
    			<nb source="intpairs_2to9">20</nb>
    		</question>

    	</exercise>

    </sheet>

The ``<sheet>`` tags
^^^^^^^^^^^^^^^^^^^^

They have attributes that let you easily change the title of the sheet, a subtitle etc.

The ``<layout>`` tags
^^^^^^^^^^^^^^^^^^^^^

They may show up as first child of a ``<sheet>`` or ``<exercise>``. They work about the same way in both cases but both have their own special features too.

.. image:: pics/layouts.png

If a ``<sheet>`` or ``<exercise>`` contains no ``<layout>``, it is assumed that the default layout will be used, i.e. no layout at all: all exercises and all questions will simply be printed one after the other. It would be equivalent to:

.. code-block:: xml

		<layout />

what would be the same as:

.. code-block:: xml

		<layout>
			<wordings />
			<answers />
		</layout>

and also the same as:

.. code-block:: xml

		<layout>
			<wordings rowxcol="none" />
			<answers rowxcol="none" />
		</layout>

The ``<wordings>`` and ``<answers>`` tags contain the layout for wordings and for answers, respectively.

Attributes of ``<wordings />`` and ``<answers />``
""""""""""""""""""""""""""""""""""""""""""""""""""

* ``rowxcol`` can contain ``"none"`` (default: no layout) or the number of rows and columns as a multiplication of two integers: ``"r×c"``, for instance: ``"2×3"``. This would mean to use 2 rows and 3 columns, what would define 6 "cells". As a convenience, you can use a x instead of a ×, like this: ``"2x3"``. The first number can be replaced by a ``?`` (exercises layouts only), in that case, the number of rows will be automatically calculated, depending on the number of questions and the number of columns.

* ``colwidths`` is ignored if ``rowxcol`` contains ``"none"``. If ``rowxcol`` contains a ``"r×c"`` definition, then ``colwidths`` defaults to ``"auto"``: the width of all columns will be calculated automatically (all equal). Otherwise, you can set the values you like, separated by spaces, like: ``"4.5 4.5 9"`` what would make the two first columns 4.5 units wide and the last, 9 units wide. The length unit can be set in the ``<sheet>``'s ``<layout>``'s attribute ``unit``. It defaults to cm. There must be as many values as the number of columns defined in the ``"r×c"`` definition.

* ``distribution`` is the distribution of the questions (or exercises) per cell. It is also ignored if ``rowxcol`` contains ``"none"``. If ``rowxcol`` contains a ``"r×c"`` definition, then ``distribution`` defaults to ``"auto"``: each "cell" will contain one question. Otherwise, you can tell how many questions you want in each cell, row after row, as integers separated by spaces, like: ``"2 1 1 3 1 1"`` what would put (with ``rowxcol="2×3"``) 2 questions (or exercises) in the first cell, then 1 question in each other cell of the first row, then 3 questions in the first cell of the second row, and 1 question in each cell left. There must be as many numbers as cells. As a convenience, you can add a ``;`` or ``,`` to separate the rows, like: ``"2 1 1, 3 1 1"`` (These two punctuation signs will simply be ignored). Each row must contain as many numbers as defined in the ``"r×c"`` definition. If the number of rows is left undefined (``?``) then only the first row has to be defined (extra rows will be ignored) as a pattern for all rows (the default still being ``"auto"``, i.e. 1 question per cell).

Examples:

.. code-block:: xml

		<layout>
			<wordings rowxcol="4×3" />
			<answers rowxcol="4×3" />
		</layout>

will basically distribute the questions in 4 rows of 3 columns. Same for wordings and for answers.

.. code-block:: xml

		<layout>
			<wordings rowxcol="?×3" colwidths="5 5 8" distribution="1 1 2" />
		</layout>

will distribute, only for wordings, the questions in 3 columns of widths 5 cm, 5 cm and 8 cm. There will be 1 question in the left cell of each row, 1 question in the middle cell of each row and 2 questions in the right cell of each row.

If you have 6 expressions, say A, B, C, D, E and F to distribute:

.. code-block:: xml

    <layout>
      <wordings  rowxcol="?×2" />
    </layout>

will distribute the questions in 2 columns of 3 rows, 1 question per row, i.e.:

A = ....            B = ....

C = ....            D = ....

E = ....            F = ....

whereas:

.. code-block:: xml

    <layout>
      <wordings  rowxcol="?×2"  distribution="3, 3" />
    </layout>

will distribute the questions in 2 columns of 1 row, 3 questions per row, i.e.:

A = ....            D = ....

B = ....            E = ....

C = ....            F = ....


Special attributes of ``<sheet>``'s ``<layout>``
""""""""""""""""""""""""""""""""""""""""""""""""

* ``type`` allows to use several different special preformatted layouts. Default value is ``"default"``. Other possible values are ``"short_test"``, ``"mini_test"``, ``"equations"`` and ``"mental"``.

* ``unit`` defaults to cm (SI). It is used for lengths like in ``colwidths``.

* The ``font_size_offset`` attribute is especially practical to resize the whole sheet at once (set it at ``+1`` or ``+2`` to enlarge all fonts, or ``-1`` or ``-2`` to reduce all fonts' size).

The ``<exercise>`` tags
^^^^^^^^^^^^^^^^^^^^^^^

The ``<exercise>`` part is the one you can change alot. Keep the ``id="mental_calculation"`` and ``kind="tabular"`` attributes though (they can't be changed yet) but you can put the questions you like inside.

For exercises, ``spacing`` defaults to ``""``, it is the spacing to be introduced at the end of the exercise. You can set it at ``"`` (no spacing), ``"newline"``, ``"newline_twice"`` or a value that will be inserted in a LaTeX ``addvspace{}`` command, for instance ``spacing="40.0pt"`` will result in a ``addvspace{40.0pt}`` inserted at the end of the exercise.

The questions will show up in the order you write them, unless you set the ``shuffle`` attribute of ``<exercise>`` to ``"true"``.

The ``<question>`` tags
^^^^^^^^^^^^^^^^^^^^^^^

Each question is defined this way:

.. code-block:: xml

    <question kind="divi" subkind="direct">
        <nb source="intpairs_2to9">20</nb>
    </question>

You must set at least a ``kind`` and a ``subkind`` attributes. Then inside the question, you set at least one numbers' source. This question says: "I want 20 questions about direct division (i.e. each one will be of the form a ÷ b = ?) the numbers being integers between 2 and 9". (For divisions the pair of integers will be b and the solution; mathmaker will compute a automatically).

Another example, taken from ``mathmaker/data/frameworks/mental_calculation/lev11_1/mini_problems.xml``:

.. code-block:: xml

    <question kind="addi" subkind="direct" context="mini_problem">
        <nb source="intpairs_5to20">5</nb>
    </question>

You see you can set the lower and upper values as you like. Just respect the syntax (if you write ``intpairs_5_to_20`` this won't work). And this time a context is added to the question. So it means "I want 5 simple additive problems, the numbers being integers between 5 and 20".

Note that you can put several different numbers' sources inside one ``<question>``. For instance:

.. code-block:: xml

    <question kind="multi" subkind="direct">
        <nb source="intpairs_2to9">1</nb>
        <nb source="table_11">1</nb>
        <nb source="decimal_and_one_digit">1</nb>
    </question>

This means there will be three questions, all being direct multiplications, but one pair of numbers will be integers between 2 and 9; one pair will be from the table of 11 (like 34 × 11), and one will be a decimal number and a one digit number (like 150.3 × 0.01).

The ``<mix>`` tags
^^^^^^^^^^^^^^^^^^

In some sheets you'll find ``<mix>`` tags, like this one, taken from ``mathmaker/data/frameworks/mental_calculation/lev11_2/test_11_2.xml``:

.. code-block:: xml

      <mix>
        <question kind="area" subkind="rectangle" picture="true"></question>
        <question kind="multi" subkind="direct" pick="2"></question>
        <question kind="vocabulary" subkind="multi"></question>
        <nb source="table_15">1</nb>
        <nb source="table_11">1</nb>
        <nb source="intpairs_2to9" nb_variant="decimal1">1</nb>
        <nb source="intpairs_2to9" nb_variant="decimal2">1</nb>
      </mix>

It means the numbers' sources will be randomly attributed to the questions. Each time a new sheet is generated from this framework, the numbers from table of 15 will be attributed randomly to one of the four questions of the sections, and the same will happen to the other numbers' sources.

.. note::

    The ``<question>``'s ``pick`` attribute tells how many times to create such a question. If unspecified, default value is ``1``. This attribute has no effect outside ``<mix>`` tags.

The rules to follow in a ``<mix>`` section are:

* Any numbers' source must be assignable to any of the questions of the section.

* Put at least as many numbers' sources as there are questions. For instance in the example above we could have written this too:

.. code-block:: xml

    <mix>
        <question kind="area" subkind="rectangle" picture="true"></question>
        <question kind="multi" subkind="direct" pick="2"></question>
        <question kind="vocabulary" subkind="multi"></question>
        <nb source="table_15">3</nb>
        <nb source="intpairs_2to9" nb_variant="decimal1">1</nb>
    </mix>

If you put more number's sources as there are questions, the extraneous ones will be ignored. This is useful when there are a lot of possibilities to pick from and you want to define special features to each of them, if chosen (like different number sources depending on variant or subvariant).

If among the sources you want to have at least one of a certain type, you can set the ``required`` attribute of ``<nb>`` to ``"true"``. In the example below, 8 questions will be created. Among them, there will be at least 2 of variants 8 to 23, one of variant 116 to 155 and one of variant between 156 and 187. The 4 other ones will each match a variant between 8 and 23 or 100 and 187.

.. code-block:: xml

    <mix>
		  <question kind="calculation" subkind="order_of_operations" subvariant="only_positive" pick="8"></question>
		  <nb source="singleint_3to12;;intpairs_2to9" variant="8-23" required="true">2</nb>
		  <nb source="singleint_3to12;;intpairs_2to9" variant="116-155" required="true">1</nb>
		  <nb source="singleint_3to12;;intpairs_2to9" variant="156-187" required="true">1</nb>
		  <nb source="singleint_3to12;;intpairs_2to9" variant="8-23,100-187">10</nb>
		</mix>

Also, note that the question's variant can be redefined as ``<nb>``'s attribute (it overrides the one defined in ``<question>``, if any).

Conclusion
^^^^^^^^^^

Now the question is: how to know about the questions kinds and subkinds, and the possible contexts, variants or whatever other attributes? Well it is planned to add an easy way to know that (like a special directive) but there's nothing yet. The better, so far, may be to look at the provided sheets in ``mathmaker/data/frameworks/`` and see what's in there.
