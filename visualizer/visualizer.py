# -*- coding: utf-8 *-*

import statistics

import numpy as np

from cozypygame import *
from definitions import *
from entity import SpaceThing


class Visualizer:

	def __init__(self, world):
		print("Called INGAME CHALLENGE MODE ctor")
		self.world = world

		self.font = pygame.font.Font("fonts/ARCADE_N.TTF", 24)

		self.surf = pygame.Surface((dispXXX, dispYYY))

	def visualize(self):
		self.surf.fill((0, 0, 0))

		with self.world.world_objects_mutex:
			if self.world.earth is not None:
				self.vis_earth(self.world.earth)
			if self.world.moon is not None:
				self.vis_moon(self.world.moon)
			for pID, player in self.world.players.items():
				self.vis_player(player)
			self.vis_footer()
			self.world.last_update += 1

		return self.surf

	def vis_earth(self, earth):
		pygame.draw.circle(self.surf, earth.color, (int(earth.x * XXX), int(earth.y * YYY)), 2 * int(earth.r*XXX))
		# pygame.draw.lines(self.surf, earth.color, False, [(x*XXX, y*YYY) for (x, y) in earth.tra])

	def vis_moon(self, moon):
		print(self.world.last_update)
		if self.world.last_update == 0:
			pygame.draw.circle(self.surf, moon.color, (int(moon.x * XXX), int(moon.y * YYY)), 2 * int(moon.r*XXX))
		else:
			next = moon.tra[self.world.last_update - 1]

			inter = (statistics.mean(moon.x, next))
			pygame.draw.circle(self.surf, moon.color, (int(inter[0] * XXX), int(inter[1] * YYY)), 2 * int(moon.r*XXX))
		pygame.draw.lines(self.surf, moon.color, False, [(x*XXX, y*YYY) for (x, y) in moon.tra])

	def vis_player(self, player):
		pygame.draw.circle(self.surf, player.color, (int(player.x * XXX), int(player.y * YYY)), player.r)
		pygame.draw.lines(self.surf, player.color, False, [(x*XXX, y*YYY) for (x, y) in player.tra])

	def vis_bomb(self, bomb):
		pygame.draw.circle(self.surf, (255, 0, 0), (int(bomb.x * XXX), int(bomb.y * YYY)), 10)

	def vis_footer(self):
		pygame.draw.line(self.surf, (255, 255, 255), (XXX, 0), (XXX, YYY), 1)
