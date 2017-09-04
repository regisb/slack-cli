import json
import slacker
import websocket

from . import utils


def receive(token, sources):
    try:
        loop(token, sources)
    except KeyboardInterrupt:
        pass

def loop(token, sources):
    source_ids = utils.get_source_ids(token, sources)
    print(source_ids)
    connection = get_rtm_websocket(token)
    while True:
        data = json.loads(connection.recv())
        print(data)
        if data['type'] == 'hello':
            continue
        if data['type'] == 'message' and 'subtype' not in data:
            source_id = data.get('channel') or data.get('group') or data.get('user')
            if source_id not in source_ids:
                # TODO we have a problem identifying the channel here
                continue
            print(utils.format_message(token, source_ids[source_id], data))

def get_rtm_websocket(token):
    slacker_api = slacker.BaseAPI(token)
    url = slacker_api.get('rtm.start').body['url']
    return websocket.create_connection(url)
