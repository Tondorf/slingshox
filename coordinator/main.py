#!/usr/bin/env python3

from tcpserver import TCPServer

if __name__ == '__main__':
    server = TCPServer('127.0.0.1', 8888)
    server.start()
