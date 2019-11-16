# -*- coding: utf-8 *-*

import asyncio
import json

PORT = 8888


class Client:
	def __init__(self, world, host='127.0.0.1'):
		self.world = world
		self.host = host

	async def start(self, loop):
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
		dat = (json.dumps(cmds) + '\n').encode()
		#print('sending cmds', dat)
		self.writer.write(dat)
