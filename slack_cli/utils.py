import argparse
import os

def get_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--token",
                        help=("Slack token. This argument is unnecessary if you"
                        "have defined the SLACK_TOKEN variable."))
    return parser

def get_token(token=None):
    token = token or os.environ.get('SLACK_TOKEN')
    if not token:
        raise ValueError("Empty slack token value.")
    return token

def get_destination_id(channel=None, group=None, user=None):
    is_destination_valid(channel, group, user)
    if channel:
        return "#" + channel
    if group:
        return group
    if user:
        return "@" + user#unsupported for now

def is_destination_valid(channel=None, group=None, user=None):
    """
    Raise a ValueError if zero or more than one destinations are selected.
    """
    if channel is None and group is None and user is None:
        raise ValueError("You must define one of channel, group or user argument.")
    if len([a for a in (channel, group, user) if a is not None]) > 1:
        raise ValueError("You must define only one of channel, group or user argument.")

