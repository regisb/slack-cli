#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Send a message to Slack from the CLI
"""

import slacker
import subprocess
import sys

from . import utils


def main():
    parser = utils.get_parser("Send messages to Slack from the CLI")
    parser.add_argument("-c", "--channel", help="Slack channel")
    parser.add_argument("-g", "--group", help="Slack group")
    parser.add_argument("-u", "--user", help="Slack user")
    parser.add_argument("-f", "--file", help="File to upload")
    parser.add_argument("--pre", action="store_true", help="Post as verbatim `message`")
    parser.add_argument("-m", "--message", help="Message to send. If unspecified, input will be read from stdin.")
    parser.add_argument("--run", action="store_true",
                        help="Run command before sending message. Used in conjunction with --message")
    args = parser.parse_args()

    token = utils.get_token(args.token)

    destination_id = utils.get_destination_id(args.channel, args.group, args.user)
    file_name = args.file

    if file_name:
        # Upload file
        slacker.Files(token).upload(file_name, channels=destination_id)
    else:
        pre = args.pre
        if args.message:
            if args.run:
                # Run command and post result
                command_result = subprocess.check_output(args.message, shell=True)
                message = "$ {}\n{}".format(args.message, command_result)
                pre = True
            else:
                # Just post the message
                message = args.message
        else:
            # Read message from stdin
            message = "".join([line for line in sys.stdin])
        message = format_message(message, pre=pre)
        slack_chat = SlackerChat(token)
        slack_chat.post_message(destination_id, message)


class SlackerChat(slacker.Chat):

    def post(self, api, **kwargs):
        params = kwargs.pop("params", {})
        if "as_user" not in params:
            params["as_user"] = "true"
        return super(SlackerChat, self).post(api, params=params, **kwargs)


def format_message(message, pre=False):
    if pre:
        return "```{}```".format(message)
    return message.strip()
