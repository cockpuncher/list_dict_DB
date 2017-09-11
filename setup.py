#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals, absolute_import

from setuptools import setup

setup(
    name='list_dict_DB',
    py_modules=['list_dict_DB'],
    long_description=open('README.rst').read(),
    version='20170911.2',
    description='in memory database like object with O(1) queries',
    url='https://github.com/Jwink3101/list_dict_db',
    author='Justin Winokur',
    author_email='Jwink3101@gmail.com',
)
