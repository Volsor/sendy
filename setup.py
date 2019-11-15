#!/usr/bin/env python

from setuptools import setup

setup(
    name='sendy',
    version='0.2',
    description='Sendy.co API wrapper',
    license='MIT',
    author='Stanislav Shershnev',
    author_email='shershnev.stas@gmail.com',
    url='https://github.com/Volsor/sendy',
    packages=['sendy'],
    install_requires=['requests'],
    tests_require=['pytest'],
    python_requires='>=3.6',
)
