# -*- coding: utf-8 *-*

import asyncio
import hashlib
import json
import time


class TCPServer:
    def __init__(self, host, port, fps):
        self.host = host
        self.port = port
        self.fps = fps
        self._loop = asyncio.get_event_loop()

    def start(self):
        coro = asyncio.start_server(self._handle_client, self.host, self.port)
        server = self._loop.run_until_complete(coro)

        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            server.close()
            self._loop.run_until_complete(server.wait_closed())
            self._loop.close()

    def _on_new_client(self, client_id):
        raise NotImplementedError('not implemented in abstract base class')

    def _on_leave_client(self, client_id):
        raise NotImplementedError('not implemented in abstract base class')

    def _on_client_message(self, message, client_id):
        raise NotImplementedError('not implemented in abstract base class')

    def _generate_broadcast_messages(self):
        raise NotImplementedError('not implemented in abstract base class')

    async def _handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        client_id = hashlib.md5(str(addr).encode()).hexdigest()
        self._on_new_client(client_id)
        writer.write((client_id + '\n').encode())
        await writer.drain()

        tasks = [self._consumer_handler(reader, client_id), self._producer_handler(writer)]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, loop=self._loop)

        self._on_leave_client(client_id)

        for task in pending:
            task.cancel()

        writer.close()

    async def _consumer_handler(self, reader, client_id):
        while True:
            data = await reader.readline()
            if data:
                msg = data.decode().rstrip()
                self._on_client_message(json.loads(msg), client_id)
            else:
                return

    async def _producer_handler(self, writer):
        while True:
            t1 = time.time()
            for msg in self._generate_broadcast_messages():
                writer.write((msg + '\n').encode())
                await writer.drain()

            t2 = time.time()
            dt = t2 - t1
            sleep_time = 1. / self.fps - dt
            await asyncio.sleep(max(sleep_time, 0.), loop=self._loop)
