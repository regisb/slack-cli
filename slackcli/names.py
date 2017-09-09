import slacker

__all__ = ['username', 'sourcename']

class Singleton(object):

    INSTANCE = None

    @classmethod
    def instance(cls, token):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls(token)
        return cls.INSTANCE


class UserIndex(Singleton):
    """An index for storing user names without making too many calls to the
    API."""

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
    return UserIndex.instance(token).name(user_id)


class SourceIndex(Singleton):
    """An index for storing channel/group names without making too many calls to the
    API.
    """

    def __init__(self, token):
        self.slacker = slacker.Slacker(token)
        self.source_index = {}
        for im in self.slacker.im.list().body['ims']:
            self.source_index[im['id']] = username(token, im['user'])

    def name(self, source_id):
        if source_id not in self.source_index:
            self.source_index[source_id] = self.slacker.channels.info(source_id).body['channel']['name']
        return self.source_index[source_id]


def sourcename(token, user_id):
    """
    Find the source name associated to a source ID.
    """
    return SourceIndex.instance(token).name(user_id)
