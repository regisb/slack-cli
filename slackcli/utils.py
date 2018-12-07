from __future__ import unicode_literals
from datetime import datetime

from . import errors
from . import names
from . import slack


def get_destination_id(name):
    return get_resource(name)[1]['id']

def get_resource(name):
    # We should probably switch to the conversations.list method once Slacker
    # supports it:
    # https://api.slack.com/methods/conversations.list
    # https://github.com/os/slacker/issues/116
    fetchers = [
        ('channel', lambda: slack.client().channels.list().body['channels']),
        ('group', lambda: slack.client().groups.list().body['groups']),
        ('user', lambda: slack.client().users.list().body['members']),
    ]
    for resource_type, fetcher in fetchers:
        for resource in fetcher():
            if resource['name'] == name:
                return resource_type, resource
    raise errors.SourceDoesNotExistError(name)


def upload_file(path, destination_id):
    return slack.client().files.upload(path, channels=destination_id)


def search_messages(source_name, count=20):
    resource_type, resource = get_resource(source_name)
    # channel->channels, group->groups, but im->im :-(
    method_name = resource_type + 's'
    if resource_type == 'user':
        # In case of conversation with a user, we need to find the corresponding IM object
        resource = [i for i in slack.client().im.list().body['ims'] if i['user'] == resource['id']][0]
        method_name = 'im'

    history = getattr(slack.client(), method_name).history

    messages = []
    latest = None
    while len(messages) < count:
        response_body = history(resource['id'], count=min(count - len(messages), 1000), latest=latest, inclusive=False).body
        # Note that in the response, messages are sorted by *descending* date
        # (most recent first)
        messages += response_body["messages"]
        if not response_body["has_more"]:
            break
        latest = messages[-1]['ts']

    # Print the last count messages, from last to first
    for message in messages[::-1]:
        print(format_message(source_name, message))

def format_message(source_name, message):
    time = datetime.fromtimestamp(float(message['ts']))
    # Some bots do not have a 'user' entry, but only a 'username'.
    # However, we prefer to rely on the 'username' entry if it is present, for
    # performance reasons.
    username = message.get('username') or names.username(message['user'])
    formatted = "[@{} {}] {}: {}".format(
        source_name, time.strftime("%Y-%m-%d %H:%M:%S"),
        username, message['text']
    )
    for f in message.get('files', []):
        formatted += "\n    {}: {}".format(f['name'], f['url_private'])
    return formatted
