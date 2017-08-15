Guided tour
===========

.. _guided_tour.foreword:

Foreword
--------

This code has been developed chunk by chunk over more than 10 years now, starting with python2.3 or 4. Now it is a python3.4 software and my python skills have fortunately improved over the years. Problem is that several old parts, even after big efforts to correct the worst pieces, are not very idiomatic, especially the core.

Luckily there are unit tests, and whatever one might think about them, it's not difficult to admit that they're extremely useful to check nothing got broken when the core parts are written anew or debugged.

The documentation has been originately written using `doxygen <http://www.stack.nl/~dimitri/doxygen/>`_. Despite the fact it is an excellent documentation software, I have decided to move to `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ because it corresponds closer to python best practices. So, all doxygen-style comments will be turned into docstrings so mathmaker can use Sphinx to build the documentation. At the moment this work is just started, so the auto-generated Sphinx documentation is quite uncomplete now.

So, a part of the work to do is surely to bring new features, but another part, more annoying, is to turn ugly old parts into the right pythonic idioms. That's why at places you'll see that this or this module is deprecated and should be "reduced", or rewritten. A list of such things to do is available on `sourceforge <https://sourceforge.net/p/mathmaker/tickets/>`_. The 1.0 milestone inventories many things.

The issue
---------

It is utmost important to understand that mathmaker is not a software intended to compute mathematical stuff, but to display it. For instance, resolving a first-degree equation is not in itself a goal of mathmaker, because other softwares do that already (and we don't even need any software to do it). Instead, mathmaker will determine and display the steps of this resolution. Sometimes, mathmaker solutions will even try to mimic the pupils' way of doing things.

For instance, it won't automatically simplify a fraction to make it irreducible in one step, but will try to reproduce the steps that pupils usually need to simplify the fraction. So the GCD is only used to check when the fraction is irreducible and for the cases where there's no other choice, but not as the mean to simplify a fraction directly (not before pupils learn how to use it, at least).

Another example is the need of mathmaker to control the displaying of decimal and integer numbers perfectly. Of course, most of the time, it doesn't matter if a computer tells that 5.2×5.2 = 27.040000000000003 or 3.9×3.9 = 15.209999999999999 because everyone knows that the correct results are 27.04 and 15.21 and because the difference is not so important, so in many situations, this precision will be sufficient. But, can mathmaker display to pupils that the result of 5.2×5.2 is 27.040000000000003 ?

Also, the human rules we use to write maths are full of exceptions and odd details we don't notice usually because we're familiar to them. We would never write

   +2x² + 1x - 1(+5 - 1x)

but instead

   2x² + x - (5 - x)

There are many conventions in the human way to write maths and many exceptions.

These are the reasons why the core is quite complex: re-create these writing rules and habits on a computer and let the result be readable by pupils is not an easy thing.


Workflow
--------

Mathmaker creates Sheets of maths Exercises.

Each Exercise contains Questions.

Each Question uses objects from the core, that embbed enough information to compute and write the text of the Question and also the answer.

The main executable (``entry_point()`` in ``mathmaker/cli.py``) performs following steps:

* Load the default settings from configuration files.

* Setup the main logger.

* Check that the correct dependencies are installed.

* Parse the command-line arguments, updates the settings accordingly.

* Install the language and setup shared objects, like the database connection.

* If the main directive is ``list``, it just write the directives list to stdout

* Otherwise, it checks that the directive matches a known sheet (either a xml file or a sheet's name that mathmaker provides) and writes the result to the output (``stdout`` or a file)

The directories
---------------

Directories that are relevant to git, at the root:

.. code::

  .
  ├── docs
  ├── mathmaker
  ├── outfiles
  ├── tests
  └── toolbox

* The usual ``docs/`` and ``tests/`` directories
* ``mathmaker/`` contains the actual python source code
* ``toolbox/`` contains several standalone scripts that are useful for developers only (not users)
* Several usual files (``.flake8`` etc.)
* ``outfiles/`` (not listed here, because it is not relevant to git) is where the garbage is put (figures created when testing, etc.). Sometimes it is useful to remove all garbage files it contains.

``mathmaker/``'s content:

.. code::

  $ tree -d -L 1 mathmaker -I __pycache__
  mathmaker
  ├── data
  ├── lib
  ├── locale
  └── settings

* ``data/`` is where the database is stored, but also yaml files containing additional wordings, translations etc.
* ``lib/`` contains all useful classes and submodules (see below).
* ``locale/`` contains all translation files.
* ``settings/`` contains the functions dedicated to setup the settings and also the default settings files themselves.

``lib/``'s content:

.. code::

  $ tree -d -L 3 mathmaker/lib -I __pycache__
  mathmaker/lib
  ├── constants
  ├── core
  ├── document
  │   ├── content
  │   │   ├── algebra
  │   │   ├── calculation
  │   │   ├── geometry
  │   │   └── ... (maybe some others in the future)
  │   └── frames
  ├── machine
  ├── old_style_sheet
  │   └── exercise
  │       └── question
  └── tools

* ``constants/`` contains several constants (but ``pythagorean.py`` must be replaced by requests to the database)
* ``core/`` contains all mathematical objects, numeric or geometric
* ``document/`` contains the frames for sheets, exercises in questions, under ``document/frames/``, and the questions' content, under ``document/content/``.
* ``machine/`` contains the "typewriter"
* ``old_style_sheet/`` contains all old style sheets, exercices and questions. All of this is obsolete (will be replaced by generic objects that take their data from yaml files and created by the objects defined in ``document/frames/``)
* ``tools/`` contains collections of useful functions

  - ``__init__.py`` contains various functions

  - ``database.py`` contains all functions required to interact with mathmaker's database

  - ``frameworks.py`` contains a collection of useful functions to handle the collection of yaml sheet files

  - ``ignition.py`` contains several functions called at startup

  - ``maths.py`` contains some extra mathematical functions

  - ``wording.py`` contains a collection of useful functions to handle wordings

  - ``xml.py`` contains a collection of useful functions to handle the xml files (obsolete, will disappear)

* ``shared.py`` contains objects and variables that need to be shared (except settings), like the database connection

Overview of the main classes
----------------------------

A Machine is like a typewriter: it turns all printable objects (Sheets, and everything they contain) into LaTeX. It knows how to turn a mathematical expression in LaTeX format. It knows how to draw figures from the geometrical objects (using eukleides).

The Sheet objects given to a Machine contain guidelines for the Machine: the layout of the Sheet and what Exercises it contains.

The Exercise objects contain Questions and also layout informations that might be specific to the exercise (for instance, display the equations' resolutions in two columns).

The Question objects contain the mathematical objects from the core and uses them to compute texts and answers.

The objects from the core are all different kinds of mathematical objects, like Sums, Products, Equations or Triangles, Tables... For instance, a Question about Pythagora's theorem would embed a RightTriangle (which itself embeds information on its sides, vertices, angles; and enough methods to create a picture of it) but also fields telling if the figure should be drawn in the Question's text or if only a description of the figure should be given; if the hypotenuse should be calculated or another side; if the result should be a rounded decimal and how precise it should be etc.

When a new Sheet is created, all objects it contains are created randomly, following some rules, though, to avoid completely random uninteresting results.

More details about the core objects a little bit below, in the paragraph about :ref:`the_core`.
