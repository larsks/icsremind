#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='icsremind',
    version='1',
    description='Generate remind calendars from a caldav server',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='http://github.com/larsks/icsremind',
    install_requires=open('requirements.txt').readlines(),
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'icsremind=icsremind.main:main',
        ],
    }
)

