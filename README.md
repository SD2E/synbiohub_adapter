
# synbiohub_adapter
![Build Status](https://api.travis-ci.com/SD2E/synbiohub_adapter.svg?branch=master)

## Installation


To install synbiohub_adapter so it is importable by python, run one
of the two commands below.

```
python setup.py install
```

or 

```
pip install .
```

### Development Install

If you would like to install synbiohub_adapter so that changes to the
source will be represented in the imported code without having to
re-install, run one of the two commands below.

```
python setup.py develop
```

```
pip install -e .
```

### Running Tests

Running tests requires the user provide a password for SynBioHub through the `SBH_PASSWORD` environment variable, e.g.

```
SBH_PASSWORD=<pword> python3 -m unittest discover tests
```

### Linux Prerequisites

On linux, you will to install `libxslt-dev` and `curl`.

```
apt-get install curl libxslt-dev
```
>>>>>>> Update install instructions in readme


### Using docker and docker-compose
Run bash in docker container:
```
docker-compose run --rm synbiohub_adapter bash
```
