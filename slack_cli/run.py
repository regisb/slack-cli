#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Send the result of a command to Slack from the CLI
"""

import subprocess

from . import utils


def main():
    parser = utils.get_parser("Send the result of a command to Slack")
    parser.add_argument("command", help="Command to run")
    parser.add_argument("destination", help="Slack channel, group or username")
    args = parser.parse_args()

    token = utils.get_token(args.token)
    destination_id = utils.get_source_id(token, args.destination)

    command_result = subprocess.check_output(args.command, shell=True)
    #import ipdb; ipdb.set_trace()
    message = "$ " + args.command + "\n" + command_result.decode("utf-8")
    utils.ChatAsUser(token).post_formatted_message(destination_id, message, pre=True)
