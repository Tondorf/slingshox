#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import itertools

from mode import Mode
from cozypygame import *


class IngameMode(Mode):

	def __init__(self, world):
		super(IngameMode, self).__init__(world)

		self.smallResultFont = pygame.font.Font("fonts/ARCADE_N.TTF", 24)
		self.bigResultFont = pygame.font.Font("fonts/ARCADE_N.TTF", 80)
		print("Called INGAME CHALLENGE MODE ctor")

		self.surf = pygame.Surface((640,480))
		self.canvas = load_image_cached("image/background.png")
		self.world.colorsurf = pygame.Surface((640,448), flags=pygame.SRCALPHA)

		# joystick control memory. this doesn't really belong here, but whatevs
		self.joy_dir = 0

	def activate(self):  # called after fading in and finished
		pass

	def input(self, menu_events, game_events):
		pass

	def tick(self):
		pass

	def visualize(self):
		self.surf.blit(self.canvas, (0,0))
		self.surf.blit(self.world.colorsurf, (0,0))
		return self.surf
