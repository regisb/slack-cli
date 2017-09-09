import os
import stat
import sys

import appdirs
import slacker


__all__ = ['client', 'init']

TOKEN_PATH = os.path.join(appdirs.user_config_dir("slack-cli"), "slack_token")

if sys.version[0] == '2':
    # pylint: disable=undefined-variable
    ask_user = raw_input
else:
    ask_user = input


class Slacker(object):
    INSTANCE = None

def init(token=None):
    token = get_token(token)

    # Save token
    if not os.path.exists(TOKEN_PATH):
        # Check token
        try:
            client().api.test()
        except slacker.Error:
            sys.stderr.write("Invalid Slack token: '{}'".format(token))
            sys.exit(1)

        # Write token file
        token_directory = os.path.dirname(TOKEN_PATH)
        if not os.path.exists(token_directory):
            os.makedirs(token_directory)
        with open(TOKEN_PATH, "w") as slack_token_file:
            slack_token_file.write(token)
        os.chmod(TOKEN_PATH, stat.S_IREAD | stat.S_IWRITE)

    # Initialize slacker client globally
    Slacker.INSTANCE = slacker.Slacker(token)

def get_token(token):
    # Read from command line argument
    token = token or os.environ.get('SLACK_TOKEN')

    # Read from environment variable
    if not token:
        token = os.environ.get('SLACK_TOKEN')

    # Read from local config file
    if not token:
        try:
            with open(TOKEN_PATH) as slack_token_file:
                token = slack_token_file.read().strip()
        except IOError:
            pass

    # Read from user input
    while not token:
        token = ask_user(
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


def client():
    if Slacker.INSTANCE is None:
        # This is not supposed to happen
        raise ValueError("Slacker client token was not undefined")
    return Slacker.INSTANCE

def post_message(destination_id, text, pre=False):
    if pre:
        text = "```" + text + "```"
    text = text.strip()
    client().chat.post_message(destination_id, text, as_user=True)
