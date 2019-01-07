#!/usr/bin/env python

from setuptools import setup, find_packages
import os, pcpp

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()
    
setup(
    name='pcpp',
    version=pcpp.version,
    description='A C99 preprocessor written in pure Python',
    long_description=long_description,
    author='Niall Douglas and David Beazley',
    url='http://pypi.python.org/pypi/pcpp',
    packages=['pcpp', 'pcpp/ply/ply'],
    package_data={'pcpp' : ['../LICENSE.txt']},
    test_suite='tests',
    entry_points={
        'console_scripts': [ 'pcpp=pcpp:main' ]
    },
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
