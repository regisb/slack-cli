import json
import websocket

from . import names
from . import slack
from . import utils


def receive(sources, json_format):
    try:
        for message in loop(sources):
            if json_format:
                print(json.dumps(message))
            else:
                print(utils.format_message(message))
    except KeyboardInterrupt:
        pass


def loop(sources):
    url = slack.client().rtm.start().body["url"]
    connection = websocket.create_connection(url)
    while True:
        data = json.loads(connection.recv())
        if not data:
            # Sometimes, empty dictionaries are received
            continue
        if "team" not in data:
            # At the beginning, the connection replays some of the latest
            # messages, for an unknown reason. They can be filtered out by
            # checking for the "team" key.
            continue
        if data["type"] == "hello":
            continue
        if data["type"] == "message" and "subtype" not in message:
            source_name = names.sourcename(data["channel"])
            if source_name not in sources and "all" not in sources:
                # The streaming API provides all messages in all channels, so
                # we need to do some filtering here
                continue
            yield utils.decorate_message(data)
