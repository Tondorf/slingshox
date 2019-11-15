#!/usr/bin/env python3

import asyncio


async def handle_client(reader, writer):
    client_alive = True
    while client_alive:
        data = await reader.read(100)
        message = data.decode()
        if message:
            addr = writer.get_extra_info('peername')

            print(f'Received {message!r} from {addr!r}')

            print(f'Send: {message!r}')
            writer.write(data)
            await writer.drain()
        else:
            client_alive = False

    print('Close the connection')
    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
