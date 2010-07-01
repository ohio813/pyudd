#!/usr/bin/env python

from setuptools import setup

import pyudd

setup(
    name='pyudd',
    version=pyudd.__version__,
    description='OllyDbg UDD management module',
    author=pyudd.__author__,
    author_email=pyudd.__contact__,
    url='http://code.google.com/p/pyudd',
    py_modules=['pyudd'],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
    )
