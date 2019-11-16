#!/usr/bin/env python3

from server import GameServer

if __name__ == '__main__':
    fps = 10.
    server = GameServer('127.0.0.1', 8888, fps=fps)
    server.start()
