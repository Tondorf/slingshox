#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from mode import Mode, Modes
from cozypygame import *
from definitions import *


class IntroMode(Mode):

	def __init__(self, world):
		super(IntroMode, self).__init__(world)

		print("Called INTRO MODE ctor")
		self.timeout = 7.5
		self.surf = pygame.Surface((XXX, dispYYY))
		self.font = pygame.font.SysFont("Consolas", 20)
		draw_text(self.surf, "Intro", self.font, (320,240), (255,0,0))

	def input(self, menu_events, game_events):
		self.timeout -= 1
		if self.timeout <= 0:
			self.world.init_mode(Modes.Ingame)

	def tick(self):
		pass

	def visualize(self):
		return self.surf
