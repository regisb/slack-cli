import argparse
import os

import slacker


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

def is_destination_valid(channel=None, group=None, user=None):
    """
    Raise a ValueError if zero or more than one destinations are selected.
    """
    if channel is None and group is None and user is None:
        raise ValueError("You must define one of channel, group or user argument.")
    if len([a for a in (channel, group, user) if a is not None]) > 1:
        raise ValueError("You must define only one of channel, group or user argument.")

def get_source_id(token, source_name):
    destination = get_sources(token, [source_name])
    if not destination:
        raise ValueError(u"Channel, group or user '{}' does not exist".format(source_name))
    return destination[0]["id"]

def get_source_ids(token, source_names):
    return {
        s['id']: s['name'] for s in get_sources(token, source_names)
    }

def get_sources(token, source_names):
    def filter_objects(objects):
        return [
            obj for obj in objects if len(source_names) == 0 or obj['name'] in source_names
        ]

    sources = []
    sources += filter_objects(slacker.Channels(token).list().body['channels'])
    sources += filter_objects(slacker.Groups(token).list().body['groups'])
    sources += filter_objects(slacker.Users(token).list().body['members'])
    return sources


class ChatAsUser(slacker.Chat):

    def post_formatted_message(self, destination_id, text, pre=False):
        if pre:
            text = "```" + text + "```"
        text = text.strip()
        self.post_message(destination_id, text, as_user=True)
