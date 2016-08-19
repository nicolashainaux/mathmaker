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

At the moment (version 0.7), it's only possible to create mental calculation sheets this way. So there's not much to change from a raw model.

Let's have a look at ``mathmaker/data/frameworks/mental_calculation/lev11_1/divisions.xml``:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>

    <sheet header="" title="Mental calculation" subtitle="Divisions" text="" answers_title="Answers">

    	<!-- Default values: type="std" unit="cm" font_size_offset="0" -->
    	<!-- Available layout types: std|short_test|mini_test|equations|mental -->
    	<layout type="mental" font_size_offset="-1">
    		<exc>
    			<line nb="None">
    				<exercises>all</exercises>
    			</line>
    		</exc>
    		<ans>
    			<line nb="None">
    				<exercises>all</exercises>
    			</line>
    		</ans>
    	</layout>

    	<!-- Default value: id='generic'
    		 No default for kind and subkind, they must be given -->
    	<!-- Available kinds for mental calculation: tabular, slideshow -->
    	<exercise id="mental_calculation" kind="tabular">

    		<!--No default for kind and subkind, they must be given -->
    		<question kind="divi" subkind="direct">
    			<nb source="intpairs_2to9">20</nb>
    		</question>

    	</exercise>

    </sheet>

The ``<sheet>`` tag has attributes that let you easily change the title of the sheet, a subtitle etc.

The ``<layout>`` part can't be changed (yet) except the ``unit`` and ``font_size_offset`` attributes. The later one is especially practical to resize the whole sheet at once.

The ``<exercise>`` part is the one you can change alot. Keep the ``id="mental_calculation"`` and ``kind="tabular"`` attributes though (they can't be changed yet) but you can put the questions you like inside.

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

This means there will be three questions, all being direct multiplications, but one pair of numbers will be integers between 2 and 9; one pair will be from the table of 11 (like 34 × 11), and one will be a decimal number and a one digit number (like 150,3 × 0.01).

Last explained feature: in some sheets you'll find ``<mix>`` sections, like this one, taken from ``mathmaker/data/frameworks/mental_calculation/lev11_2/test_11_2.xml``:

.. code-block:: xml

    <mix>
        <question kind="area" subkind="rectangle" picture="true"></question>
        <question kind="multi" subkind="direct"></question>
        <question kind="multi" subkind="direct"></question>
        <question kind="vocabulary" subkind="multi"></question>
        <nb source="table_15">1</nb>
        <nb source="table_11">1</nb>
        <nb source="intpairs_2to9" variant="decimal1">1</nb>
        <nb source="intpairs_2to9" variant="decimal2">1</nb>
    </mix>

It means the numbers' sources will be randomly attributed to the questions. Each time a new sheet is generated from this framework, the numbers from table of 15 will be attributed . The rules to follow for a ``<mix>`` section are:

* Put as many numbers' sources as there are questions. For instance in the example above we could have written this too:

.. code-block:: xml

    <mix>
        <question kind="area" subkind="rectangle" picture="true"></question>
        <question kind="multi" subkind="direct"></question>
        <question kind="multi" subkind="direct"></question>
        <question kind="vocabulary" subkind="multi"></question>
        <nb source="table_15">3</nb>
        <nb source="intpairs_2to9" variant="decimal1">1</nb>
    </mix>

* Any numbers' source must be assignable to any of the questions.

Now the question is: how to know about the questions kinds and subkinds, and the possible contexts, variants or whatever other attributes? Well it is planned to add an easy way to know that (like a special directive) but there's nothing yet. The better, so far, may be to look at the provided sheets in ``mathmaker/data/framworks/mental_calculation/`` and see what's in there.