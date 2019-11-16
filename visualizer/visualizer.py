# -*- coding: utf-8 *-*

from cozypygame import *
from definitions import *


class Visualizer:

	def __init__(self, world):
		print("Called INGAME CHALLENGE MODE ctor")
		self.world = world

		self.font = pygame.font.Font("fonts/ARCADE_N.TTF", 24)

		self.surf = pygame.Surface((dispXXX, dispYYY))

	def visualize(self):
		self.surf.fill((0, 100, 0))

		if not self.world.got1stState:
			return self.surf

		self.vis_earth(self.world.earth)
		self.vis_moon(self.world.moon)
		for pID, player in self.world.players.items():
			self.vis_ship(player, pID == self.world.pID)
		# self.vis_ship(0.2, 0.2, True)
		# self.vis_ship(0.4, 0.7)
		# self.vis_ship(0.1, 0.9)
		self.vis_footer()

		return self.surf

	def vis_earth(self, earth):
		print("vis_earth")
		pygame.draw.circle(self.surf, (100, 100, 100), (int(earth.x * XXX), int(earth.y * YYY)), 200)

	def vis_moon(self, earth):
		pygame.draw.circle(self.surf, (200, 200, 200), (int(earth.x * XXX), int(earth.y * YYY)), 100)

	def vis_ship(self, ship, me=False):
		color = (255, 0, 0) if me else (0, 0, 255)
		pygame.draw.circle(self.surf, color, (int(ship.pos.x * XXX), int(ship.pos.y * YYY)), 10)

	def vis_footer(self):
		pygame.draw.line(self.surf, (255, 255, 255), (XXX, 0), (XXX, YYY), 1)
