#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='synbiohub_adapter',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'SPARQLWrapper>=1.8.2',
        'appdirs>=1.4.3',
        'pycodestyle>=2.5.0',
        'pysbol==2.3.1.post6',
        'requests>=2.21.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ]
)