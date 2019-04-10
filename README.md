
# synbiohub_adapter
![Build Status](https://api.travis-ci.com/SD2E/synbiohub_adapter.svg?branch=master)

synbiohub_adapter is a Python 3 package that provides an API to [SynBioHub](http://wiki.synbiohub.org/wiki/Main_Page).

synbiohub_adapter is not compatible with Python 2.


## Installation

To install the current release of synbiohub_adapter:

```shell
pip3 install git+https://github.com/SD2E/synbiohub_adapter.git@v1.1
```

### Install from git clone

You can also install from a git clone:

```shell
pip3 install .
```

### Development Install

If you would like to install synbiohub_adapter so that changes to the
source will be represented in the imported code without having to
re-install, run this command:

```shell
pip3 install -e .
```

### Running Tests

Running tests requires the user provide a password for SynBioHub through the `SBH_PASSWORD` environment variable, e.g.

```shell
SBH_PASSWORD=<pword> python3 -m unittest discover tests
```

The tests include a check for conformance with Python style best-practices. If a new style violation is introduced into
the code base, the test will fail. To diagnose this failure, run the following test:

```shell
VERBOSE=1 python3 -m unittest tests/test_pycodestyle.py
```

### Using docker and docker-compose
Run bash in docker container:

```shell
docker-compose run --rm synbiohub_adapter bash
```
