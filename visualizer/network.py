#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import json
import asyncio

PORT = 8888


class Client:
	def __init__(self, host='192.168.1.126'):
		self.host = host

		self.event_loop = asyncio.get_event_loop()
		self.event_loop.run_until_complete(self.handle())
		self.event_loop.close()

	async def handle(self):
		reader, writer = await asyncio.open_connection(self.host, PORT, loop=self.event_loop)

		running = True
		while running:
			data = await reader.readline()
			if data:
				print('Received:', data.decode().rstrip())
			else:
				running = False

		print('Close the socket')
		writer.close()

	def recv_world(self):
		wrld = self.sock.recv(1024)
		return json.loads(wrld)

	def send_cmds(self, cmds):
		dat = json.dumps({"cmds": cmds}).encode("ascii")
		self.sock.send(dat)
		print('cmds sent', dat)
