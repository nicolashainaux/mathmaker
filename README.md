[![PyPI1](https://img.shields.io/pypi/v/mathmaker.svg?maxAge=2592000)](https://pypi.python.org/pypi/mathmaker)
[![PyPI2](https://img.shields.io/pypi/status/mathmaker.svg?maxAge=2592000)]()
[![PyPI3](https://img.shields.io/pypi/pyversions/mathmaker.svg?maxAge=2592000)]()
[![Build Status](https://travis-ci.org/nicolashainaux/mathmaker.svg?branch=dev)](https://travis-ci.org/nicolashainaux/mathmaker)
[![Coveralls branch](https://img.shields.io/coveralls/nicolashainaux/mathmaker/dev.svg?maxAge=2592000)](https://coveralls.io/github/nicolashainaux/mathmaker)
[![Documentation Status1](https://readthedocs.org/projects/mathmaker/badge/?version=master)](http://mathmaker.readthedocs.io/en/master/)
[![Documentation Status2](https://readthedocs.org/projects/mathmaker/badge/?version=dev)](http://mathmaker.readthedocs.io/en/dev/) [![Maintenance](https://img.shields.io/maintenance/yes/2016.svg?maxAge=2592000)](https://github.com/nicolashainaux/mathmaker/)

[![PyPI4](https://img.shields.io/pypi/l/mathmaker.svg?maxAge=2592000)](https://github.com/nicolashainaux/mathmaker/blob/master/LICENSE)

Overview
========

Mathmaker creates elementary maths worksheets with detailed solutions.

The output documents can be compiled into pdf files by lualatex.
Examples of available themes are: first degree equations, pythagorean
theorem, fractions calculation...

It can run from command line, but can be controlled via http requests
too.

[License](https://github.com/nicolashainaux/mathmaker/blob/master/LICENSE)

[Documentation (master release)](http://mathmaker.readthedocs.io/en/master/index.html)
[Documentation (latest development version))](http://mathmaker.readthedocs.io/en/dev/index.html).

Quickstart
==========

Complete install
----------------

-   on Ubuntu 14.04 or later:

    External dependencies:

        $ sudo apt-get install eukleides libxml2-utils gettext texlive-full

    Note: to avoid installing `texlive-full`, check the  [documentation](http://mathmaker.readthedocs.io/en/master/user_doc.html#install).

    Then:

        $ pip3 install mathmaker

-   on FreeBSD 10.*:

    External dependencies:

        $ sudo pkg install python34 py34-sqlite3 gettext eukleides libxml2 texlive-full
        $ rehash

    > **note**
    >
    > Because of a bug in current FreeBSD's eukleides package you'll have to fix eukleides install. See [here](http://mathmaker.readthedocs.io/en/master/user_doc.html#eukleides-fix).

    Once you're done, you can proceed installing mathmaker:

        $ pip3 install mathmaker

    > **note**
    >
    > If you stumble upon an error during the install of the python-daemon dependency, you'll find the way to solve it [there](http://mathmaker.readthedocs.io/en/master/user_doc.html#python-daemon-error-at-install)

Basic use
---------

    $ mathmaker pythagorean-theorem-short-test > out.tex
    $ lualatex out.tex

or directly:

    $ mathmaker pythagorean-theorem-short-test --pdf > out.pdf

Get the list of all provided sheets(3):

    $ mathmaker list

To get the command-line options, you can use `mathmaker --help`.

Several settings can be overriden by user defined values in
`~/.config/mathmaker/user_config.yaml`. Read [the complete
documentation](http://mathmaker.readthedocs.io/en/master/user_doc.html#user-settings) for more information.

Advanced use
------------

It's possible to create your own sheets in xml (only for the mental
calculation theme yet). Read [the complete
documentation](http://mathmaker.readthedocs.io/en/master/user_doc.html#xml-sheets)
for more information.

Contribute
==========

You can contribute to mathmaker:

As a wordings contributor
-------------------------

Mathmaker needs contexts for problems wordings. There are already some,
but the more there is, the better. Existing wordings can be found
[here](https://github.com/nicolashainaux/mathmaker/tree/dev/mathmaker/data/wordings).
You can submit any new idea as an enhancement proposal
[there](https://github.com/nicolashainaux/mathmaker/issues) (should be
written in english, french or german).

Any question can be sent to nh dot techn (hosted at gmail dot com).

As a translator
---------------

You can help translating mathmaker to your language (or any language you
like, if you have enough elementary maths vocabulary for that).

If the translation to your language isn't started yet, there are several
pot files to get
[here](https://github.com/nicolashainaux/mathmaker/tree/dev/mathmaker/locale)
(see explanations about their respective roles
[there](http://mathmaker.readthedocs.io/en/dev/dev_doc.html#the-real-and-the-fake-translation-files)).
You can use an editor like [poedit](https://poedit.net/) or any other
you like better, to create po files from them and start to translate.

If you want to add missing translations, or to correct some, you can
find the po files in the subdirectories
[here](https://github.com/nicolashainaux/mathmaker/tree/dev/mathmaker/locale).

Once you're done, you can make a pull request
[here](https://github.com/nicolashainaux/mathmaker/pulls).

Any question can be sent to nh dot techn (hosted at gmail dot com).

As a developer
--------------

Before submitting a PR, please ensure you've had a look at the [writing
rules](http://mathmaker.readthedocs.io/en/dev/dev_doc.html#writing-rules).

More details can be found in the [documentation for
developers](http://mathmaker.readthedocs.io/en/dev/dev_index.html).

Any question can be sent to nh dot techn (hosted at gmail dot com).

Additional informations
-----------------------

Contact: nh dot techn (hosted by gmail dot com)

[Changelog](https://github.com/nicolashainaux/mathmaker/blob/master/CHANGELOG.rst)

[Contributors](https://github.com/nicolashainaux/mathmaker/blob/master/CONTRIBUTORS.rst)