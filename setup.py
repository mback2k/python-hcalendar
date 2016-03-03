#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup, find_packages
import os

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(
    name='python-hcalendar',
    version=__import__('hcalendar').__version__,
    author='Marc Hoersken',
    author_email='info@marc-hoersken.de',
    packages=find_packages(exclude=['unittests']),
    include_package_data=True,
    url='https://github.com/mback2k/python-hcalendar',
    license='MIT',
    description=' '.join(__import__('hcalendar').__doc__.splitlines()).strip(),
    install_requires=['isodate>=0.5.0', 'beautifulsoup4>=4.3.2'],
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
)
