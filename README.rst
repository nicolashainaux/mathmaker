Overview
========

Mathmaker creates elementary maths worksheets with detailed solutions.

The output documents can be compiled into pdf files by lualatex.
Examples of available themes are: first degree equations, pythagorean
theorem, fractions calculation...

.. warning::

    The links in this document are not up-to-date but will be, very quickly

Quickstart
==========

Install
-------

Required dependencies:

-  python >=3.4
-  euktoeps >=1.5.4
-  xmllint
-  msgfmt
-  lualatex
-  a bunch of LaTeX packages(1)

To install them:

-  on Ubuntu, python3.4 is already installed, so:

   ::

       $ sudo apt-get install eukleides libxml2-utils gettext texlive-latex-base

   And for the LaTeX packages: you can either install the complete
   texlive distribution (takes some room on the hard disk): run
   ``$ sudo apt-get install texlive-full``, or install only the
   necessary packages:

   ::

       $ sudo apt-get install texlive-luatex texlive-latex-recommended texlive-xetex texlive-pstricks texlive-font-utils texlive-latex-extra texlive-base texlive-latex-base texlive-science texlive-pictures texlive-generic-recommended texlive-fonts-recommended texlive-fonts-extra

-  on FreeBSD(2):

   ::

       $ sudo pkg install python34 py34-sqlite3 gettext eukleides libxml2 texlive-full
       $ rehash

Once you're done, you can proceed installing mathmaker:

::

    $ pip3 install mathmaker

(this will automatically install three extra python3 libraries too:
polib, PyYAML and python-daemon).

Basic use
---------

::

    $ mathmaker pythagorean-theorem-short-test > out.tex
    $ lualatex out.tex

Get the list of all provided sheets(3):

::

    $ mathmaker list

Some settings
-------------

The default settings can be overriden by user defined values in
``~/.config/mathmaker/user_config.yaml``. Read `the complete
documentation <>`__ for more information.

Some of them can be changed as mathmaker options:

::

    $ mathmaker --help
    usage: mathmaker [-h] [-l LANG] [--pdf] [-d OUTPUTDIR] [-f FONT]
                     [--encoding ENCODING] [--version]
                     [DIRECTIVE|FILE]

    Creates maths exercices sheets and their solutions.

    positional arguments:
      [DIRECTIVE|FILE]      this can either match a sheetname included in
                            mathmaker, or a mathmaker xml file, or it may be the
                            special directive "list", that will print the complete
                            list and exit.

    optional arguments:
      -h, --help            show this help message and exit
      -l LANG, --language LANG
                            force the language of the output to LANGUAGE. This
                            will override any value you may have set in
                            ~/.config/mathmaker/user_config.yaml
      --pdf                 the output will be in pdf format instead of LaTeX
      -d OUTPUTDIR, --output-directory OUTPUTDIR
                            where to put the possible output files, like pictures.
                            This will override any value you may have set
                            ~/.config/mathmaker/user_config.yaml. Left undefined,
                            the default will be current directory.
      -f FONT, --font FONT  The font to use. If it's not installed on your system,
                            lualatex will not be able to compile the document.
                            This will override any value you may have set in
                            ~/.config/mathmaker/user_config.yaml
      --encoding ENCODING   The encoding to use. Take care it's available on your
                            system, otherwise lualatex will not be able to compile
                            the document. This will override any value you may
                            have set in ~/.config/mathmaker/user_config.yaml
      --version, -v         show program's version number and exit

Advanced use
------------

It's possible to create your own sheets in xml (only for the mental
calculation theme yet). Read `the complete documentation <>`__ for more
information.

Contribute
==========

You can contribute to mathmaker:

As a wordings contributor
-------------------------

Mathmaker needs contexts for problems wordings. There are already some,
but the more there is, the better. Existing wordings can be found
[here][]. You can submit any new idea as an enhancement proposal
`there <>`__ (should be written in english, french or german).

As a translator
---------------

You can help translating mathmaker to your language (or any language you
like, if you have enough elementary maths vocabulary for that).

If the translation to your language isn't started yet, there are several
pot files to get `here <>`__ (see explanations about their respective
roles `there <>`__). You can use an editor like
`poedit <https://poedit.net/>`__ or any other you like better, to create
po files from them and start to translate.

If you want to add missing translations, or to correct some, you can
find the po files in the subdirectories `here <>`__.

Once you're done, you can send the po files to `??? <>`__.

As a developer
--------------

Please check the `documentation for developers <>`__.

--------------

**Footnotes:**

(1) Complete list of recommended LaTeX packages:

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

(3) Complete list of provided sheets:

+-----------------------+------------------+-----------------------------------------------------------------+
| Theme                 | Subtheme         | Directive name                                                  |
+=======================+==================+=================================================================+
| algebra               |                  | algebra-balance-01                                              |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-binomial-identities-expansion                           |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-expression-expansion                                    |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-expression-reduction                                    |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-factorization-01                                        |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-factorization-02                                        |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-factorization-03                                        |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-mini-test-0                                             |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-mini-test-1                                             |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-short-test                                              |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               |                  | algebra-test-2                                                  |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               | equations        | equations-basic                                                 |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               | equations        | equations-classic                                               |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               | equations        | equations-harder                                                |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               | equations        | equations-short-test                                            |
+-----------------------+------------------+-----------------------------------------------------------------+
| algebra               | equations        | equations-test                                                  |
+-----------------------+------------------+-----------------------------------------------------------------+
| geometry              | right triangle   | converse-and-contrapositive-of-pythagorean-theorem-short-test   |
+-----------------------+------------------+-----------------------------------------------------------------+
| geometry              | right triangle   | pythagorean-theorem-short-test                                  |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | divisions                                                       |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | mini\_problems                                                  |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | multi\_11\_15\_25                                               |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | multi\_decimal                                                  |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | multi\_hole\_any\_nb                                            |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | multi\_hole\_tables2\_9                                         |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | multi\_reversed                                                 |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | ranks                                                           |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | tables2\_9                                                      |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_1         | test\_11\_1                                                     |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_2         | multi\_divi\_10\_100\_1000                                      |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_2         | operations\_vocabulary                                          |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_2         | polygons\_perimeters                                            |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_2         | rectangles                                                      |
+-----------------------+------------------+-----------------------------------------------------------------+
| mental\_calculation   | lev11\_2         | test\_11\_2                                                     |
+-----------------------+------------------+-----------------------------------------------------------------+
| numeric calculation   | fractions        | fraction-simplification                                         |
+-----------------------+------------------+-----------------------------------------------------------------+
| numeric calculation   | fractions        | fractions-product-and-quotient                                  |
+-----------------------+------------------+-----------------------------------------------------------------+
| numeric calculation   | fractions        | fractions-sum                                                   |
+-----------------------+------------------+-----------------------------------------------------------------+

