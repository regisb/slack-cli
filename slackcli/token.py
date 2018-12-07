import json
import os
import stat
import sys

import appdirs

if sys.version[0] == '2':
    # pylint: disable=undefined-variable
    ask_user = raw_input
else:
    ask_user = input

TOKEN_PATH = os.path.join(appdirs.user_config_dir("slack-cli"), "slack_token")
TEAMS_PATH = os.path.join(appdirs.user_config_dir("slack-cli"), "teams.json")


def load(team=None):
    # Read from environment variable
    token = os.environ.get('SLACK_TOKEN')
    if token:
        return token

    # Read from local config file
    if team:
        try:
            with open(TEAMS_PATH) as teams_file:
                teams = json.load(teams_file)
            if team in teams:
                return teams[team]["token"]
        except IOError:
            pass
    else:
        try:
            with open(TOKEN_PATH) as slack_token_file:
                return slack_token_file.read().strip()
        except IOError:
            pass

def ask(team=None):
    token = None
    while not token:
        message = """In order to interact with the Slack API, slack-cli requires a valid Slack API
token. To create and view your tokens, head over to:

    https://api.slack.com/custom-integrations/legacy-tokens

This message will only appear once. After the first run, the Slack API token
will be stored in a local configuration file.

Your Slack API token{}: """.format(
            " for the " + team + " team" if team else ""
        )
        token = ask_user(message).strip()
    return token

def save(token, team):
    # Create directory
    token_directory = os.path.dirname(TOKEN_PATH)
    if not os.path.exists(token_directory):
        os.makedirs(token_directory)

    # Save default token
    with open(TOKEN_PATH, "w") as slack_token_file:
        slack_token_file.write(token)
    os.chmod(TOKEN_PATH, stat.S_IREAD | stat.S_IWRITE)

    # Save team token
    teams = {}
    if os.path.exists(TEAMS_PATH):
        with open(TEAMS_PATH) as teams_file:
            teams = json.load(teams_file)
    teams[team] = {"token": token}
    with open(TEAMS_PATH, 'w') as teams_file:
        json.dump(teams, teams_file, sort_keys=True, indent=4)
    os.chmod(TEAMS_PATH, stat.S_IREAD | stat.S_IWRITE)
