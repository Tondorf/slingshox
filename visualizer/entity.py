# -*- coding: utf-8 *-*

import pygame


class Thing(pygame.math.Vector2):

	def __init__(self, x, y, r):
		super().__init__(x, y)
		self.r = r

	def __repr__(self):
		return "Thing<%d,%d,r=%d>" % (self.x, self.y, self.r)


class Player(Thing):
	def __init__(self, pos, velocity, phi, trajectories):
		super().__init__(pos.x, pos.y, 10)
		self.vel = velocity
		self.phi = phi
		self.tra = trajectories

	def __repr__(self):
		return "Player<%s,%s,phi=%d,tra_count=%d>" % (super().__repr__(), self.vel, self.phi, len(self.tra))
