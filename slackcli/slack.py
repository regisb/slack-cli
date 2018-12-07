import slacker

from . import errors
from . import token

__all__ = ['client', 'init', 'post_message']


class Slacker(object):
    INSTANCE = None

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
        raise errors.InvalidSlackToken(user_token)

    # Get team
    try:
        team = team or client().team.info().body["team"]["domain"]
    except slacker.Error as e:
        message = e.args[0]
        if e.args[0] == 'missing_scope':
            message = "Missing scope on token {}. This token requires the 'dnd:info' scope."
        raise errors.InvalidSlackToken(message)

    # Save token
    token.save(user_token, team)

def client():
    if Slacker.INSTANCE is None:
        # This is not supposed to happen
        raise ValueError("Slacker client token was not undefined")
    return Slacker.INSTANCE

def post_message(destination_id, text, pre=False, username=None):
    if pre:
        text = "```" + text + "```"
    text = text.strip()
    client().chat.post_message(
        destination_id, text,
        as_user=(not username),
        username=username,
    )
