from __future__ import unicode_literals
import argparse
from datetime import datetime
import os
import stat
import sys

import appdirs
import slacker


SLACK_TOKEN_PATH = os.path.join(appdirs.user_config_dir("slack-cli"), "slack_token")


def get_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--token",
                        help=("Slack token which will be saved to {}. This argument only needs to be" +
                              " specified once.").format(SLACK_TOKEN_PATH))
    return parser

def parse_args(parser):
    """
    Parse cli arguments; eventually save the token to disk.
    """
    args = parser.parse_args()
    token = _get_token(args.token)

    # Save token
    if not os.path.exists(SLACK_TOKEN_PATH):
        # Check token
        try:
            slacker.API(token).test()
        except slacker.Error:
            sys.stderr.write("Invalid Slack token: '{}'".format(token))
            sys.exit(1)

        # Write token file
        token_directory = os.path.dirname(SLACK_TOKEN_PATH)
        if not os.path.exists(token_directory):
            os.makedirs(token_directory)
        with open(SLACK_TOKEN_PATH, "w") as slack_token_file:
            slack_token_file.write(token)
        os.chmod(SLACK_TOKEN_PATH, stat.S_IREAD | stat.S_IWRITE)

    return args, token

def _get_token(token):
    # Read from command line argument
    token = token or os.environ.get('SLACK_TOKEN')

    # Read from environment variable
    if not token:
        token = os.environ.get('SLACK_TOKEN')

    # Read from local config file
    if not token:
        try:
            with open(SLACK_TOKEN_PATH) as slack_token_file:
                token = slack_token_file.read().strip()
        except IOError:
            pass

    # Read from user input
    while not token:
        token = input(
"""In order to interact with the Slack API, slack-cli requires a valid Slack API
token. To create and view your tokens, head over to:

    https://api.slack.com/custom-integrations/legacy-tokens

This message will only be printed once. After the first run, the Slack API
token will be stored in a local configuration file.
Slack API token: """
        )
        if token:
            token = token.strip()

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
    sources = get_sources(token, [source_name])
    if not sources:
        raise ValueError(u"Channel, group or user '{}' does not exist".format(source_name))
    return sources[0]["id"]

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

def upload_file(token, path, destination_id):
    return slacker.Files(token).upload(path, channels=destination_id)


def search_messages(token, source_name, count=20):
    search = slacker.Search(token)
    messages = []
    page = 1
    while len(messages) < count:
        response_body = search.messages("in:{}".format(source_name), page=page, count=1000).body
        # Note that in the response, messages are sorted by *descending* date
        # (most recent first)
        messages = response_body["messages"]["matches"][::-1] + messages
        paging = response_body["messages"]["paging"]
        if paging["page"] == paging["pages"]:
            break
        page += 1

    # Print the last count messages
    for message in messages[-count:]:
        print(format_message(token, source_name, message))

def format_message(token, source_name, message):
    time = datetime.fromtimestamp(float(message['ts']))
    return "[{} {}]{}: {}".format(
        source_name, time.strftime("%Y-%m-%d %H:%M:%S"),
        username(token, message['user']), message['text']
    )

class ChatAsUser(slacker.Chat):

    def post_formatted_message(self, destination_id, text, pre=False):
        if pre:
            text = "```" + text + "```"
        text = text.strip()
        self.post_message(destination_id, text, as_user=True)



class UserIndex:
    """A user index for storing user names without making too many calls to the
    API.
    """

    INSTANCE = None

    def __init__(self, token):
        self.slacker_users = slacker.Users(token)
        self.user_index = {}

    def name(self, user_id):
        if user_id not in self.user_index:
            self.user_index[user_id] = self.slacker_users.info(user_id).body['user']['name']
        return self.user_index[user_id]


def username(token, user_id):
    """
    Find the user name associated to a user ID.
    """
    if UserIndex.INSTANCE is None:
        UserIndex.INSTANCE = UserIndex(token)

    return UserIndex.INSTANCE.name(user_id)
