#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='synbiohub_adapter',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['SPARQLWrapper', 'appdirs', 'requests', 'pySBOLx==0.1', 'pysbol'],
    dependency_links=[
        'git+https://git@github.com/nroehner/pySBOLx.git#egg=pySBOLx-0.1'
    ]
)
