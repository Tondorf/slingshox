# -*- coding: utf-8 *-*

import json

import pygame

from visualizer import Visualizer
from definitions import *
from network import Client


class Thing(pygame.math.Vector2):

	def __init__(self, x, y, r):
		super().__init__(x, y)
		self.r = r

	def __repr__(self):
		return "Thing<%d,%d,r=%d>" % (self.x, self.y, self.r)


class Player(Thing):
	def __init__(self, pos, velocity, phi, trajectories):
		super().__init__(pos.x, pos.y, 10)
		self.vel = velocity
		self.phi = phi
		self.tra = trajectories

	def __repr__(self):
		return "Player<%s,%s,phi=%d,tra_count=%d>" % (super().__repr__(), self.vel, self.phi, len(self.tra))


class World(object):
	"""well... just store everything in a giant world object"""

	def __init__(self):
		self.running = True
		self.visualizer = Visualizer(self)

		self.earth = None
		self.moon = None
		self.players = {}

		self.inited = False
		self.pID = None
		self.got1stState = False

		self.network = Client(self)

	def input(self, _menu_events, game_events):
		# EvAct = enum('Up', 'Down', 'Left', 'Right', 'Submit', 'Exit', 'Pause')
		# -1 = left, 0 = nothing, +1 = right
		events = [g.dir for g in game_events]
		direction = int(EvAct.Right in events) - int(EvAct.Left in events)
		thrust = int(EvAct.Submit in events)
		cmds = {'direction': direction, 'thrust': thrust}
		##print("CMDS:", cmds)
		#self.network.send_cmds(cmds)
		### TODO

	def tick(self):
		pass

	def visualize(self):
		return self.visualizer.visualize()

	async def incoming_message(self, new_msg):
		if not self.inited:
			self.pID = new_msg
			self.inited = True
		else:
			await self.parse_new_world(new_msg)

	async def parse_new_world(self, new_world):
		new_world = json.loads(new_world)
		#print("NEW WORLD:", new_world, type(new_world))
		# Received: {"earth": {"x": 0.8, "y": 0.5, "r": 0.1}, "moon": {"x": 0.8, "y": 0.2, "r": 0.01}, "4ddad0457b7f419efb1c637937cbbeb3": {"x": 0.5, "y": 0.5, "vx": -0.1, "phi": 0.3, "tx": [0.55, 0.6, 0.65], "ty": [0.45, 0.4, 0.35]}}
		self.earth = self.decodeXYR(new_world.pop("earth"))
		self.moon = self.decodeXYR(new_world.pop("moon"))
		self.players.clear()
		for pID, pObj in new_world.items():
			self.players[pID] = self.decodePlayer(pObj)
		self.got1stState = True
		print(self.earth, self.moon, self.players)

	@staticmethod
	def decodeXYR(obj):
		return Thing(obj['x'], obj['y'], obj['r'])

	@staticmethod
	def decodePlayer(obj):
		pos = pygame.math.Vector2(obj['x'], obj['y'])
		velocity = pygame.math.Vector2(obj['vx'], obj['vy'])
		phi = obj['phi']
		trajectories = list(zip(obj['tx'], obj['ty']))
		return Player(pos, velocity, phi, trajectories)
