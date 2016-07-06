#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import mathmaker
from mathmaker.lib.startup_actions import check_dependencies
from mathmaker import settings
from mathmaker.lib.tools import fonts


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


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


def create_mo_files():
    data_files = []
    localedir = 'mathmaker/locale'
    po_dirs = [localedir + '/' + l + '/LC_MESSAGES/'
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
            mo_files.append(d + mo_file)
        data_files.append((d, mo_files))
    return data_files

settings.init()
try:
    check_dependencies()
except EnvironmentError as e:
    raise EnvironmentError(str(e) + 'Once you have installed all correct '
                           'versions, you can run mathmaker\'s setup again.')

fonts.create_list()

setup(
    name=mathmaker.__software_name__,
    version=mathmaker.__version__,
    url='http://github.com/nicolas.hainaux/mathmaker/',
    license=mathmaker.__licence__,
    author=mathmaker.__author__,
    tests_require=['tox'],
    install_requires=['PyYAML>=3.11',
                      'polib>=1.0.7'],
    cmdclass={'test': PyTest,
              'tox': Tox},
    author_email=mathmaker.__author_email__,
    description='Mathmaker creates automatically elementary maths exercises '
                'and their (detailed) answers.',
    long_description=read('README.rst', 'CHANGELOG.rst'),
    packages=find_packages(exclude=['tests', 'docs']),
    entry_points={
        'console_scripts': ['mathmaker = mathmaker.cli:entry_point',
                            'mathmakerd = mathmaker.daemon:run'],
    },
    data_files=create_mo_files() + ['mathmaker/data/fonts_list.txt'],
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: ' + mathmaker.__licence__],
    extras_require={'testing': ['pytest']}
)
