Detailed version
----------------

Dev environment
^^^^^^^^^^^^^^^

.. note::

  git and python>=3.6 are mandatory for mathmaker development

Install external dependencies
"""""""""""""""""""""""""""""
You'll need to install the same dependencies as users do (see :ref:`install`), plus ``gettext``.

Get mathmaker's source code from github repo
""""""""""""""""""""""""""""""""""""""""""""

In the folder of your choice:

::

    $ git clone https://github.com/nicolashainaux/mathmaker.git

Setup a python virtual environment
""""""""""""""""""""""""""""""""""

It is strongly advised to install mathmaker in develop mode inside of a python virtual environment. This allows to install the required libraries without conflicting with other projects or python software on the same computer. Just get to the directory of your choice, and to create a virtual environment named ``dev0``, you type:

::

    $ python3 -m venv dev0

From there, you can activate it:

on Linux::

    $ source dev0/bin/activate

on FreeBSD::

    $ source dev0/bin/activate.csh

Install mathmaker
"""""""""""""""""

Once your virtual environment is activated, go to mathmaker's root:

::

    (dev0) $ cd path/to/mathmaker/

You should see something like:
::

    (dev0) $ ls
    CHANGELOG.rst  docs  LICENSE  MANIFEST.in  mathmaker README.md  README.rst  requirements.txt  setup.py  tests  tools  tox.ini

There you can install mathmaker in developer mode:
::

    (dev0) $ python3 setup.py develop

It's possible to clean the project's main directory:
::

    (dev0) $ python3 setup.py clean


Run mathmaker and tools
"""""""""""""""""""""""

From now on, it is possible to run ``mathmaker`` from your virtual environment. As ``mathmaker`` is installed in developer mode, any change in the source files will be effective when running ``mathmaker``. Go to a directory where you can leave temporary files (each sheet requiring pictures will produce picture files, by default), and test it:
::

    (dev0) $ cd path/to/garbage/directory/
    (dev0) $ mathmaker 06_orange_exam > out.tex 2> stderr.log && lualatex out.tex

You can check ``out.pdf`` with the pdf viewer you like.

You can also run the tools from the toolbox. Somewhat below, more informations about the :ref:`auxiliary_tools`.

Once you're done working with mathmaker, you can deactivate the virtual environment:
::

    (dev0) $ deactivate
    $

Note that it is not recommanded but possible to run ``mathmaker`` outside the virtual environment this way (as of 2018, not sure this feature still works and anyway you shouldn't do that):
::

    $ cd path/to/mathmaker/
    $ python3 -m mathmaker.cli

But it requires to have installed the python dependencies yourself on the host system (e.g. the computer) and maybe also to have set ``$PYTHONPATH`` correctly (and exported it).

Other dependencies
""""""""""""""""""

Linters
#######

It is recommended to install linters for PEP 8 and PEP 257 (see :ref:`writing_rules`):

::

    (dev0) $ pip3 install flake8
    (dev0) $ pip3 install pydocstyle

.. note::

    PEP 257 is not yet really applied... but PEP 8 is!


Test dependencies
#################
In addition you should install at least ``pytest``, and maybe ``tox`` if you intend to include tox tests in mathmaker:

::

    (dev0) $ pip3 install pytest
    (dev0) $ pip3 install tox

Below is more information about `testing`_.

Documentation dependencies
##########################
You'll need to install these dependencies in the virtual environment:

::

    (dev0) $ pip3 install sphinx sphinx-rtd-theme

``sphinx-rtd-theme`` is the theme used for mathmaker's documentation. It's the `readthedocs <https://readthedocs.org/>`_ theme.

.. note::

    ``sphinx-autodoc-annotation`` makes writing docstrings lighter when using python3 annotations.

Below is more information about `documentation`_.

.. _dev_settings:

Dev settings
^^^^^^^^^^^^

You should make a copy of the default configuration files:
::

    (dev0) $ cd path/to/mathmaker/settings/
    (dev0) $ mkdir dev/
    (dev0) $ cp default/*.yaml dev/

Then you can edit the files in ``mathmaker/settings/dev/`` to your liking. Any value redefined there will override all other settings (except the options from the command line).

In ``logging.yaml`` the loggers part is interesting. I usually set the ``__main__`` logger to ``INFO`` (this way, informations about starting and stopping mathmaker are recorded to ``/var/log/mathmaker``, take care to define the log rotation if you do so) and the dbg logger to ``DEBUG``. This second setting is important because it will allow to enable debugging loggers in ``debug_conf.yaml``.

``debug_conf.yaml`` allows to trigger each debugging logger individually by setting it to ``DEBUG`` instead of ``INFO``.

And in ``user_config.yaml`` it is especially nice to define an output directory where all garbage files will be stored, but also to set the language, the font etc.

For instance, my ``settings/dev/user_config.yaml`` contains this:
::

    # SOFTWARE'S CONFIGURATION FILE

    PATHS:
        OUTPUT_DIR: /home/nico/dev/mathmaker/poubelle/

    LOCALES:
        LANGUAGE: fr_FR
        CURRENCY: euro

    LATEX:
        FONT: Ubuntu
        ROUND_LETTERS_IN_MATH_EXPR: True

    DOCUMENT:
        QUESTION_NUMBERING_TEMPLATE_SLIDESHOWS: "n°{n}"

See :ref:`settings` to learn more about the way settings are handled by ``mathmaker``.


Testing
^^^^^^^

Run the tests
"""""""""""""

The testing suite is run by `py.test <http://pytest.org/latest/contents.html>`_ this way:

::

    (dev0) $ pytest

or this way:

::

    (dev0) $ python3 setup.py test

Where do they live?
"""""""""""""""""""

Most of the tests belong to ``tests/``. Any function whose name starts with ``test_`` or ends with ``_test`` written in any python file whose name also starts with ``test_`` (and stored somewhere under ``tests/``) and will be automatically added to the tests run by ``pytest``.

Some more tests are written as `doctests <https://docs.python.org/3/library/doctest.html>`_ (see also `pytest documentation about doctests <http://pytest.org/latest/doctest.html>`_) in the docstrings of the functions. It's possible to add doctests, especially for simple functions (sometimes it is redundant with the tests from ``tests/``, but this is not a serious problem). The configuration for tests is so that any new doctest will be automatically added to the tests run by ``pytest``.

Tox
"""

Still needs to be setup for mathmaker. To test ``mathmaker`` against different versions of python, we should be able to run tox this way:
::

    (dev0) $ tox

or this way:

::

    (dev0) $ python3 setup.py tox

Be sure you have different versions of python installed correctly on your computer before starting this. The missing versions will be skipped anyway. Note that it is not a purpose of ``mathmaker`` to run under a lot of python versions (several python3 versions are OK, but no support for python2.7 is planned and that would be a waste of time since in 2020 python2.7 will not be developped anymore).

.. _logging_debugging:

Loggers: main, daemon, debugging, output watcher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`dev_settings` to know how to use the settings files and enable or disable logging and debugging.

Main logger
"""""""""""

``__main__`` is intended to be used for messages relating to ``mathmaker`` general working. In particular, it should be used to log any error that forces ``mathmaker`` to stop, before it stops.

In order to use this ``__main__`` logger, you can write this at the start of any function (assuming you have imported settings at the top of the file):

::

    log = settings.mainlogger


And then inside this function:

::

    log.error("message")

(or ``log.warning("message")`` or ``log.critical("message")`` depending on the severity level).

If an Exception led to stop ``mathmaker``, then the message should include its Traceback (if you notice this is not the case somewhere, you can modify this and make a pull request). For instance in ``cli.py``:

::

    try:
        shared.machine.write_out(str(sh))
    except Exception:
        log.error("An exception occured during the creation of the sheet.",
                  exc_info=True)
        shared.db.close()
        sys.exit(1)

Daemon logger
"""""""""""""

This logger is intended to be used by the daemon script. Works the same way as the main logger.

Debugging logger
""""""""""""""""

``dbg`` is the logger dedicated to debugging and ready to use. No need to write ``sys.stderr.write(msg)`` anywhere.

If there's no logger object in the function you want to print debugging messages, you can create one this way:

* Add the matching entry in ``debug_conf.yaml`` (both the ``settings/default/`` and ``settings/dev/`` versions, but set to ``INFO`` in the ``settings/default/`` version). For short modules, you can add only one level, and for modules containing lots of functions of classes, two levels should be added, like the example of the extract below: ::

    dbg:
        db: INFO
        wording:
            merge_nb_unit_pairs: INFO
            setup_wording_format_of: INFO
            insert_nonbreaking_spaces: INFO
        class_or_module_name:
            fct: DEBUG

* Import the settings at the top of the file, if it's not done yet: ::

    from mathmaker import settings


* Create the logger at the start of the function (i.e. locally): ::

    def fct():
        log = settings.dbg_logger.getChild('class_or_module_name.fct')

* Then where you need it, inside ``fct``, write messages this way: ::

    log.debug("the message you like")


Later when you need to disable this logger, you just set it to ``INFO`` instead of ``DEBUG`` in ``settings/dev/debug_conf.yaml``. See :ref:`dev_settings` for information on these files.

(Will be obsolete once the core is replaced by ``mathmakerlib``) A summary of the conventions used to represent the different core objects (i.e. what their ``__repr__()`` returns):

.. image:: pics/dbg_all.png

Output Watcher logger
"""""""""""""""""""""
This is another debugging logger. It can be used to check wether output is as expected, in order to detect bugs that do not crash mathmaker.
Works the same way as the main logger. The log messages are sent to another facility (local4), in order to be recorded independently.

System log configuration
^^^^^^^^^^^^^^^^^^^^^^^^

Systems using ``rsyslog``
"""""""""""""""""""""""""

The communication with ``rsyslog`` goes through a local Unix socket (no need to load ``rsyslog`` TCP or UDP modules).

.. note::

    The default socket is ``/dev/log`` for Linux systems, and ``/var/run/log`` for FreeBSD. These values are defined in the logging*.yaml settings files.

``rsyslog`` may be already enabled and running by default (Ubuntu) or you can install, enable and start it (in Manjaro, ``# systemctl enable rsyslog`` and ``# systemctl start rsyslog``).

Ensure ``/etc/rsyslog.conf`` contains these lines:
::

    $ModLoad imuxsock

    $IncludeConfig /etc/rsyslog.d/*.conf

Then create (if not created yet) a 'local' configuration file, like: ``/etc/rsyslog.d/40-local.conf`` and put (or add) in it:

.. code-block:: text

    #  Local user rules for rsyslog.
    #
    #
    local4.*                     /var/log/mathmaker_output.log
    local5.*                     /var/log/mathmaker.log
    local6.*                     /var/log/mathmakerd.log

Then save it and restart:

- in Ubuntu: ``# service rsyslog restart``
- in Manjaro: ``# systemctl restart rsyslog``

.. warning::
    Do not create ``/var/log/mathmaker.log`` yourself with the wrong rights, otherwise nothing will be logged.

To format the messages in a nicer way, it's possible to add this in /etc/rsyslog.conf:

.. code-block:: text

    $template MathmakerTpl,"%$now% %timegenerated:12:23:date-rfc3339% %syslogtag%%msg%\n"

and then, modify /etc/rsyslog.d/40-local.conf like:

.. code-block:: text

    local4.*                        /var/log/mathmaker_output.log;MathmakerTpl
    local5.*                        /var/log/mathmaker.log;MathmakerTpl
    local6.*                        /var/log/mathmakerd.log;MathmakerTpl

Tools to check everything's fine: after having restarted rsyslog, enable some more informations output:

.. code-block:: console

    # export RSYSLOG_DEBUGLOG="/var/log/myrsyslogd.log"
    # export RSYSLOG_DEBUG="Debug"

and running the configuration validation:

.. code-block:: console

    # rsyslogd -N2 | grep "mathmaker"

should show something like (errorless):

.. code-block:: console

    rsyslogd: version 7.4.4, config validation run (level 2), master config /etc/rsyslog.conf
    2564.153590773:7f559632b780:   ACTION 0x2123160 [builtin:omfile:/var/log/mathmaker.log;MathmakerTpl]
    2564.154126386:7f559632b780:   ACTION 0x2123990 [builtin:omfile:/var/log/mathmakerd.log;MathmakerTpl]
    2564.158461309:7f559632b780:   ACTION 0x2123160 [builtin:omfile:/var/log/mathmaker.log;MathmakerTpl]
    2564.158729012:7f559632b780:   ACTION 0x2123990 [builtin:omfile:/var/log/mathmakerd.log;MathmakerTpl]
    rsyslogd: End of config validation run. Bye.

Once you've checked this works as expected, do not forget to configure your log rotation.

.. note::

    mathmaker does not support systemd journalisation (the default one in Manjaro). You may have to setup systemd too (enable ``ForwardToSyslog`` in its conf file) in order to get ``rsyslog`` recording messages. Also you may need to add ``$ModLoad imjournal`` in ``/etc/rsyslog.conf`` and to create the file ``/var/spool/rsyslog``. For a better setup, see https://www.freedesktop.org/wiki/Software/systemd/syslog/. A workaround to prevent duplicate messages could be to discard the unwanted ones, like described here: http://www.rsyslog.com/discarding-unwanted-messages/.

Documentation
^^^^^^^^^^^^^

Current state
"""""""""""""

As stated in the :ref:`guided_tour.foreword`, the documentation is being turned from doxygen to Sphinx, so there are missing parts .

Any new function or module has to be documented as described in `PEP 257  <https://www.python.org/dev/peps/pep-0257/>`_.

The doxygen documentation for version 0.6 is `here <http://mathmaker.sourceforge.net/contribute/doc/annotated.html>`_. The core parts are still correct, so far.

Format
""""""

This documentation is written in `ReStructured Text <http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_ format.

There are no newlines inside paragraphs. Set your editor to wrap lines automatically to your liking.

Make html
"""""""""

To produce the html documentation:

::

    (dev0) mathmaker [dev] $ $ cd docs/
    (dev0) mathmaker/docs [dev] $ $ make html

If modules have changed (new ones, deleted ones), it is necessary to rebuild the autogenerated index:

::

    (dev0) mathmaker/docs [dev] $ sphinx-apidoc -f -o . ../mathmaker

.. _auxiliary_tools:

Auxiliary tools
^^^^^^^^^^^^^^^

Several standalone scripts live in the ``toolbox/`` directory under root. They can be useful for several tasks that automate the handling of data.

* ``build_db.py`` rebuilds the database from scratch, updating its data from several sources (some \*.yaml files, \*.po files etc.). This tool greatly needs to be rewritten! And once the database is smaller, it should be included in the main code and used to generate the database that will be shipped).

* ``build_index.py`` must be run when a new sheet is to be "registered" (or removed)

* ``update_pot_files``, a shell script making use of ``xgettext`` and of the scripts ``merge_py_updates_to_main_pot_file``, ``merge_yaml_updates_to_pot_file`` and ``merge_xml_updates_to_pot_file`` (this last one will be removed in 0.7.2). Run ``update_pot_files`` to update ``locale/mathmaker.pot`` when new strings to translate have been added to python code (i.e. inside a call to ``_()``) or new entries have been added to any yaml or xml (xml files will be turned to yaml files in 0.7.2) file from ``mathmaker/data`` (only entries matching a number of identifiers are taken into account, see DEFAULT_KEYWORDS in the source code to know which ones exactly).

``import_msgstr`` and ``retrieve_po_entries`` are useful on some rare occasions. See their docstrings for more explanations. They both have a ``--help`` option.

``pythagorean_triples_generator`` shouldn't be of any use any more (later on maybe a part of its code will be incorporated to ``build_db.py``, that's why it's still around here)

.. _writing_rules:

Writing rules
^^^^^^^^^^^^^

It is necessary to write the cleanest code possible. It has not been the case in the past, but the old code is updated chunk by chunk and **any new code portion must follow python's best practices**, to avoid adding to the mess, and so, must:

* Use idioms (to learn some, it is recommended to read Jeff Knupp's `Writing Idiomatic Python <https://jeffknupp.com/writing-idiomatic-python-ebook/>`_)

* Conform to the `PEP 8 -- Style Guide for Python <https://www.python.org/dev/peps/pep-0008/>`_

* Conform to the `PEP 257 -- Docstring Conventions <https://www.python.org/dev/peps/pep-0257/>`_

And of course, all the code is written in english.

As to PEP 8, mathmaker 's code being free from errors, the best is to use a linter, like ``flake8``. They also exist as plugins to various text editors or IDE (see :ref:`atom_packages` for instance). Three `error codes <http://pep8.readthedocs.io/en/latest/intro.html#error-codes>`_ are ignored (see ``.flake8``):

* E129 because it is triggered anytime a comment is used to separate a multiline conditional of an ``if`` statement from its nested suite. A choice has been made to wrap multiline conditions in ``()`` and realize the separation with next indented block using a ``# __`` comment (or any other comment if it's necessary) and this complies with PEP 8 (second option here):

    Acceptable options in this situation include, but are not limited to:

    ::

        # No extra indentation.
        if (this_is_one_thing and
            that_is_another_thing):
            do_something()

        # Add a comment, which will provide some distinction in editors
        # supporting syntax highlighting.
        if (this_is_one_thing and
            that_is_another_thing):
            # Since both conditions are true, we can frobnicate.
            do_something()

* W503 because PEP 8 does not compel to break before binary operators (the choice of breaking *after* binary operators has been done).

* E704 because on some occasions it is OK to put several *short* statements on one line in the case of ``def``. It is the case in several test files using lines like ``def v0(): return Value(4)``

Other choices are:

* A maximum line length of 79
* Declare ``_`` as builtin, otherwise all calls to ``_()`` (i.e. the translation function installed by gettext) would trigger flake8's error F821 (undefined name).
* No complexity check. This might change in the future, but the algorithms in the core are complex. It's not easy to make them more simple (if anyone wants to try, (s)he's welcome).
* Name modules, functions, instances, and other variables in lower case, whenever possible using a single ``word`` but if necessary, using ``several_words_separated_with_underscores``.
* Name classes in CapitalizedWords, like: ``SuchAWonderfullClass`` (don't use mixedCase, like ``wrongCapitalizedClass``).
* All ``import`` statements must be at the top of any module. It must be avoided to add ``from ... import ...`` at the top of some functions, but sometimes it's necessary. A solution to avoid this is always preferred.
* All text files (including program code) are encoded in UTF-8.

As to PEP 257, this is also a good idea to use a linter, but lots of documentation being written as doxygen comments, the linter will detect a lot of missing docstrings. Just be sure the part you intend to push does not introduce new PEP 257 errors (their number must decrease with time, never increase).

The text of any docstring is marked up with reStructuredText.

The module `mathmaker.lib.tools.wording` can be considered as a reference on how to write correct docstrings. As an example, the code of two functions is reproduced here.

.. note::

    The use of python3's annotations and ``sphinx-autodoc-annotation`` would automatically add the types (including return type) to the generated documentation. If ``sphinx-autodoc-annotation``'s bug is corrected, the ``:type ...: ...`` and ``:rtype: ...`` lines will be removed.

.. code-block:: python

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


    def merge_nb_unit_pairs(arg: object):
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

.. _atom_packages:

Atom packages
^^^^^^^^^^^^^

This paragraph lists useful packages for atom users (visit the links to have full install and setup informations):

* ``flake8`` linter provider: `linter-flake8 <https://atom.io/packages/linter-flake8>`_ (Note: you should let the settings as is, except for the "Project config file" entry where you can write ".flake8" to use ``mathmaker`` project's settings.)

* ``pydocstyle`` linter provider: `linter-pydocstyle <https://atom.io/packages/linter-pydocstyle>`_

* python3's highlighter:  `MagicPython <https://atom.io/packages/MagicPython>`_ (MagicPython is able to highlight correctly python3's annotations. You'll have to disable the language-python core package.)

* To edit rst documentation: `language-restructuredtext <https://atom.io/packages/language-restructuredtext>`_ and `rst-preview-pandoc <https://atom.io/packages/rst-preview-pandoc>`_
