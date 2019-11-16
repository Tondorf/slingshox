#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from mode import Mode
from cozypygame import *
from definitions import *


class GameMode(Mode):

	def __init__(self, world):
		super(GameMode, self).__init__(world)

		self.smallResultFont = pygame.font.Font("fonts/ARCADE_N.TTF", 24)
		self.bigResultFont = pygame.font.Font("fonts/ARCADE_N.TTF", 80)
		print("Called INGAME CHALLENGE MODE ctor")

		self.surf = pygame.Surface((XXX, dispYYY))
		self.canvas = load_image_cached("image/background.png")

		# joystick control memory. this doesn't really belong here, but whatevs
		self.joy_dir = 0

	def activate(self):  # called after fading in and finished
		pass

	def input(self, menu_events, game_events):
		pass

	def tick(self):
		pass

	def visualize(self):
		self.surf.fill((0, 0, 0))

		self.vis_ship(0.2, 0.2, True)
		self.vis_ship(0.4, 0.7)
		self.vis_ship(0.1, 0.9)
		self.vis_ship(0.99, 0.9)
		self.vis_ship(0.1, 0.99)
		self.vis_ship(0.99, 0.99)

		self.vis_footer()

		return self.surf

	def vis_ship(self, x, y, me=False):
		color = (255, 0, 0) if me else (0, 0, 255)
		pygame.draw.circle(self.surf, color, (int(x * XXX), int(y * YYY)), 10)

	def vis_footer(self):
		pygame.draw.line(self.surf, (255, 255, 255), (0, YYY), (XXX, YYY), 1)
