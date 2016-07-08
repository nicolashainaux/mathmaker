A deeper look in the source code
================================

.. _settings:

Settings
--------

Everything happens in ``mathmaker/settings/__init__.py`` (it would be better to have everything happening rather in something like ``mathmaker/settings/settings.py``, so this will most certainly change).

This module is imported by the main script at start, that run its ``init()`` function. After that, any subsequent ``from mathmaker import settings`` statement will make ``settings.*`` available.

The values shared as ``settings.*`` are: the paths to different subdirectories of the project, the loggers and the values read from `configuration`_ files. (Plus at the moment, two default values that should move to some other place).

None of these values is meant to be changed after it has been set by the main script, what calls ``settings.init()`` and then corrects some of them depending on the command-line options. Once this is done, these values can be considered actually as constants (they are not really constants as they are setup and corrected, so no UPPERCASE naming).

``tests/conftest.py `` uses the ``settings`` module the same way ``mathmaker/cli.py`` does.

Configuration
-------------
This is handled by ``mathmaker/lib/tools/config.py``. It works the same way for any of the ``*.yaml`` files. It first loads the default values from ``mathmaker/settings/default/filename.yaml``. Then it updates any value found redefined in any of these files: ``/etc/mathmaker/filename.yaml``, ``~/.config/mathmaker/filename.yaml`` and ``mathmaker/settings/dev/filename.yaml``. Any missing file is skipped (except the first one: the default settings are part of the code, are shipped with it and must be present).

An extended dict class is used to deal easier with dicts created from yaml files. See ``mathmaker/lib/tools/ext_dict.py``.

The daemon
----------

It's a daemonized web server that allows to communicate with mathmaker through http requests. See :ref:`http_server`.

Shared
------

Three resources are shared: `the database`_, the LaTeX machine and the sources.

``mathmaker/lib/shared.py`` works a similar way as the ``settings`` module. It is initialized once in the main script and then its resources are used.


The database
------------

The aim of the database is to avoid having to create a lot of randomly values and store them in lists or dicts everytime we need something.

It is considered as a source among others.

The sources
-----------

They concern as well numbers as words or letters or anything one can think of. So far, they are used only for mental calculation, but they should be used for any kind of question.

When random numbers are required, most of the time, we don't need complete random. For instance if we want a pair of integers for the multiplication tables between 2 and 9, we don't want to ask the same question twice in a row.

The sources manage this randomness. Anytime we need to use a source, we can use its ``next()`` method to get the next random data, without worrying in the same time whether it's the same as the previous one or not.

So we have sources for names, for words having a limited number of letters, for different kinds of numbers but also for mini-problems wordings.

So far, there are two kinds of sources: the ones that are provided by the database, and the ones that are provided by the python function ``generate_values()`` from ``mathmaker/lib/sources.py``.

All sources are initialized in ``mathmaker/lib/shared.py``. There you can see which one has its values provided by the database, which are the other ones.

The database provides an easy way to ensure the next value will be different from the last one: we simply "stamp" each drawn value and the next time we draw a value among the yet unstamped ones. When they're all stamped, we reset all stamps and redraw. There's a tiny possibility to draw two times in a row the same value, so far, but it's so tiny we can safely ignore it. (This could be improved later). The values drawn from ``generate_values()`` are so different the ones from the others that it's very unlikely to draw the same ones two times in a row.

.. _translation_files:

The real and the fake translation files
---------------------------------------

``mathmaker/locale/mathmaker.pot`` is a real translation file.

The other ``mathmaker/locale/*.pot`` files are "fake" ones. They are used to get random words in a specific language, but the words do not need to be the exact translation from a source language.

For instance, ``w4l.pot`` contains words of four different letters. It wouldn't make sense to translate the english word "BEAN" into a word of the same meaning AND having exactly four different letters, in another language. This wouldn't work for french, for instance. In general this would only work for rare exceptions (like "HALF" can be translated to "DEMI" in french).

The same applies to ``feminine_names.pot`` and ``masculine_names.pot``. These files are used to get random names, but we don't need to *translate* them.

So, the entries in these "fake" translation files are only labeled entries, with nothing to translate.

A translator only needs to provide a number of entries (at least 10) in each of these files. No matter how many, no matter which ``msgid`` do they match. So: in ``masculine_names.po`` are several masculine names required, in ``feminine_names.po`` are several feminine names required and in ``w4l.po`` are several words of four unique letters required. Each time, at least 10, and then, the more the better.


The sheets, exercises and questions
-----------------------------------
I won't describe thoroughly all objects under ``lib/sheet``, ``lib/sheet/exercise`` and ``lib/sheet/exercise/question`` because most of them are the old-style way of implementing this all.

Now the sheets should be frameworks stored as xml files (under ``data/frameworks/``). Under ``lib/sheet``, The classes ``S_Structure`` and ``S_Generic`` will be kept. ``S_Structure`` handles the layout of the sheet depending on the ``SHEET_LAYOUT`` dict you can find at the top of any sheet module, and that is built by ``S_Generic`` from the ``<layout>`` section of any xml framework.

There are no ``X_Generic`` nor ``Q_Generic`` classes yet, but there will be. They will replace the old-style ``X_*`` and ``Q_*`` classes. The way ``X_MentalCalculation`` and ``Q_MentalCalculation`` classes are written is a prefiguration of the future ``X_Generic`` and ``Q_Generic`` classes.

The ``Q_MentalCalculation`` class actually leaves the work to a ``sub_object`` that is written in one of the mental calculation modules (under ``mc_modules/``). This allow a great variety of questions distributed in many files instead of one long file for all questions. These ``sub_object``s also have a mother class (defined in ``mc_modules/mc_module.py``) and can be organized in subclasses (like vocabulary questions what all inherit from ``vocabulary_questions.structure``).

.. _the_core:

The core
--------

Diagram
^^^^^^^

You can check the 0.6 version (i.e. from doxygen) of the `top of the core diagram <http://mathmaker.sourceforge.net/contribute/doc/classcore_1_1base_1_1Clonable.html>`_, though it will be somewhat changed later, it still can be used as reference for some time.

Unfinished draft of future plans:

.. image:: pics/new_inheritance_2015.png

Core objects' summary
^^^^^^^^^^^^^^^^^^^^^
Objects at left; associated ``__repr()`` at right:

.. image:: pics/all_pics.png

Core objects' details
^^^^^^^^^^^^^^^^^^^^^
The "old" doc for 0.6 version is available `here <https://sourceforge.net/p/mathmaker/doc4dev/Core%20Objects/>`_ and mainly still correct for 0.7 version. When things will have settled down to something more stable, an updated documentation will be published chunk by chunk.


