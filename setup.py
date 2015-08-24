#!/usr/bin/env python
import os
from setuptools import setup, find_packages


long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.md'
    )
).read()


setup(
    name='foresight',
    author='Adam Schwalm',
    version='0.1',
    license='LICENSE',
    url='https://github.com/ALSchwalm/foresight',
    description='A library for predicting the output of random number generators.',
    long_description=long_description,
    packages=find_packages('.'),
    install_requires=[],
)
