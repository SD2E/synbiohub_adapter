#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='synbiohub_adapter',
    version='1.0a0',
    packages=find_packages(),
    install_requires=['pycodestyle==2.5.0', 'SPARQLWrapper', 'appdirs', 'requests', 'pySBOLx==0.1', 'pysbol'],
    dependency_links=[
        'git+https://git@github.com/nroehner/pySBOLx.git#egg=pySBOLx-0.1'
    ]
)
