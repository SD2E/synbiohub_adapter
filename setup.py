#!/usr/bin/env python

import pip
from pkg_resources import parse_version
from setuptools import setup, find_packages

install_requires = [
    'SPARQLWrapper>=1.8.2',
    'appdirs>=1.4.3',
    'pycodestyle>=2.5.0',
    'requests>=2.21.0',
    'sbol2',
    'tenacity>=5.0.3'
]

setup(
    name='synbiohub_adapter',
    version='1.4',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ]
)
