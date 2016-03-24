#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Send a message to Slack from the CLI
"""

import sys

from . import utils


def main():
    parser = utils.get_parser("Send input from stdin to Slack")
    parser.add_argument("destination", help="Slack channel, group or username")
    args = parser.parse_args()

    token = utils.get_token(args.token)
    destination_id = utils.get_source_id(token, args.destination)

    message = "".join([line for line in sys.stdin])
    utils.ChatAsUser(token).post_formatted_message(destination_id, message, pre=True)
