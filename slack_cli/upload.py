#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Send a file to Slack from the CLI
"""

import slacker

from . import utils


def main():
    parser = utils.get_parser("Upload file to Slack")
    parser.add_argument("path", help="Path to file to upload")
    parser.add_argument("destination", help="Slack channel, group or username")
    args = parser.parse_args()

    token = utils.get_token(args.token)

    destination_id = utils.get_source_id(token, args.destination)
    slacker.Files(token).upload(args.path, channels=destination_id)
