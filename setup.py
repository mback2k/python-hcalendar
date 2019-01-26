#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup, find_packages
from hcalendar import __version__ as version
from hcalendar import __doc__ as doc
import os

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        with open(filepath, 'r') as fh:
            return fh.read()
    except IOError:
        return ''

setup(
    name='python-hcalendar',
    version=version,
    author='Marc Hoersken',
    author_email='info@marc-hoersken.de',
    packages=find_packages(exclude=['unittests']),
    include_package_data=True,
    url='https://github.com/mback2k/python-hcalendar',
    license='MIT',
    description=' '.join(doc.splitlines()).strip(),
    install_requires=read_file('requirements.txt').splitlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
)
