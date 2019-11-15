#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from definitions import *

import pygame


DEADZONE = 0.1


class MenuEvent:
	def __init__(self, act: EvAct):
		self.action = act

	def __str__(self):
		return "MenuEvent<%s>" % self.action

	def __repr__(self):
		return str(self)

	def __eq__(self, other):  # better save than sorry
		return self.action == other.action


class GameEvent:

	def __init__(self, p: int, d: EvAct):
		self.player = p  # 1-4
		self.dir = d  # Left,Right

	def __str__(self):
		return "GameEvent<%d,%s>" % (self.player, self.dir)

	def __repr__(self):
		return str(self)

	def __eq__(self, other):  # better save than sorry
		return self.player == other.player and self.dir == other.dir


class EventProcessor:

	def __init__(self):
		self.joysticks = self.init_joysticks()
		self.menu_events = []  # list of Key Down Keyboard Events. cleared and re-written each tick
		self.game_events = []  # retained across ticks and updated according to input

	@staticmethod
	def init_joysticks():
		# The following event types will be generated by the joysticks: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		# we only really care about: JOYAXISMOTION and JOYBUTTONDOWN
		# SNES GamePad:
		#   Cross X=0: links=-1 rechts=1
		#   Cross Y=1: oben=-1 unten=1
		#   Buttons: A=1 B=2 X=0 Y=3   L=4 R=5   Select=8 Start=9
		print("There are %d joysticks!" % pygame.joystick.get_count())
		joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		if not joysticks:
			return []
		for joy in joysticks:
			joy.init()
			print(joy, joy.get_name(), joy.get_numaxes(), joy.get_numballs(), joy.get_numbuttons(), joy.get_numhats())
			#get_axis', 'get_ball', 'get_button', 'get_hat', 'get_id', 'get_init', 'get_name', 'get_numaxes', 'get_numballs', 'get_numbuttons', 'get_numhats
		joysticks = [j for j in joysticks if j.get_init()]
		print("Successfully initialized %d joysticks!" % len(joysticks))
		return joysticks

	def quit_joysticks(self):
		for joy in self.joysticks:
			joy.quit()

	@staticmethod
	def keyboard_2_menu_event(menu_events, ke):
		if ke.type in [KEYDOWN, KEYUP] and ke.key in KEYS:
			if ke.type == KEYDOWN:
				for key, act in MENU_KEYS.items():
					if ke.key == key:
						menu_events.append(MenuEvent(act))
		return menu_events

	@staticmethod
	def joystick_2_menu_event(menu_events, je):
		if je.type == JOYBUTTONDOWN:
			# TODO: Maybe differentiate between different buttons in some meaningful way...
			menu_events.append(MenuEvent(EvAct.Submit))
		if je.type == JOYHATMOTION:
			pass
		if je.type == JOYAXISMOTION:
			if je.axis == 1:  # Cross Y=1: oben=-1 unten=1
				if je.value < 0:
					menu_events.append(MenuEvent(EvAct.Up))
				if je.value > 0:
					menu_events.append(MenuEvent(EvAct.Down))
			elif je.axis == 0:  # Cross X=0: links=-1 rechts=1
				if je.value < 0:
					menu_events.append(MenuEvent(EvAct.Left))
				elif je.value > 0:
					menu_events.append(MenuEvent(EvAct.Right))
		return menu_events

	@staticmethod
	def keyboard_2_game_event(game_events, ke):
		def handle_player_key_game_event(player_keys, num):
			for key, act in player_keys.items():
				if ke.key == key:
					ge = GameEvent(num, act)
					if ke.type == KEYDOWN:
						game_events.append(ge)
					elif ke.type == KEYUP and ge in game_events:
						game_events.remove(ge)
		handle_player_key_game_event(PLAYER_1_KEYS, 0)
		handle_player_key_game_event(PLAYER_2_KEYS, 1)
		handle_player_key_game_event(PLAYER_3_KEYS, 2)
		handle_player_key_game_event(PLAYER_4_KEYS, 3)
		return game_events

	def joystick_2_game_event(self, game_events, je):

		if je.type == JOYHATMOTION:
			dir = je.value[0]
			if dir == 0:  # this is like "Key up" but we don't know from which side (left/right) we came from
				game_events = [ge for ge in game_events if ge.player != je.joy]
			elif dir < 0:
				game_events.append(GameEvent(je.joy, EvAct.Left))
			elif dir > 0:
				game_events.append(GameEvent(je.joy, EvAct.Right))

		# if a joystick has a HAT, ignore Axis Motions from it
		if je.type == JOYAXISMOTION and self.joysticks[je.joy].get_numhats() > 0:
			return game_events

		if je.type == JOYAXISMOTION:
			if je.axis == 0:  # Cross X=0: links=-1 rechts=1
				if je.value == 0:  # this is like "Key up" but we don't know from which side (left/right) we came from
					game_events = [ge for ge in game_events if ge.player != je.joy]
				elif je.value < 0:
					game_events.append(GameEvent(je.joy, EvAct.Left))
				elif je.value > 0:
					game_events.append(GameEvent(je.joy, EvAct.Right))
		return game_events

	def process_new_events(self, rawEventList):
		# reduce events to key strokes we care about
		rawKeyEvents = [rke for rke in rawEventList if rke.type in [KEYDOWN, KEYUP] and rke.key in KEYS]
		rawJoyEvents = [rje for rje in rawEventList if rje.type in [JOYBUTTONDOWN, JOYBUTTONUP, JOYAXISMOTION, JOYHATMOTION]]
		rawJoyEvents = [rje for rje in rawJoyEvents if rje.type != JOYAXISMOTION or (rje.type == JOYAXISMOTION and abs(rje.value) > DEADZONE)]

		# TODO: if we have a HAT, drop all axis motions from that joystick and only user HAT events

		# reset every tick
		self.menu_events = []

		for ke in rawKeyEvents:
			# Raw Key Events to Menu Events
			self.menu_events = self.keyboard_2_menu_event(self.menu_events, ke)
			# Raw Key Events to Game Events
			self.game_events = self.keyboard_2_game_event(self.game_events, ke)

		for je in rawJoyEvents:
			# Raw Joystick Events to Menu Events
			self.menu_events = self.joystick_2_menu_event(self.menu_events, je)
			# Raw Joystick Events to Game Events
			self.game_events = self.joystick_2_game_event(self.game_events, je)

	def get_menu_events(self):
		return self.menu_events

	def get_game_events(self):
		return self.game_events
