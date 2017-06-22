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
    connection = get_rtm_websocket(token)
    current_source_id = None
    while True:
        data = json.loads(connection.recv())
        if data['type'] == 'hello':
            continue
        if data['type'] == 'message' and 'subtype' not in data:
            source_id = data.get('channel') or data.get('group') or data.get('user')
            if source_id not in source_ids:
                continue
            if len(sources) != 1 and current_source_id != source_id:
                if current_source_id is not None:
                    print("")
                print("==> {} <==".format(source_ids[source_id]))
                current_source_id = source_id
            username = slacker.Users(token).info(data['user']).body['user']['name']
            print(u"{}: {}".format(username, data['text']))

def get_rtm_websocket(token):
    slacker_api = slacker.BaseAPI(token)
    url = slacker_api.get('rtm.start').body['url']
    return websocket.create_connection(url)
