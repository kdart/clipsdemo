#!/usr/bin/python
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

import os
from setuptools import setup
from glob import glob

NAME = "clipsdemo"
VERSION = open("VERSION").read().strip()

setup (name=NAME, version=VERSION,
    #namespace_packages = ["namespace"],
    package_dir = {'': 'src'},
    packages = ["clipsdemo",],
    scripts = glob("bin/*"),
    package_data = {
        'clipsdemo': ['*.kv', '*.clp'],
    },
    #install_requires = ['kivy>=1.8', 'pyclips'],
    test_suite = "test.Tests",

    author = "Keith Dart",
    author_email = "keith@dartworks.biz",
    description = "Simple clips engine demonstration and learning tool.",
    long_description = """Simple clips engine demonstration using pyclips and kivy.
    """,
    license = "LGPL",
    keywords = "Python",
    classifiers = ["Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Intended Audience :: Developers"],
)

