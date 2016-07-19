.. _freebsd_notes:

FreeBSD notes
=============

.. _eukleides_patch_for_freebsd:

eukleides fix
-------------

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

    /usr/local/venv/mm0/lib/python3.4/site-packages/setuptools/dist.py:294: UserWarning: The version specified ('UNKNOWN') is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.
      "details." % self.metadata.version
    creating /usr/local/venv/mm0/lib/python3.4/site-packages/python_daemon-UNKNOWN-py3.4.egg
    Extracting python_daemon-UNKNOWN-py3.4.egg to /usr/local/venv/mm0/lib/python3.4/site-packages
    Adding python-daemon UNKNOWN to easy-install.pth file
    Installed /usr/local/venv/mm0/lib/python3.4/site-packages/python_daemon-UNKNOWN-py3.4.egg
    error: The 'python-daemon>=2.1.1' distribution was not found and is required by mathmaker
    [mm0] root@testmm0:/usr/local/src/mathmaker #

Fix it this way:

.. code-block:: console

    # pip3 install python-daemon --upgrade

And finish the install:

.. code-block:: console

    # pip3 install mathmaker
