# -*- coding: utf-8 *-*

import pygame


class Entity:

    def __init__(self, world=None, x=320, y=240, z=0):
        self.world = world
        self._pos = pygame.math.Vector2(x, y)
        self._z = z

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        (x, y) = pos
        self._pos = pygame.math.Vector2(x, y)

    @property
    def x(self):
        return self._pos.x
    @x.setter
    def x(self, x):
        self._pos.x = x

    @property
    def y(self):
        return self._pos.y
    @y.setter
    def y(self, y):
        self._pos.y = y

    @property
    def z(self):
        return self._z
    @z.setter
    def z(self, z):
        self._z = z
