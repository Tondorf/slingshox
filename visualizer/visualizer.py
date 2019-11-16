# -*- coding: utf-8 *-*

from cozypygame import *
from definitions import *
from entity import Thing


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
				self.vis_player(player, pID == self.world.pID)
			self.vis_footer()

		return self.surf

	def vis_earth(self, earth):
		pygame.draw.circle(self.surf, (0, 0, 100), (int(earth.x * XXX), int(earth.y * YYY)), int(earth.r*XXX))

	def vis_moon(self, moon):
		pygame.draw.circle(self.surf, (200, 200, 200), (int(moon.x * XXX), int(moon.y * YYY)), int(moon.r*XXX))

	def vis_player(self, player, me=False):
		color = (255, 255, 0) if me else (0, 255, 0)
		pygame.draw.circle(self.surf, color, (int(player.pos.x * XXX), int(player.pos.y * YYY)), 10)
		for (x, y) in player.tra:
			pygame.draw.circle(self.surf, color, (int(x * XXX), int(y * YYY)), 3)

	def vis_bomb(self, bomb):
		pygame.draw.circle(self.surf, (255, 0, 0), (int(bomb.pos.x * XXX), int(bomb.pos.y * YYY)), 10)

	def vis_footer(self):
		pygame.draw.line(self.surf, (255, 255, 255), (XXX, 0), (XXX, YYY), 1)
