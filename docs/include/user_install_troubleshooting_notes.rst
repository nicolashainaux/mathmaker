.. _install_notes:

Install notes
=============

.. _eukleides_patch_for_freebsd:

eukleides install fix for FreeBSD
---------------------------------

``eukleides`` currently does not work out of the box. The pkg-installed version has a functional euktoeps script, it is required, so keep it somewhere. Then do ``pkg remove eukleides`` and re-install it from source:

- get the 1.5.4 source from http://www.eukleides.org/, for instance ``wget http://www.eukleides.org/files/eukleides-1.5.4.tar.bz2``
- then ``tar xvzf eukleides-1.5.4.tar.bz2``
- then possibly modify the prefix for install in the ``Config`` file, at your liking
- remove the making of documentation and manpages from the ``install`` target in the ``Makefile`` (they cause errors)
- install the required dependencies to compile eukleides: ``pkg install bison flex gmake gcc``
- do ``gmake`` and then ``gmake install``. This will provide functional binaries.
- replace the euktoeps script by the one you did get from the pkg installed version.
- if necessary (if ``lualatex`` complains about not finding ``eukleides.sty``), reinstall ``eukleides.sty`` and ``eukleides.tex`` correctly:

    .. code-block:: console

        # mkdir /usr/local/share/texmf-dist/tex/latex/eukleides
        # cp /usr/local/share/texmf/tex/latex/eukleides/eukleides.* /usr/local/share/texmf-dist/tex/latex/eukleides/
        # mktexlsr


python-daemon error at install
------------------------------

You might get an error before the end of ``mathmaker``'s installation:

.. code-block:: console

    error: The 'python-daemon>=2.1.1' distribution was not found and is required by mathmaker

or:

.. code-block:: console

      File "/home/nico/dev/mathmaker/venv/test071_bis/lib/python3.6/site-packages/setuptools/command/easy_install.py", line 250, in finalize_options
        'dist_version': self.distribution.get_version(),
      File "/tmp/easy_install-myl7eaei/python-daemon-2.1.2/version.py", line 656, in get_version
      File "/tmp/easy_install-myl7eaei/python-daemon-2.1.2/version.py", line 651, in get_version_info
      File "/tmp/easy_install-myl7eaei/python-daemon-2.1.2/version.py", line 552, in get_changelog_path
      File "/usr/lib/python3.6/posixpath.py", line 154, in dirname
        p = os.fspath(p)
      TypeError: expected str, bytes or os.PathLike object, not NoneType


Fix it this way:

.. code-block:: console

    # pip3 install python-daemon --upgrade

And finish the install:

.. code-block:: console

    # pip3 install mathmaker
