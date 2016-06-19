#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import mathmaker


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

setup(
    name=mathmaker.lib.__software_name__,
    version=mathmaker.lib.__version__,
    url='http://github.com/zezollo/mathmaker/',
    license=mathmaker.lib.__licence__,
    author=mathmaker.lib.__author__,
    tests_require=['pytest'],
    install_requires=['PyYAML>=3.11',
                      'polib>=1.0.7'],
    cmdclass={'test': PyTest},
    author_email=mathmaker.lib.__author_email__,
    description='Mathmaker creates automatically elementary maths exercises '
                'and their (detailed) answers.',
    long_description=read('README.rst', 'CHANGELOG.rst'),
    packages=find_packages(exclude=['tests']),
    #    package_dir={'mathmaker': 'mathmaker'},
    entry_points={
        'console_scripts': ['mathmaker = mathmaker.cli:entry_point'],
    },
    data_files=create_mo_files(),
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: ' + mathmaker.lib.__licence__],
    extras_require={'testing': ['pytest']}
)

"""
setup(

    package_dir={'python_boilerplate':
                 'python_boilerplate'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='python_boilerplate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
"""
