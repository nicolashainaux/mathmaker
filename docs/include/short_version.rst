Short version
-------------

Install dependencies:

* Ubuntu::

   $ sudo apt-get install eukleides libxml2-utils gettext texlive-full

* FreeBSD::

   $ sudo pkg install python34 py34-sqlite3 gettext eukleides libxml2 texlive-full
   $ rehash

And FreeBSD users should check the :ref:`eukleides_patch_for_freebsd`

To install mathmaker in dev mode in a venv, get to the directory where you want to work, and (assuming git and python3.4 are installed):

* Ubuntu::

    $ pyvenv-3.4 dev0
    $ source dev0/bin/activate
    (dev0) $ pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
    (dev0) $ mkdir mathmaker
    (dev0) $ cd mathmaker/
    (dev0) $ git clone https://github.com/nicolashainaux/mathmaker.git
    (dev0) $ python3 setup.py develop


* FreeBSD::

    $ pyvenv-3.4 dev0
    $ source dev0/bin/activate.csh
    [dev0] $ sudo pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
    [dev0] $ mkdir mathmaker
    [dev0] $ cd mathmaker/
    [dev0] $ git clone https://github.com/nicolashainaux/mathmaker.git
    [dev0] $ python3 setup.py develop



Usage: get to an empty directory and:

::

    (dev0) $ mathmaker test_11_2 > out.tex
    (dev0) $ lualatex out.tex

You can check ``out.pdf`` with the pdf viewer you like.

Run the tools:
::

    (dev0) $ cd path/to/mathmaker/tools/
    (dev0) $ ./build_db.py
    (dev0) $ ./update_pot_files

Most of the tests are stored under ``tests/``. Some others are doctests. Any new test or doctest will be added automatically to the tests run by ``py.test`` or ``tox``.

Run the tests:
::

    (dev0) $ py.test
    (dev0) $ tox

Tox will ignore missing python interpreters.

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
