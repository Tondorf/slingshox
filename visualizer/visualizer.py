# -*- coding: utf-8 *-*

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
				self.vis_player(player, pID == self.world.pID)
			self.vis_footer()

		return self.surf

	def vis_earth(self, earth):
		pygame.draw.circle(self.surf, (0, 0, 100), (int(earth.x * XXX), int(earth.y * YYY)), 2 * int(earth.r*XXX))
		# pygame.draw.lines(self.surf, (0, 0, 100), False, [(x*XXX, y*YYY) for (x, y) in earth.tra])

	def vis_moon(self, moon):
		pygame.draw.circle(self.surf, (200, 200, 200), (int(moon.x * XXX), int(moon.y * YYY)), 2 * int(moon.r*XXX))
		pygame.draw.lines(self.surf, (200, 200, 200), False, [(x*XXX, y*YYY) for (x, y) in moon.tra])
		# for (x, y) in moon.tra:
		# 	pygame.draw.circle(self.surf, (200, 200, 200), (int(x * XXX), int(y * YYY)), 1)

	def vis_player(self, player, me=False):
		color = (255, 255, 0) if me else (0, 255, 0)
		pygame.draw.circle(self.surf, color, (int(player.x * XXX), int(player.y * YYY)), player.r)
		pygame.draw.lines(self.surf, color, False, [(x*XXX, y*YYY) for (x, y) in player.tra])

	def vis_bomb(self, bomb):
		pygame.draw.circle(self.surf, (255, 0, 0), (int(bomb.x * XXX), int(bomb.y * YYY)), 10)

	def vis_footer(self):
		pygame.draw.line(self.surf, (255, 255, 255), (XXX, 0), (XXX, YYY), 1)
