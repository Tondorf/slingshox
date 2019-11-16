import json

import numpy as np

import physics
from tcpserver import TCPServer


class GameServer(TCPServer):
    def __init__(self, host, port):
        super(GameServer, self).__init__(host, port)
        self.players = []

        self.world = {
            'earth': {
                'x': .8,
                'y': .5,
                'vx': 0.,
                'vy': 0.,
                'm': 1.,
                'r': .1,
            },
            'moon': {
                'x': .8,
                'y': .2,
                'vx': .1,
                'vy': 0.,
                'm': .001,
                'r': .01,
            },
#            self.players[0]: {
#                'x': .5,
#                'y': .5,
#                'vx': .1,
#                'vy': -.1,
#                'phi': .3,
#                'tx': [.55, .6, .65],
#                'ty': [.45, .4, .35],
#            }
        }

    def _on_new_client(self, client_id):
        print(f'New client: {client_id}')
        self.players.append(client_id)

    def _on_client_message(self, message, client_id):
        print(f'Received from client {client_id}', message)

    def _update_world(self):
        planets = ['earth', 'moon']
        xs = [np.array([self.world[p]['x'], self.world[p]['y']]) for p in planets]
        vs = [np.array([self.world[p]['vx'], self.world[p]['vy']]) for p in planets]
        ms = [self.world[p]['m'] for p in ['earth', 'moon']]
        fs = None  # TODO save fs for next update
        dt = 1
        xs, ys, fs, ms, dt = physics.integrate(xs, vs, fs, ms, dt)

        for i, p in enumerate(planets):
            x, y = xs[i]
            self.world[p]['x'] = x
            self.world[p]['y'] = y

            vx, vy = vs[i]
            self.world[p]['vx'] = vx
            self.world[p]['vy'] = vy

    def _generate_broadcast_messages(self):
        self._update_world()
        return [json.dumps(self.world), ]
