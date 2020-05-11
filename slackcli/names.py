from . import slack


__all__ = ["username", "sourcename"]


class Singleton:

    INSTANCE = None

    @classmethod
    def instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls()
        return cls.INSTANCE


class UserIndex(Singleton):
    """An index for storing user names without making too many calls to the API."""

    def __init__(self):
        # user id -> user name
        self.user_id_index = {}
        # user name -> user id
        self.user_name_index = {}
        self.bot_index = {}

    def username(self, user_id):
        if user_id not in self.user_id_index:
            self.user_id_index[user_id] = (
                slack.client().users.info(user_id).body["user"]["name"]
            )
        return self.user_id_index[user_id]

    def user_id(self, slack_name):
        """
        Fetch the user ID from the user name. Note that this is really slow, as we need
        to parse the entire list of user IDs. Unfortunately it is not possible to fetch
        a user by its username. Ideally, we should cache this list.
        """
        if not self.user_name_index:
            members = slack.client().users.list().body["members"]
            for member in members:
                self.user_name_index[member["name"]] = member["id"]
        return self.user_name_index[slack_name.lower()]

    def botname(self, bot_id):
        if bot_id not in self.bot_index:
            self.bot_index[bot_id] = (
                slack.client().bots.info(bot_id).body["bot"]["name"]
            )
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


def get_user_id(slack_name, default=None):
    """
    Find the user id associated to a username.
    """
    try:
        return UserIndex.instance().user_id(slack_name)
    except KeyError:
        return default


class SourceIndex(Singleton):
    """
    An index for storing channel/group names without making too many calls to
    the API.
    """

    def __init__(self):
        self.source_index = {}
        # TODO much of the time lost at boot comes from this loop. This could
        # maybe be run later? If we had the conversations API we could retrieve
        # user names at run time.
        for im in slack.client().im.list().body["ims"]:
            self.source_index[im["id"]] = username(im["user"])

    def name(self, source_id):
        if source_id not in self.source_index:
            self.source_index[source_id] = self._get_source_name(source_id)
        return self.source_index[source_id]

    @staticmethod
    def _get_source_name(source_id):
        if source_id.startswith("G"):
            # We need to process groups and channels differently until slacker
            # implements the `conversations` API.
            # https://api.slack.com/methods/conversations.info
            return slack.client().groups.info(source_id).body["group"]["name"]
        return slack.client().channels.info(source_id).body["channel"]["name"]


def sourcename(source_id):
    """
    Find the source name associated to a source ID.
    """
    return SourceIndex.instance().name(source_id)
