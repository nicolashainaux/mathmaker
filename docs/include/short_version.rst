Short version
-------------

.. warning::

  Git and python>=3.6 are required.

Install dependencies:
^^^^^^^^^^^^^^^^^^^^^

* Ubuntu 18.04+

  ::

    $ sudo apt-get install eukleides libxml2-utils gettext texlive-full

  .. note::

    If you work on an older Ubuntu version, then most probably the binary package is outdated (should be >= 2017), and then instead, install TeXLive over the internet, like `described on the official website <https://www.tug.org/texlive/acquire-netinstall.html>`__. Do not forget to `setup the fonts for lualatex <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-340003.4.4>`__.

* Manjaro

  ::

    $ sudo pacman -S python-pip texlive-most libxml2 python-lxml gettext
    $ yaourt -S eukleides


* FreeBSD

  ::

    $ sudo pkg install python36 py36-sqlite3 gettext eukleides libxml2
    $ rehash
    $ python3.6 -m ensurepip

  .. note::
    FreeBSD users: in 2018 (mathmaker 0.7.3), the binary version of TeXLive is outdated (2015) and it is, again, necessary to install texlive directly using `texlive instructions <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-50001.3>`__. Do not forget to setup the fonts for lualatex if you intend to use them (as described in the same `page <https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-340003.4.4>`__).

  .. note::

    You should check the :ref:`eukleides_patch_for_freebsd`

Install mathmaker in dev mode:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install mathmaker in dev mode in a venv, get to the directory where you want to work:

* Linux

  ::

    $ python3 -m venv dev0
    $ source dev0/bin/activate
    (dev0) $ pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
    (dev0) $ mkdir mathmaker
    (dev0) $ cd mathmaker/
    (dev0) $ git clone https://gitlab.com/nicolas.hainaux/mathmaker.git
    (dev0) $ python3 setup.py develop


* FreeBSD

  ::

    $ python3 -m venv dev0
    $ source dev0/bin/activate.csh
    [dev0] $ sudo pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
    [dev0] $ mkdir mathmaker
    [dev0] $ cd mathmaker/
    [dev0] $ git clone https://gitlab.com/nicolas.hainaux/mathmaker.git
    [dev0] $ python3 setup.py develop



Try it
^^^^^^

Get to an empty directory and:

::

    (dev0) $ mathmaker 06_orange_exam > out.tex 2> stderr.log && lualatex out.tex

You can check ``out.pdf`` with the pdf viewer you like.

To run the auxiliary tools:
::

    (dev0) $ cd path/to/mathmaker/toolbox/
    (dev0) $ ./build_db.py
    (dev0) $ ./update_pot_files

Most of the tests are stored under ``tests/``. Some others are doctests. Any new test or doctest will be added automatically to the tests run by ``pytest``.

Run the tests:
::

    (dev0) $ pytest -x -vv -r w tests/

Edit the settings:
::

    (dev0) $ cd path/to/mathmaker/settings/
    (dev0) $ mkdir dev/
    (dev0) $ cp default/*.yaml dev/

In ``dev/logging.yaml`` you can set the ``__main__`` logger to ``INFO`` (take care to define log rotation for ``/var/log/mathmaker``). Set the dbg logger to ``DEBUG``.

Each debugging logger can be enabled/disabled individually in ``debug_conf.yaml`` (by setting it to ``DEBUG`` or ``INFO``).

See :ref:`logging_debugging` for more details on how to setup new loggers (and debugging loggers).

You can override settings in ``dev/user_config.yaml`` to your liking.

Before starting, you should read at least the :ref:`auxiliary_tools` and :ref:`writing_rules` sections. It is certainly worth also to have a look at :ref:`user_advanced_features`.

Hope you'll enjoy working on mathmaker!
