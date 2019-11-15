#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from cozypygame import enum

""" There are different modes for this application
	From these modes, exactly one is active at a given time. This can be considered a state machine

	Intro : Start Here. Before the start screen. Only occurs right at the beginning of the program.
	StartScreen : The start screen. The player can choose between local, network, challenge, quit
	Config : Here the player can select the role of each Brush (player, AI, disabled) and configure Teams, Timeout and required medals for winning
	Ingame : The mode the player probably wants to spend the most time in :) [one mode for Challenge/SingleBattle/TeamBattle]

	Highscore : Watch the highscore for the challenge mode.
	Winner : Results for local mode

	ConfigNetwork : Wont implement this until everything else works perfectly
	IngameNetwork : dito
	ResultNetwork : dito

	Transition : The Transition Manager is working and NO ONE SHOULD DISTRACT IT! :D

"""

Modes = enum('Intro',
             'Ingame',
             )


class Mode(object):

	def __init__(self, world):
		self.world = world

	def activate(self):
		"""post-ctor init stuff"""
		raise NotImplementedError("Subclasses should implement this!")

	def input(self, menu_events, game_events):
		"""get: world + [menu events] + [game events]
		   return: nothing
		"""
		raise NotImplementedError("Subclasses should implement this!")

	def tick(self):
		"""get: world
		   return: nothing
		"""
		raise NotImplementedError("Subclasses should implement this!")

	def visualize(self):
		"""get: world
		   return: the Surface that shall be drawn"""
		raise NotImplementedError("Subclasses should implement this!")
