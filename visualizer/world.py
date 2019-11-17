# -*- coding: utf-8 *-*

import json
import threading

from definitions import *
from entity import SpaceThing, Player
from visualizer import Visualizer


class World(object):
	"""well... just store everything in a giant world object"""

	def __init__(self):
		self.running = True
		self.visualizer = Visualizer(self)

		self.world_objects_mutex = threading.RLock()
		self.earth = None
		self.moon = None
		self.players = {}
		self.bombs = []

		self.cmds_mutex = threading.RLock()
		self.cmds = {}

		self.inited = False
		self.pID = None

	def input(self, _menu_events, game_events):
		# EvAct = enum('Up', 'Down', 'Left', 'Right', 'Submit', 'Exit', 'Pause')
		# -1 = left, 0 = nothing, +1 = right
		events = [g.dir for g in game_events]
		direction = int(EvAct.Right in events) - int(EvAct.Left in events)
		thrust = int(EvAct.Submit in events)
		with self.cmds_mutex:
			self.cmds = {'direction': direction, 'thrust': thrust}

	def tick(self):
		pass

	def visualize(self):
		return self.visualizer.visualize()

	def incoming_message(self, new_msg):
		if not self.inited:
			self.pID = new_msg
			self.inited = True
		else:
			self.parse_new_world(new_msg)

	def parse_new_world(self, new_world):
		new_world = json.loads(new_world)
		#print(new_world)
		with self.world_objects_mutex:
			self.earth = SpaceThing(new_world.pop("earth"))
			self.moon = SpaceThing(new_world.pop("moon"))
			# self.bombs = SpaceThing(new_world.pop("bombs"))  # TODO
			self.players.clear()
			for pID, pObj in new_world.items():
				self.players[pID] = Player(pObj)

	# print(self.earth, self.moon, self.players)
