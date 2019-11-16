import json

import numpy as np

import physics
from tcpserver import TCPServer


class GameServer(TCPServer):
    def __init__(self, host, port, fps):
        super(GameServer, self).__init__(host, port, fps)
        self._players = set()

        self._forces = None
        self._world = {
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
        }

    def _on_new_client(self, client_id):
        print(f'New client: {client_id}')
        self._players.add(client_id)

    def _on_leave_client(self, client_id):
        print(f'Client has left: {client_id}')
        self._players.add(client_id)

    def _on_client_message(self, message, client_id):
        print(f'Received from client {client_id}', message)
        self._players.remove(client_id)

    def _update_world(self):
        planets = ['earth', 'moon']
        xs = [np.array([self._world[p]['x'], self._world[p]['y']]) for p in planets]
        vs = [np.array([self._world[p]['vx'], self._world[p]['vy']]) for p in planets]
        ms = [self._world[p]['m'] for p in ['earth', 'moon']]
        dt = 1
        xs, ys, self._forces, ms, dt = physics.integrate(xs, vs, self._forces, ms, dt)

        for i, p in enumerate(planets):
            x, y = xs[i]
            self._world[p]['x'] = x
            self._world[p]['y'] = y

            vx, vy = vs[i]
            self._world[p]['vx'] = vx
            self._world[p]['vy'] = vy

    def _generate_broadcast_messages(self):
        self._update_world()
        return [json.dumps(self._world), ]
