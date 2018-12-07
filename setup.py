#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

setup(
    name="slack-cli",
    version="2.1.0",
    description="Slack CLI for productive developers",
    long_description=(read('README.rst')),
    url="https://github.com/regisb/slack-cli",
    install_requires=[
        "appdirs<1.5",
        "slacker<0.12.0",
        "websocket-client<0.55.0",
    ],
    license='MIT',
    author="Régis Behmo",
    author_email="nospam@behmo.com",
    packages=['slackcli'],
    entry_points={
        'console_scripts': [
            'slack-cli=slackcli.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
