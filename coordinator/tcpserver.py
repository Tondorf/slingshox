import asyncio
import hashlib


class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._loop = asyncio.get_event_loop()
        self._stopping = False

    def start(self):
        coro = asyncio.start_server(self._handle_client, self.host, self.port)
        server = self._loop.run_until_complete(coro)

        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            server.close()
            self._loop.run_until_complete(server.wait_closed())
            self._loop.close()

    async def _handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        client_id = hashlib.md5(str(addr).encode()).hexdigest()
        print('New client:', client_id)
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
                print('recv:', msg)
            else:
                return

    async def _producer_handler(self, writer):
        while not self._stopping:
            message = 'foobar\n'.encode()
            print(f'Send: {message}')
            writer.write(message)
            await writer.drain()
            await asyncio.sleep(1.)
