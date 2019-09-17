#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

NAME = 'aeroframe'
VERSION = '0.0.1'
AUTHOR = 'Aaron Dettmann'
EMAIL = 'dettmann@kth.se'
DESCRIPTION = 'Framework for aeroelastic analyses'
URL = ''
REQUIRES_PYTHON = '>=3.6.0'
REQUIRED = []
README = ''
LICENSE = 'Apache License 2.0'

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    url=URL,
    include_package_data=True,
    license=LICENSE,
    packages=[],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    classifiers=[
        "Development Status :: 1 - Planning",
    ],
)
