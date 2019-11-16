#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import asyncio


async def handle(loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    running = True
    while running:
        data = await reader.readline()
        if data:
            print('Received:', data.decode().rstrip())
        else:
            running = False

    print('Close the socket')
    writer.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle(loop))
    loop.close()
