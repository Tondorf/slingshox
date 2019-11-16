#!/usr/bin/env python3

from server import GameServer

if __name__ == '__main__':
    server = GameServer('127.0.0.1', 8888)
    fps = 1.
    server.start(fps)
