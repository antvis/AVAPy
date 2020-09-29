#!/usr/bin/env python3

"""
Python Automatic Visual Analyze Library.
"""

from setuptools import find_packages, setup

setup(
    name='AVAPy',
    packages=find_packages(include=['AVAPy']),
    version='0.1.0',
    description='AVA Python Library',
    author='AFX',
    license='MIT',
    install_requires=['pandas', 'altair'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
