#!/usr/bin/env python

import pip
from pkg_resources import parse_version
from setuptools import setup, find_packages

install_requires = [
    'SPARQLWrapper>=1.8.2',
    'appdirs>=1.4.3',
    'pycodestyle>=2.5.0',
    'pysbol==2.3.1.post6',
    'requests>=2.21.0',
    'tenacity>=5.0.3'
]

pip_version = parse_version(pip.__version__)
if pip_version >= parse_version('19.0.0'):
    # dependency specification changed in pip 19.0
    dependency_links = []
    install_requires.append('pysbolx @ git+https://git@github.com/nroehner/pySBOLx.git@master')
else:
    dependency_links = [
        'git+https://git@github.com/nroehner/pySBOLx.git#egg=pySBOLx-0.1'
    ]
    install_requires.append('pySBOLx==0.1')

setup(
    name='synbiohub_adapter',
    version='1.1',
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ]
)
