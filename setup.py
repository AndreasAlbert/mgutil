from setuptools import setup, find_packages
import sys

requirements = []
if sys.version_info < (3,7,0):
    requirements.append('dataclasses')

setup(
    name = 'mgutil',
    version = '0.0.1',
    url = 'https://github.com/AndreasAlbert/mgutil',
    author = 'Andreas Albert',
    author_email = 'andreas.albert@cern.ch',
    description = 'Standalone utilities to deal with madgraph output',
    packages = find_packages(),
    install_requires=requirements
)
