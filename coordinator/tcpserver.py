import asyncio
import hashlib
import time


class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._loop = asyncio.get_event_loop()
        self._stopping = False

    def start(self, fps):
        self.fps = fps

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

        tasks = [self._consumer_handler(reader), self._producer_handler(writer)]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, loop=self._loop)

        self._stopping = True
        for task in pending:
            task.cancel()

        writer.close()

    async def _consumer_handler(self, reader):
        while not self._stopping:
            data = await reader.readline()
            if data:
                msg = data.decode().rstrip()
                self._on_client_message(msg)
            else:
                return

    async def _producer_handler(self, writer):
        while not self._stopping:
            t1 = time.time()
            for msg in self._generate_broadcast_messages():
                writer.write((msg + '\n').encode())
                await writer.drain()

            t2 = time.time()
            dt = t2 - t1
            sleep_time = 1. / self.fps - dt
            await asyncio.sleep(max(sleep_time, 0.))
