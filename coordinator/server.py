#!/usr/bin/env python3

import asyncio
import time
import hashlib


async def consumer_handler(reader, client_id):
    while True:
        try:
            data = await reader.readline()
            msg = data.decode()
        except ConnectionResetError:
            return


async def producer_handler(writer):
    while True:
        try:
            t1 = time.time()
            writer.write(b'foo\n')
            await writer.drain()
            t2 = time.time()
            dt = t2 - t1
            await asyncio.sleep(max(.1 - dt, 0.))
        except ConnectionResetError:
            return


async def handle(reader, writer):
    addr = writer.get_extra_info('peername')
    client_id = hashlib.md5(str(addr).encode()).digest()
    writer.write(client_id)

    consumer_task = asyncio.ensure_future(consumer_handler(reader, client_id))
    producer_task = asyncio.ensure_future(producer_handler(writer))
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    writer.close()


async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
