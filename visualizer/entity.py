# -*- coding: utf-8 *-*

import pygame


class SpaceThing(pygame.math.Vector2):

	def __init__(self, obj):
		super().__init__(obj['x'], obj['y'])
		self.r = obj['r']
		self.tra = list(zip(obj['tx'], obj['ty']))

	def __repr__(self):
		return "SpaceThing<%f,%f,r=%f,tra_count=%d>" % (self.x, self.y, self.r, len(self.tra))


SpaceThing.__str__ = SpaceThing.__repr__


class Player(SpaceThing):
	def __init__(self, obj):
		obj['r'] = 10
		super().__init__(obj)
		self.vel = pygame.math.Vector2(obj['vx'], obj['vy'])
		self.phi = obj['phi']

	def __repr__(self):
		return "Player<%s,vel=%s,phi=%d>" % (super().__repr__(), self.vel, self.phi)
