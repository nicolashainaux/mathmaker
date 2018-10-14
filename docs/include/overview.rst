Overview
========

Mathmaker creates elementary maths worksheets with detailed solutions.

The output documents can be compiled into pdf files by lualatex.
Examples of available themes are: first degree equations, pythagorean theorem, fractions calculation...

It can run from command line, but can be controlled via http requests too.

`License <https://gitlab.com/nicolas.hainaux/mathmaker/blob/master/LICENSE>`__

`Documentation (master release) <http://mathmaker.readthedocs.io/en/master/index.html>`__

`Documentation (latest development release) <http://mathmaker.readthedocs.io/en/dev/index.html>`_.

Quickstart
==========

.. _install:

Install
-------

Dependencies
^^^^^^^^^^^^

On Ubuntu, Manjaro, FreeBSD
"""""""""""""""""""""""""""

-  on Ubuntu 18.04+:

   ::

       $ sudo apt install python3-pip texlive-full eukleides libxml2-utils


-  on Manjaro:

   ::

       $ sudo pacman -S python-pip texlive-most libxml2 python-lxml
       $ yaourt -S eukleides


-  on FreeBSD 10.4+:

   ::

       $ sudo pkg install python36 py36-sqlite3 eukleides libxml2
       $ rehash
       $ python3.6 -m ensurepip

   .. note::
       FreeBSD users: in 2018 (mathmaker 0.7.3), the binary version of TeXLive is outdated (2015) and it is, again, necessary to install texlive directly using `texlive instructions <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-50001.3>`__. Do not forget to setup the fonts for lualatex if you intend to use them (as described in the same `page <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-340003.4.4>`__).

   .. note::

       FreeBSD users, check how to fix eukleides install in `the complete documentation <http://mathmaker.readthedocs.io/en/master/user_doc.html#eukleides-fix>`__


On other Linux or BSD platforms
"""""""""""""""""""""""""""""""

- python (3.6+) and pip

  `Python is available for most platforms <https://www.python.org/downloads/>`__.

  It is included by default in most distributions, but you may have to install it, for instance if your Ubuntu version is older than 18.04 (maybe `try this <https://www.linuxbabe.com/ubuntu/install-python-3-6-ubuntu-16-04-16-10-17-04>`__?), or on openSUSE Leap 42.3 (some hints `here <https://stackoverflow.com/questions/41558535/python-3-6-installation-and-lib64>`__ or `there <https://gist.github.com/antivanov/01ed4eac2d7486a170be598b5a0a4ac7>`__).

  pip may come automatically with python installation, or as a separate package (look for python-pip or python3-pip and ensure this is pip for python 3, not python 2!).

- a LaTeX distribution

  It must include lualatex and related tools. You can either install a full distribution or add the required packages one by one, or try to use a package that helps to download and install packages "on the fly", like `texliveonfly <https://ctan.org/pkg/texliveonfly>`__ in the case of TeX Live.

  Recommanded LaTeX distribution is actually an up to date `TeXLive <https://www.tug.org/texlive/>`__, as this is the one used in mathmaker's development and testing. Nothing prevents you from using another distribution, there is just no guarantee that it will be fully compatible.

  Some distributions provide up-to-date binary packages for TeXLive (mathmaker >= 0.7.4 requires TeXLive >= 2017). If not, the recommanded way to install TeXLive is over the internet, like `described on the official website <https://www.tug.org/texlive/acquire-netinstall.html>`__. Do not forget to setup the fonts for lualatex if you intend to use them (as described in the same `page <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-340003.4.4>`__).

- eukleides

  .. note::

    This dependency won't be required in mathmaker 0.8+

  Some distributions provide a binary package. You can also install it `directly from source <http://www.eukleides.org/download.html>`__.

- libxml2

  .. note::

    This dependency won't be required in mathmaker 0.8+

  It is available as binary package in most distributions (look for a package named libxml2).


Install mathmaker
^^^^^^^^^^^^^^^^^

Once you're done with the dependencies, you can proceed installing mathmaker:

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
`here <https://gitlab.com/nicolas.hainaux/mathmaker/tree/dev/mathmaker/data/wordings>`_. You can submit any new idea as an enhancement proposal
`there <https://gitlab.com/nicolas.hainaux/mathmaker/issues>`__ (should be written in english, french or german).

Any question can be sent to nh dot techn (hosted at gmail dot com).

As a translator
---------------

You can help translating mathmaker to your language (or any language you
like, if you have enough elementary maths vocabulary for that).

If the translation to your language isn't started yet, there are several
pot files to get `here <https://gitlab.com/nicolas.hainaux/mathmaker/tree/dev/mathmaker/locale>`__ (see explanations about their respective
roles `there <http://mathmaker.readthedocs.io/en/dev/dev_doc.html#the-real-and-the-fake-translation-files>`__). You can use an editor like
`poedit <https://poedit.net/>`__ or any other you like better, to create
po files from them and start to translate.

If you want to add missing translations, or to correct some, you can
find the po files in the subdirectories `here <https://gitlab.com/nicolas.hainaux/mathmaker/tree/dev/mathmaker/locale>`__.

Once you're done, you can make a pull request `here <https://gitlab.com/nicolas.hainaux/mathmaker/pulls>`__.

Any question can be sent to nh dot techn (hosted at gmail dot com).

As a developer
--------------

Before submitting a PR, please ensure you've had a look at the `writing rules <http://mathmaker.readthedocs.io/en/dev/dev_doc.html#writing-rules>`_.

More details can be found in the `documentation for developers <http://mathmaker.readthedocs.io/en/dev/dev_index.html>`__.

Any question can be sent to nh dot techn (hosted at gmail dot com).

.. include:: ../CONTRIBUTORS.rst

.. include:: ../CHANGELOG.rst
