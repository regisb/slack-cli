import json
import slacker
import websocket

from . import names
from . import utils


def receive(token, sources):
    try:
        loop(token, sources)
    except KeyboardInterrupt:
        pass

def loop(token, sources):
    connection = get_rtm_websocket(token)
    while True:
        data = json.loads(connection.recv())
        if not data:
            # Sometimes, empty dictionaries are received
            continue
        if data['type'] == 'hello':
            continue
        if data['type'] == 'message' and 'subtype' not in data:
            source_name = names.sourcename(token, data['channel'])
            if source_name not in sources:
                # The streaming API provides all messages in all channels, so
                # we need to do some filtering here
                continue
            print(utils.format_message(token, source_name, data))

def get_rtm_websocket(token):
    slacker_api = slacker.BaseAPI(token)
    url = slacker_api.get('rtm.start').body['url']
    return websocket.create_connection(url)
