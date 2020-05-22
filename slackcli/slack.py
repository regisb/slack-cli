import json
import re
import sys

import slacker

from . import errors
from . import token
from . import messaging

__all__ = ["client", "init"]


BaseError = slacker.Error


class Slacker(slacker.Slacker):
    INSTANCE = None

    @classmethod
    def create_instance(cls, user_token):
        cls.INSTANCE = cls(user_token)

    @classmethod
    def instance(cls):
        if cls.INSTANCE is None:
            # This is not supposed to happen
            raise ValueError("Slacker client token was not undefined")
        return cls.INSTANCE


def init(user_token=None, team=None):
    """
    This function must be called prior to any use of the Slack API.
    """
    user_token = user_token
    loaded_token = token.load(team=team)
    must_save_token = False
    if user_token:
        if user_token != loaded_token:
            must_save_token = True
    else:
        user_token = loaded_token
        if not user_token:
            user_token = token.ask(team=team)
            must_save_token = True

    # Initialize slacker client globally
    Slacker.INSTANCE = slacker.Slacker(user_token)
    if must_save_token:
        save_token(user_token, team=team)


def save_token(user_token, team=None):
    # Always test token before saving
    try:
        client().api.test()
    except slacker.Error:
        raise errors.SlackCliError("Invalid Slack token: '{}'".format(user_token))

    # Get team
    try:
        team = team or client().team.info().body["team"]["domain"]
    except slacker.Error as e:
        message = e.args[0]
        if e.args[0] == "missing_scope":
            message = (
                "Missing scope on token {}. This token requires the 'team:read' scope."
            ).format(user_token)
        raise errors.SlackCliError(message)

    # Save token
    try:
        token.save(user_token, team)
    except errors.ConfigSaveError as e:
        sys.stderr.write("❌ ")
        sys.stderr.write(e.args[0])
        sys.stderr.write("\n")
        sys.stderr.write(
            "⚠️ Could not save token to disk. You will have to configure the Slack"
            " token again next time you run slack-cli.\n"
        )


def client():
    return Slacker.instance()


def update_status_fields(**profile):
    client().users.profile.set(profile=json.dumps(profile))
