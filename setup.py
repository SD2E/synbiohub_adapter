#!/usr/bin/env python

import pip
from pkg_resources import parse_version
from setuptools import setup, find_packages

install_requires = [
    'SPARQLWrapper>=1.8.2',
    'appdirs>=1.4.3',
    'pycodestyle>=2.5.0',
    # This syntax requires pip>=18
    'sbol@git+https://github.com/llotneb/SBOL',
    'requests>=2.21.0',
    'tenacity>=5.0.3'
]

setup(
    name='synbiohub_adapter',
    version='1.3',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ]
)
