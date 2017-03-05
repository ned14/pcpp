#!/usr/bin/env python

from setuptools import setup, find_packages
import os, pcpp

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'Readme.rst')) as f:
    long_description = f.read()
    
setup(
    name='pcpp',
    version=pcpp.version,
    description='A C99 preprocessor written in pure Python',
    long_description=long_description,
    author='Niall Douglas and David Beazley',
    url='http://pypi.python.org/pypi/pcpp',
    packages=['pcpp'],
    test_suite='tests',
    entry_points={
        'console_scripts': [ 'pcpp=pcpp:main' ]
    },
    install_requires=['ply'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
