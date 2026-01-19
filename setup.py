#!/usr/bin/env python

from setuptools import setup
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

# Read version from pcpp/pcmd.py without importing it
with open(os.path.join(here, 'pcpp', 'pcmd.py')) as f:
    content = f.read()
    version_match = re.search(r"^version=['\"]([^'\"]*)['\"]", content, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='pcpp',
    version=version,
    description='A C99 preprocessor written in pure Python',
    long_description=long_description,
    author='Niall Douglas and David Beazley',
    url='https://github.com/ned14/pcpp',
    packages=['pcpp', 'pcpp.ply.ply'],
    package_data={'pcpp' : ['../LICENSE.txt']},
    test_suite='tests',
    entry_points={
        'console_scripts': [ 'pcpp=pcpp:main' ]
    },
    options={'bdist_wheel':{'universal':False}},  # Changed to False since we're Python 3 only now
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
