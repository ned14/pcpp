#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pcpp',
    version='0.1',
    description='A C99 preprocessor written in pure Python',
    author='Niall Douglas',
    url='http://pypi.python.org/pypi/pcpp',
    packages=['pcpp'],
    test_suite='tests',
    use_2to3=True,
    entry_points={
        'console_scripts': [ 'pcpp=pcpp:main' ]
    }
)
