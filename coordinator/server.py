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
                'x': .0,
                'y': 0.,
                'vx': 0.,
                'vy': 0.,
                'm': 1.,
                'r': 1.,
            },
            'moon': {
                'x': .0,
                'y': 60.,
                'vx': .2,
                'vy': 0.,
                'm': .001,
                'r': .273,
            },
        }

    def _on_new_client(self, client_id):
        self._players.add(client_id)
        self._world[client_id] = {
            'x': 50,
            'y': 50.,
            'vx': -.2,
            'vy': 0.,
            'm': 0.,
            'phi': 0.,
        }

    def _on_leave_client(self, client_id):
        print(f'Client has left: {client_id}')
        self._players.remove(client_id)
        self._world.pop(client_id)

    def _on_client_message(self, message, client_id):
        dphi = message['direction'] * -.1
        self._world[client_id]['phi'] += dphi

        R = np.array([[np.cos(dphi), np.sin(dphi)], [-np.sin(dphi), np.cos(dphi)]])
        v = R @ np.array([self._world[client_id][i] for i in ['vx', 'vy']])
        v += message['thrust'] * .1

        self._world[client_id]['vx'] = v[0]
        self._world[client_id]['vy'] = v[1]

    def _update_world(self):
        xs = [np.array([self._world[p]['x'], self._world[p]['y']]) for p in self._world]
        vs = [np.array([self._world[p]['vx'], self._world[p]['vy']]) for p in self._world]
        ms = [self._world[p]['m'] for p in self._world]
        dt = .01

        for _ in range(100):
            xs, vs, self._forces, _, _ = physics.integrate(xs, vs, self._forces, ms, dt)

        for i, p in enumerate(self._world):
            x, y = xs[i]
            self._world[p]['x'] = x
            self._world[p]['y'] = y

            vx, vy = vs[i]
            self._world[p]['vx'] = vx
            self._world[p]['vy'] = vy

        fs = self._forces
        txs = []
        for _ in range(100):
            xs, vs, fs, _, _ = physics.integrate(xs, vs, fs, ms, dt)
        txs.append(xs)

        for i in range(500):
            xs, vs, fs, _, _ = physics.integrate(xs, vs, fs, ms, 100 * dt)
            txs.append(xs)

        for i, p in enumerate(self._world):
            self._world[p]['tx'] = np.array([t[i][0] for t in txs])
            self._world[p]['ty'] = np.array([t[i][1] for t in txs])

    def _generate_broadcast_messages(self):
        self._update_world()
        serialized_world = {
            p: {
                'x': self._world[p]['x'] / 100. + .5,
                'y': self._world[p]['y'] / 100. + .2,
                'vx': self._world[p]['vx'] / 100.,
                'vy': self._world[p]['vy'] / 100.,
                'tx': (self._world[p]['tx'] / 100. + .5).tolist(),
                'ty': (self._world[p]['ty'] / 100. + .2).tolist(),
            } for p in self._world
        }

        for p in self._world:
            if 'r' in self._world[p]:
                serialized_world[p]['r'] = self._world[p]['r'] / 100
            if 'phi' in self._world[p]:
                serialized_world[p]['phi'] = self._world[p]['phi']

        return [json.dumps(serialized_world), ]
