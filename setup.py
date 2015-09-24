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
    download_url='https://github.com/ALSchwalm/foresight/tarball/0.1',
    description='A library for predicting the output of random number generators.',
    long_description=long_description,
    packages=find_packages('.', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[],
        entry_points={
        'console_scripts': [
            'foresee = foresight.foresee:main',
        ]
    },
    keywords=['predict', 'random', 'rng']
)
