import json

from tcpserver import TCPServer


class GameServer(TCPServer):
    def __init__(self, host, port):
        super(GameServer, self).__init__(host, port)
        self.players = []

    def _on_new_client(self, client_id):
        print(f'New client: {client_id}')
        self.players.append(client_id)

    def _on_client_message(self, message, client_id):
        print(f'Received from client {client_id}', message)

    def _generate_broadcast_messages(self):
        world = {
            'earth': {
                'x': .8,
                'y': .5,
                'r': .1,
            },
            'moon': {
                'x': .8,
                'y': .2,
                'r': .01,
            },
            self.players[0]: {
                'x': .5,
                'y': .5,
                'vx': .1,
                'vx': -.1,
                'phi': .3,
                'tx': [.55, .6, .65],
                'ty': [.45, .4, .35],
            }
        }
        return [json.dumps(world), ]
