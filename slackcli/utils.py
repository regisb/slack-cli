from __future__ import unicode_literals
import argparse
from datetime import datetime

from . import names
from . import slack
from . import token



def get_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--token",
                        help="Explicitely specify Slack API token which will be saved to {}.".format(token.TOKEN_PATH))
    parser.add_argument("-T", "--team", help="""
        Team domain to interact with. This is the name that appears in the
        Slack url: https://xxx.slack.com. Use this option to interact with
        different teams. If unspecified, default to the team that was last used.
    """)
    return parser

def parse_args(parser):
    """
    Parse cli arguments and initialize slack client.
    """
    args = parser.parse_args()
    slack.init(user_token=args.token, team=args.team)
    return args


def is_destination_valid(channel=None, group=None, user=None):
    """
    Raise a ValueError if zero or more than one destinations are selected.
    """
    if channel is None and group is None and user is None:
        raise ValueError("You must define one of channel, group or user argument.")
    if len([a for a in (channel, group, user) if a is not None]) > 1:
        raise ValueError("You must define only one of channel, group or user argument.")

def get_source_id(source_name):
    sources = get_sources([source_name])
    if not sources:
        raise ValueError(u"Channel, group or user '{}' does not exist".format(source_name))
    return sources[0]["id"]

def get_source_ids(source_names):
    return {
        s['id']: s['name'] for s in get_sources(source_names)
    }

def get_sources(source_names):
    def filter_objects(objects):
        return [
            obj for obj in objects if len(source_names) == 0 or obj['name'] in source_names
        ]

    sources = []
    sources += filter_objects(slack.client().channels.list().body['channels'])
    sources += filter_objects(slack.client().groups.list().body['groups'])
    sources += filter_objects(slack.client().users.list().body['members'])
    return sources

def upload_file(path, destination_id):
    return slack.client().files.upload(path, channels=destination_id)


def search_messages(source_name, count=20):
    messages = []
    page = 1
    while len(messages) < count:
        response_body = slack.client().search.messages("in:{}".format(source_name), page=page, count=1000).body
        # Note that in the response, messages are sorted by *descending* date
        # (most recent first)
        messages = response_body["messages"]["matches"][::-1] + messages
        paging = response_body["messages"]["paging"]
        if paging["page"] == paging["pages"]:
            break
        page += 1

    # Print the last count messages
    for message in messages[-count:]:
        print(format_message(source_name, message))

def format_message(source_name, message):
    time = datetime.fromtimestamp(float(message['ts']))
    return "[@{} {}] {}: {}".format(
        source_name, time.strftime("%Y-%m-%d %H:%M:%S"),
        names.username(message['user']), message['text']
    )
