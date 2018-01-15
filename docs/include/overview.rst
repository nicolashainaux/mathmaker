Overview
========

Mathmaker creates elementary maths worksheets with detailed solutions.

The output documents can be compiled into pdf files by lualatex.
Examples of available themes are: first degree equations, pythagorean theorem, fractions calculation...

It can run from command line, but can be controlled via http requests too.

`License <https://github.com/nicolashainaux/mathmaker/blob/master/LICENSE>`__

`Documentation (master release) <http://mathmaker.readthedocs.io/en/master/index.html>`__

`Documentation (latest development release) <http://mathmaker.readthedocs.io/en/dev/index.html>`_.

Quickstart
==========

.. _install:

Install
-------

Required (non python) dependencies are python >=3.6, euktoeps >=1.5.4, xmllint, msgfmt, lualatex, luaotfload-tool and a bunch of LaTeX packages(1)

To install them:

-  on Ubuntu, install python3.6 if it is not already installed, then:

   ::

       $ sudo apt-get install eukleides libxml2-utils gettext texlive-latex-base

   And for the yet missing LaTeX packages: you can either install the complete
   texlive distribution (takes some room on the hard disk): run
   ``$ sudo apt-get install texlive-full``, or install only the
   necessary packages:

   ::

       $ sudo apt-get install texlive-luatex texlive-latex-recommended texlive-xetex texlive-pstricks texlive-font-utils texlive-latex-extra texlive-base texlive-science texlive-pictures texlive-generic-recommended texlive-fonts-recommended texlive-fonts-extra

-  on FreeBSD(2):

   ::

       $ sudo pkg install python36 py36-sqlite3 gettext eukleides libxml2 texlive-full
       $ rehash

   .. note::
       As of 2018 (mathmaker version 0.7.3) it is necessary to install texlive directly using `texlive instructions <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-50001.3>`__. Do not forget to setup the fonts for lualatex if you intend to use them (as described in the same link).

   .. note::
       Check how to fix eukleides install in `the complete documentation <http://mathmaker.readthedocs.io/en/master/user_doc.html#eukleides-fix>`__

Once you're done, you can proceed installing mathmaker:

::

    $ pip3 install mathmaker

(this will automatically install some extra python3 libraries too:
mathmakerlib, polib, ruamel.yaml, intspan and python-daemon).

.. note::
    Check how to fix install if it stops with an error in python-daemon install, in `the complete documentation <http://mathmaker.readthedocs.io/en/master/user_doc.html#python-daemon-error-at-install>`__

Basic use
---------

::

    $ mathmaker pythagorean-theorem-short-test > out.tex
    $ lualatex out.tex

or directly:

::

    $ mathmaker pythagorean-theorem-short-test --pdf > out.pdf

Get the list of all provided sheets:

::

    $ mathmaker list

Some settings
-------------

Check ``mathmaker --help`` to see which settings can be changed as command line arguments.

Some more settings can be overriden by user defined values in
``~/.config/mathmaker/user_config.yaml``. Read `the complete
documentation <http://mathmaker.readthedocs.io/en/master/user_doc.html#user-settings>`__ for more information.

Advanced use
------------

It's possible to create your own sheets in yaml. Read `the complete documentation <http://mathmaker.readthedocs.io/en/master/user_doc.html#YAML-sheets>`__ for more information.

Contribute
==========

You can contribute to mathmaker:

As a wordings contributor
-------------------------

Mathmaker needs contexts for problems wordings. There are already some,
but the more there is, the better. Existing wordings can be found
`here <https://github.com/nicolashainaux/mathmaker/tree/dev/mathmaker/data/wordings>`_. You can submit any new idea as an enhancement proposal
`there <https://github.com/nicolashainaux/mathmaker/issues>`__ (should be written in english, french or german).

Any question can be sent to nh dot techn (hosted at gmail dot com).

As a translator
---------------

You can help translating mathmaker to your language (or any language you
like, if you have enough elementary maths vocabulary for that).

If the translation to your language isn't started yet, there are several
pot files to get `here <https://github.com/nicolashainaux/mathmaker/tree/dev/mathmaker/locale>`__ (see explanations about their respective
roles `there <http://mathmaker.readthedocs.io/en/dev/dev_doc.html#the-real-and-the-fake-translation-files>`__). You can use an editor like
`poedit <https://poedit.net/>`__ or any other you like better, to create
po files from them and start to translate.

If you want to add missing translations, or to correct some, you can
find the po files in the subdirectories `here <https://github.com/nicolashainaux/mathmaker/tree/dev/mathmaker/locale>`__.

Once you're done, you can make a pull request `here <https://github.com/nicolashainaux/mathmaker/pulls>`__.

Any question can be sent to nh dot techn (hosted at gmail dot com).

As a developer
--------------

Before submitting a PR, please ensure you've had a look at the `writing rules <http://mathmaker.readthedocs.io/en/dev/dev_doc.html#writing-rules>`_.

More details can be found in the `documentation for developers <http://mathmaker.readthedocs.io/en/dev/dev_index.html>`__.

Any question can be sent to nh dot techn (hosted at gmail dot com).

.. include:: ../CONTRIBUTORS.rst

.. include:: ../CHANGELOG.rst


--------------

**Footnotes:**

(1) Complete list of recommended LaTeX packages (list up-to-date for 0.7 release):

+---------------------+--------------------------------+
| CTAN Package Name   | Package name (Ubuntu 14.04 )   |
+=====================+================================+
| fontspec            | texlive-latex-recommended      |
+---------------------+--------------------------------+
| polyglossia         | texlive-xetex                  |
+---------------------+--------------------------------+
| geometry            | texlive-latex-base             |
+---------------------+--------------------------------+
| graphicx            | texlive-pstricks               |
+---------------------+--------------------------------+
| epstopdf            | texlive-font-utils             |
+---------------------+--------------------------------+
| tikz                | texlive-latex-extra            |
+---------------------+--------------------------------+
| amssymb             | texlive-base                   |
+---------------------+--------------------------------+
| amsmath             | texlive-latex-base             |
+---------------------+--------------------------------+
| siunitx             | texlive-science                |
+---------------------+--------------------------------+
| cancel              | texlive-pictures               |
+---------------------+--------------------------------+
| array               | texlive-latex-base             |
+---------------------+--------------------------------+
| ulem                | texlive-generic-recommended    |
+---------------------+--------------------------------+
| textcomp            | texlive-latex-base             |
+---------------------+--------------------------------+
| eurosym             | texlive-fonts-recommended      |
+---------------------+--------------------------------+
| lxfonts             | texlive-fonts-extra            |
+---------------------+--------------------------------+
| multicol            | texlive-latex-base             |
+---------------------+--------------------------------+

(2) Using ``pkg``, you'll have to install ``texlive-full``; if you wish
    to install only the relevant LaTeX packages, you'll have to browse
    the ports, I haven't done this yet so cannot tell you exactly which
    ones are necessary.
