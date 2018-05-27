#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import atexit
import subprocess
from glob import glob
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install

from mathmaker import __version__, __software_name__, __licence__, __author__
from mathmaker import __author_email__
from mathmaker.lib.tools.ignition import retrieve_fonts
from mathmaker.lib.tools.ignition import check_dependency, check_dependencies


class CustomInstallCommand(install):
    def _post_install(self):
        sys.stdout.write('\nRunning post-install script')
        if self.install_platlib is not None:
            install_lib = self.install_platlib
        elif self.install_purelib is not None:
            install_lib = self.install_purelib
        else:
            sys.stderr.write('\nCould not check whether a previous '
                             'mathmaker.db is still here. You have to check '
                             'yourself and possibly delete mathmaker.db '
                             'before the first run.')
            sys.exit(0)

        db_path = [os.path.join(install_lib, __software_name__, 'data', f)
                   for f in glob(os.path.join(install_lib, __software_name__,
                                              'data', 'mathmaker*.db'))]
        if len(db_path):
            for f in db_path:
                if os.path.isfile(f):
                    sys.stdout.write('\nRemoving a previous local database '
                                     'file (likely deprecated version): '
                                     '{}.'.format(f))
                    os.remove(f)
        else:
            sys.stdout.write('\nFound no previous mathmaker.db file to '
                             'remove.')
        sys.stdout.write('\nFinished post-install script tasks.\n')

    def __init__(self, *args, **kwargs):
        super(CustomInstallCommand, self).__init__(*args, **kwargs)
        atexit.register(self._post_install)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root.

    Taken from http://stackoverflow.com/questions/3779915/why-does-python-
    setup-py-sdist-create-unwanted-project-egg-info-in-project-r
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info '
                  './*.egg')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class Tox(TestCommand):
    # user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def create_mo_files(force=False):
    if force:
        return []
    data_files = []
    localedir = 'mathmaker/locale/'
    po_dirs = [localedir + l + '/LC_MESSAGES/'
               for l in next(os.walk(localedir))[1]]
    for d in po_dirs:
        mo_files = []
        po_files = [f
                    for f in next(os.walk(d))[2]
                    if os.path.splitext(f)[1] == '.po']
        for po_file in po_files:
            filename, extension = os.path.splitext(po_file)
            mo_file = filename + '.mo'
            msgfmt_cmd = 'msgfmt {} -o {}'.format(d + po_file, d + mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            sys.stdout.write('Compiled {}\n      as {}\n'.format(d + po_file,
                                                                 d + mo_file))
            mo_files.append(d + mo_file)
        data_files.append((d, mo_files))
    return data_files


missing_dependency = False
infos = ""

try:
    check_dependency("msgfmt", "compile the translations files at intall",
                     'msgfmt', "0.18.3")
except EnvironmentError as e:
    infos += str(e) + '\n'
    missing_dependency = True
try:
    check_dependencies()
except EnvironmentError as e:
    infos += str(e) + '\n'
    missing_dependency = True

if missing_dependency and '--force' not in sys.argv:
    raise EnvironmentError(infos + ' Once you have installed all correct '
                           'versions, you can run mathmaker\'s setup again. '
                           'You can check https://readthedocs.org/projects/'
                           'mathmaker/ to find instructions on install.')

setup(
    name=__software_name__,
    version=__version__,
    url='http://github.com/nicolas.hainaux/mathmaker/',
    license=__licence__,
    author=__author__,
    tests_require=['tox'],
    install_requires=['mathmakerlib>=0.7.0',
                      'polib>=1.0.8',
                      'python-daemon>=2.1.2',
                      'intspan>=1.5.8',
                      'ruamel.yaml>=0.15.25'],
    cmdclass={'test': PyTest,
              'tox': Tox,
              'clean': CleanCommand,
              'install': CustomInstallCommand},
    author_email=__author_email__,
    description='Mathmaker creates automatically elementary maths exercises '
                'and their (detailed) answers.',
    long_description=read('README.rst', 'CONTRIBUTORS.rst', 'CHANGELOG.rst'),
    packages=find_packages(exclude=['tests', 'docs']),
    entry_points={
        'console_scripts': ['mathmaker = mathmaker.cli:entry_point',
                            'mathmakerd = mathmaker.daemonized:entry_point'],
    },
    data_files=create_mo_files(force='--force' in sys.argv)
    + retrieve_fonts(force='--force' in sys.argv)
    + [('mathmaker/data/frameworks/',
       ['mathmaker/data/frameworks/index.json'])]
    + [('mathmaker/data/',
       ['mathmaker/data/db_index.json'])],
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: ' + __licence__,
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD'],
    extras_require={'testing': ['pytest']}
)
