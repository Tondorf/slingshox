#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from mode import Mode
from cozypygame import *
from definitions import *
from network import Client


class GameMode(Mode):

	def __init__(self, world):
		print("Called INGAME CHALLENGE MODE ctor")
		super(GameMode, self).__init__(world)

		self.font = pygame.font.Font("fonts/ARCADE_N.TTF", 24)

		self.surf = pygame.Surface((dispXXX, dispYYY))

		self.network = Client()

	def activate(self):  # called after fading in and finished
		self.network.connect()

	def input(self, menu_events, game_events):
		# EvAct = enum('Up', 'Down', 'Left', 'Right', 'Submit', 'Exit', 'Pause')
		# -1 = left, 0 = nothing, +1 = right
		events = [g.dir for g in game_events]
		direction = int(EvAct.Right in events) - int(EvAct.Left in events)
		thrust = int(EvAct.Submit in events)
		cmds = {'direction': direction, 'thrust': thrust}
		self.network.send_cmds(cmds)

	def tick(self):
		pass

	def visualize(self):
		self.surf.fill((0, 0, 0))

		self.vis_ship(0.2, 0.2, True)
		self.vis_ship(0.4, 0.7)
		self.vis_ship(0.1, 0.9)
		self.vis_ship(1, 0.9)
		self.vis_ship(0.1, 1)
		self.vis_ship(1, 1)

		self.vis_footer()

		return self.surf

	def vis_ship(self, x, y, me=False):
		color = (255, 0, 0) if me else (0, 0, 255)
		pygame.draw.circle(self.surf, color, (int(x * XXX), int(y * YYY)), 10)

	def vis_footer(self):
		pygame.draw.line(self.surf, (255, 255, 255), (XXX, 0), (XXX, YYY), 1)
