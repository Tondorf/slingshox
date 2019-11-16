#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import asyncio


class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def start(self, loop):
        reader, writer = await asyncio.open_connection(self.host, self.port, loop=loop)

        running = True
        while running:
            data = await reader.readline()
            if data:
                print('Received:', data.decode().rstrip())
            else:
                running = False

        print('Close the socket')
        writer.close()


async def do_stuff(loop):
    while True:
        print('doing stuff...')
        await asyncio.sleep(2.5, loop=loop)


async def start(loop):
    client = TCPClient('127.0.0.1', 8888)
    tasks = [client.start(loop), do_stuff(loop)]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, loop=loop)

    for task in pending:
        task.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop))
    loop.close()
