#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import platform
import subprocess

def pip_install(url):
    subprocess.check_output([sys.executable, '-m', 'pip', 'install', url])

def py_version():
    return tuple(sys.version_info[:2])

def install_version(include_dist_version=True):
    py_v = py_version()
    if include_dist_version:
        dist_v = tuple(platform.dist()[0:2])
    else:
        dist_v = tuple(platform.dist()[0:1])
    return py_v + dist_v

class UnsupportedPythonDistVersion(Exception): pass
class UnknownUrllibImport(Exception): pass
class PysbolInstallFailed(Exception): pass

wheels = {
    (2, 7, 'Ubuntu', '16.04'): {
        'url': 'https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_2/dist/pySBOL-2.3.0.post11-cp27-none-any.whl?raw=true',
        'name': 'pySBOL-2.3.0.post11-cp27-none-any.whl'
    },
    (2, 7, 'Ubuntu', '17.10'): {
        'url': 'https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_2/dist/pySBOL-2.3.0.post11-cp27-none-any.whl?raw=true',
        'name': 'pySBOL-2.3.0.post11-cp27-none-any.whl'
    },
    (3, 5, 'Ubuntu', '16.04'): {
        'url': 'https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-cp35-none-any.whl?raw=true',
        'name': 'pySBOL-2.3.0.post11-cp35-none-any.whl'
    },
    (3, 5, 'Ubuntu', '17.10'): {
        'url': 'https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-cp35-none-any.whl?raw=true',
        'name': 'pySBOL-2.3.0.post11-cp35-none-any.whl'
    },
    (3, 6, 'Ubuntu', '16.04'): {
        'url': 'https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-cp36-none-any.whl?raw=true',
        'name': 'pySBOL-2.3.0.post11-cp36-none-any.whl'
    },
    (3, 6, 'Ubuntu', '17.10'): {
        'url': 'https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-cp36-none-any.whl?raw=true',
        'name': 'pySBOL-2.3.0.post11-cp36-none-any.whl'
    }
}


def override_run(cls):
    """
    Decorator to override the run method for a setup command to use the custom python
    linux version if the platform is linux
    """
    orig_run = cls.run
    
    def new_run(self):
        py_v = py_version()
        inst_v_1 = install_version(include_dist_version=True)
        inst_v_2 = install_version(include_dist_version=False)
        
        if inst_v_1 in wheels:
            inst_v = inst_v_1
        elif inst_v_2 in wheels:
            inst_v = inst_v_2
        else:
            raise UnsupportedPythonDistVersion('No wheel file available for your linux distribution and python version {}. Supported versions: {}'.format(inst_v_1, sorted(wheels.keys())))

        url = wheels[inst_v]['url']
        name = wheels[inst_v]['name']

        import shutil
        import tempfile
        import os
        import site
        
        if py_v[0] == 3:
            import urllib.request as _urllib
        elif py_v[0] == 2:
            import urllib as _urllib
        else:
            raise UnknownUrllibImport('No urllib import specified for python version {}'.format(py_v))

        tmp_dir = None
        try:
            tmp_dir = tempfile.mkdtemp()
            wheel_path = os.path.join(tmp_dir, name)
            response = _urllib.urlopen(url)
            with  open(wheel_path, 'wb') as f:
                shutil.copyfileobj(response, f)

            # What if installing sbh_adapter with --user?
            # Probably should install pysbol with --user
            # How could we tell here?
            pip_install(wheel_path)

            # Will this error? Hopefully not. Crash the install if so.
            try:
                if py_v[0] == 2:
                    _reload = reload
                elif py_v[0] == 3:
                    from importlib import reload as _reload
                    
                _reload(site)
                import sbol
            except ImportError as e:
                raise PysbolInstallFailed(str(e))

        finally:
            if os.path.isdir(tmp_dir):
                shutil.rmtree(tmp_dir)

        pip_install('git+https://github.com/nroehner/pySBOLx')
        orig_run(self)

    cls.run = new_run
    return cls

    
@override_run
class LinuxInstallCommand(install):
    pass


@override_run
class LinuxDevelopCommand(develop):
    pass
        
install_requires=['SPARQLWrapper']
cmdclass = {}
        
if sys.platform in {'linux', 'linux2'}:
    # Use a custom install command to allow installing
    # custom pysbol wheel files
    cmdclass['install'] = LinuxInstallCommand
    cmdclass['develop'] = LinuxDevelopCommand
else:
    # Can use normal pysbol for mac and windows
    install_requires.append('pysbol')
    install_requires.append('pySBOLx')


setup(
    name='sbh_adapter',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=[
        'git+https://git@github.com/nroehner/pySBOLx.git#egg=pySBOLx'
    ],
    cmdclass=cmdclass
)
