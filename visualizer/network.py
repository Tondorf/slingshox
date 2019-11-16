# -*- coding: utf-8 *-*

import asyncio
import json

PORT = 8888


class Client:
	def __init__(self, world, host='127.0.0.1'):
		self.world = world
		self.host = host

		self.event_loop = asyncio.get_event_loop()
		self.event_loop.run_until_complete(self.handle(self.event_loop))
		self.event_loop.close()

	async def handle(self, loop):
		self.reader, self.writer = await asyncio.open_connection(self.host, PORT, loop=loop)

		running = True
		while running:
			data = await self.reader.readline()
			if data:
				new_message = data.decode().rstrip()
				# print('Received:', new_message)
				self.world.incoming_message(new_message)
			else:
				running = False

		print('Close the socket')
		self.writer.close()

	async def send_cmds(self, cmds):
		dat = json.dumps({"cmds": cmds}).encode()
		#self.sock.send(dat)
		await self.writer.writelines(dat)
		print('cmds sent', dat)
