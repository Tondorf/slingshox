#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from mode import Modes
from game import GameMode

enum2mode = {  # enum -> class object
	Modes.Game: GameMode,
}


class World(object):
	"""well... just store everything in a giant world object"""

	def __init__(self, startmode):
		self.running = True
		self.mode = self.init_mode(startmode)

	def init_mode(self, new_mode):
		self.mode = object.__new__(enum2mode[new_mode])
		self.mode.__init__(self)
		return self.mode

	def input(self, menu_events, game_events):
		self.mode.input(menu_events, game_events)

	def tick(self):
		self.mode.tick()

	def visualize(self):
		return self.mode.visualize()
