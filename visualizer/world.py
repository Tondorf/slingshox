#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from definitions import *

from mode import Modes
from intro import IntroMode
from ingame import IngameMode

enum2mode = {  # enum -> class object
	Modes.Intro: IntroMode,

	Modes.Ingame: IngameMode,
}


class World(object):
	"""well... just store everything in a giant world object"""

	def __init__(self, startmode):
		self.running = True

		self.mode = self.init_mode(startmode)

		self.reset_game_config()

	def reset_game_config(self):
		# config for the game mode
		self.gamemode = None  # SingleBattle, TeamBattle, RankingMode
		self.round = 1
		self.win_match = 2
		self.player1 = None
		self.player2 = None
		self.player3 = None
		self.player4 = None

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

	@property
	def players(self):
		return [self.player1, self.player2, self.player3, self.player4]
