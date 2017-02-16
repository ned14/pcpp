#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pcpp',
    version='0.01',
    description='A C99 preprocessor written in pure Python',
    author='Niall Douglas',
    url='http://pypi.python.org/pypi/pcpp',
    packages=find_packages(),
    test_suite='test',
    use_2to3=True,
)
