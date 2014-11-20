#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

setup(
    name='koosli',
    version='1.0.0',
    author='Koosli',
    author_email='webmaster@koosli.org',
    url='https://github.com/Koosli/koosli.org',
    description='Koosli frontpage',
    packages=find_packages(),
    package_data={
        '': [
            path.join('templates', '*.html'),
            path.join('templates', '*', '*.html'),
        ],
    },
    entry_points={
        'console_scripts': [
            'manage.py = koosli.manage:main'
        ]
    },
    zip_safe=False
)
