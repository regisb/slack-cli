from . import slack


__all__ = ['username', 'sourcename']


class Singleton(object):

    INSTANCE = None

    @classmethod
    def instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls()
        return cls.INSTANCE


class UserIndex(Singleton):
    """An index for storing user names without making too many calls to the
    API."""

    def __init__(self):
        self.user_index = {}
        self.bot_index = {}

    def username(self, user_id):
        if user_id not in self.user_index:
            self.user_index[user_id] = slack.client().users.info(user_id).body['user']['name']
        return self.user_index[user_id]
    
    def botname(self, bot_id):
        if bot_id not in self.bot_index:
            self.bot_index[bot_id] = slack.client().bots.info(bot_id).body['bot']['name']
        return self.bot_index[bot_id]


def username(user_id):
    """
    Find the user name associated to a user ID.
    """
    return UserIndex.instance().username(user_id)

def botname(user_id):
    """
    Find the bot name associated to a bot ID.
    """
    return UserIndex.instance().botname(user_id)

def get_username(slack_id, default=None):
    """
    Same as `username` but does not raise.
    """
    try:
        return username(slack_id)
    except slack.BaseError:
        return default

class SourceIndex(Singleton):
    """An index for storing channel/group names without making too many calls to the
    API.
    """

    def __init__(self):
        self.source_index = {}
        for im in slack.client().im.list().body['ims']:
            self.source_index[im['id']] = username(im['user'])

    def name(self, source_id):
        if source_id not in self.source_index:
            self.source_index[source_id] = slack.client().channels.info(source_id).body['channel']['name']
        return self.source_index[source_id]


def sourcename(user_id):
    """
    Find the source name associated to a source ID.
    """
    return SourceIndex.instance().name(user_id)
