#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'redis',
    'selenium',
    'cherrypy',
]

test_requirements = []

setup(
    name='nifty50-scraper',
    version='0.1.1',
    description="Python module to extract data from NSE India for Nifty50",
    long_description=readme,
    author="Ritesh Shrivastav",
    author_email='ritesh_shrv@live.com',
    url='',
    packages=[
        'nifty50',
    ],
    package_dir={'nifty50': 'nifty50'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    keywords='nifty50-scraper',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
