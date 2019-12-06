import json
import re
import sys

import slacker

from . import errors
from . import token
from . import utils

__all__ = ["client", "init", "post_message"]


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
                "Missing scope on token {}. This token requires the 'dnd:info' scope."
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


def post_message(destination_id, text, pre=False, username=None):
    if pre:
        text = "```" + text + "```"
    else:
        status_update_fields = parse_status_update(text)
        if status_update_fields:
            update_status_fields(**status_update_fields)
            return
    text = utils.format_outgoing_message(text)
    client().chat.post_message(
        destination_id, text, as_user=(not username), username=username,
    )


def parse_status_update(text):
    """
    Parse "/status :emoji: sometext" messages. If there is a match, return a dict
    containing the profile attributes to be updated. Else return None.
    """
    status_update_match = re.match(
        r"^/status( +(?P<status_emoji>:[^ :]+:))?( +(?P<status_text>[^:].*))?$", text
    )
    if status_update_match is None:
        return None
    status = status_update_match.groupdict()
    if status["status_emoji"] is None:
        if status["status_text"] is None:
            return None
        if status["status_text"] == "clear":
            status["status_text"] = ""
        else:
            status["status_emoji"] = ":speech_balloon:"
    return status


def update_status_fields(**profile):
    client().users.profile.set(profile=json.dumps(profile))
