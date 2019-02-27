#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='synbiohub_adapter',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['SPARQLWrapper', 'appdirs', 'requests', 'pysbol']
)
