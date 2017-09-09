import sys

import slacker

from . import token

__all__ = ['client', 'init', 'post_message']


class Slacker(object):
    INSTANCE = None

def init(user_token=None, team=None):
    """
    This function must be called prior to any use of the Slack API.
    """
    user_token = user_token or token.load(team=team)

    # Always test token
    try:
        slacker.Slacker(user_token).api.test()
    except slacker.Error:
        sys.stderr.write("Invalid Slack token: '{}'".format(user_token))
        sys.exit(1)

    # Initialize slacker client globally
    Slacker.INSTANCE = slacker.Slacker(user_token)

    # Save token
    team = team or client().team.info().body["team"]["domain"]
    token.save(user_token, team)

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
