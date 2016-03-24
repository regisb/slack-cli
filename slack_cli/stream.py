import json
import slacker
import websocket

from . import utils


def main():
    parser = utils.get_parser("Stream Slack messages in real time")
    parser.add_argument('sources', nargs='*',
                        help="Channel, group or user name from which to tail messages. E.g: 'general random john'")
    args = parser.parse_args()
    try:
        loop(args)
    except KeyboardInterrupt:
        pass

def loop(args):
    token = utils.get_token(args.token)
    source_ids = utils.get_source_ids(token, args.sources)
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
            if len(args.sources) != 1 and current_source_id != source_id:
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
