#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

def get_requirements():
    path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = [l.strip() for l in open(path)]
    try:
        import argparse# pylint: disable=unused-variable
    except ImportError:
        requirements.append('argparse')
    return requirements

setup(
    name="slack-cli",
    version="0.2.0",
    description="Interact with Slack from the command line",
    long_description=(read('README.rst')),
    url="https://github.com/regisb/slack-cli",
    install_requires=[
        "slacker==0.9.9",
        "websocket-client==0.35.0"
    ],
    license='MIT',
    author="Régis Behmo",
    author_email="nospam@behmo.com",
    packages=['slack_cli'],
    entry_points={
        'console_scripts': [
            'slack-pipe=slack_cli.pipe:main',
            'slack-run=slack_cli.run:main',
            'slack-send=slack_cli.send:main',
            'slack-stream=slack_cli.stream:main',
            'slack-upload=slack_cli.upload:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
