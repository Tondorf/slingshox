#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import json
import socket

PORT = 4711


class Client:
	def __init__(self, HOST='192.168.1.102'):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self) -> int:
		self.sock.connect((HOST, PORT))
		sid = self.sock.recv(1024)
		print('Received', repr(sid))
		try:
			return int(sid)
		except ValueError as ve:
			# raise ve
			return -1

	def recv_world(self):
		wrld = self.sock.recv(1024)
		return json.loads(wrld)

	def send_cmds(self, cmds):
		dat = json.dumps({"cmds": cmds}).encode("ascii")
		self.sock.send(dat)
		print('cmds sent', dat)
