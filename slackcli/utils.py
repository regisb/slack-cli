from __future__ import unicode_literals
import argparse
from datetime import datetime

from . import errors
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

def get_destination_id(name):
    # We should probably switch to the conversations.list method once Slacker
    # supports it:
    # https://api.slack.com/methods/conversations.list
    # https://github.com/os/slacker/issues/116
    fetchers = [
        lambda: slack.client().channels.list().body['channels'],
        lambda: slack.client().groups.list().body['groups'],
        lambda: slack.client().users.list().body['members'],
    ]
    for fetcher in fetchers:
        for resource in fetcher():
            if resource['name'] == name:
                return resource['id']

    raise errors.SourceDoesNotExistError(name)


def upload_file(path, destination_id):
    return slack.client().files.upload(path, channels=destination_id)


def search_messages(source_name, count=20):
    messages = []
    page = 1
    while len(messages) < count:
        response_body = slack.client().search.messages("in:{}".format(source_name), page=page, count=min(count, 1000)).body
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
    # Some bots do not have a 'user' entry, but only a 'username'.
    # However, we prefer to rely on the 'username' entry if it is present, for
    # performance reasons.
    username = message.get('username') or names.username(message['user'])
    return "[@{} {}] {}: {}".format(
        source_name, time.strftime("%Y-%m-%d %H:%M:%S"),
        username, message['text']
    )
