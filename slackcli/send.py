#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Send a message to Slack from the CLI
"""

from . import utils


def main():
    parser = utils.get_parser("Send messages to Slack")
    parser.add_argument("--pre", action="store_true", help="Post as verbatim `message`")
    parser.add_argument("message", help="Message to send.")
    parser.add_argument("destination", help="Slack channel, group or username")
    args, token = utils.parse_args(parser)

    destination_id = utils.get_source_id(token, args.destination)
    utils.ChatAsUser(token).post_formatted_message(destination_id, args.message, pre=args.pre)
