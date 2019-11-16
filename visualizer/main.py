#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import sys

from cozypygame import *
from definitions import *
from mode import Modes
from world import World
from controls import EventProcessor

# init pygame
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.joystick.init()
pygame.display.set_caption('')
print(XXX, dispYYY)
if not FULLSCREEN:
	display = pygame.display.set_mode((XXX, dispYYY))
else:
	display = pygame.display.set_mode((XXX, dispYYY), pygame.FULLSCREEN)
fpsClock = pygame.time.Clock()
tick = 0

if FULLSCREEN:
	pygame.mouse.set_visible(False)
pygame.event.set_blocked(pygame.MOUSEMOTION)

# initialize all the shit
world = World(Modes.Game)

ep = EventProcessor()
world.ep = ep

#start_background_music('menu')

while world.running:  # main game loop

	##############
	### EVENTS ###
	##############
	# get events
	rawEvents = pygame.event.get()
	ep.process_new_events(rawEvents)

	# This is the ONLY place where we directly interact on raw events!
	# check for quit event
	if any(e.type == QUIT or (isDownPress(e) and e.key == K_ESCAPE) for e in rawEvents):
		break

	world.input(ep.get_menu_events(), ep.get_game_events())

	############
	### TICK ###
	############
	world.tick()

	##############
	### RENDER ###
	##############
	#display.fill((0, 0, 0))
	display.blit(world.visualize(), (0, 0))
	pygame.display.update()

	############
	### WAIT ###
	############
	tick = tick % 3000 + 1  # avoid overflow
	fpsClock.tick(FPS)

# tidy up and quit
ep.quit_joysticks()
pygame.joystick.quit()
if FULLSCREEN:
	pygame.mouse.set_visible(True)
pygame.quit()
sys.exit(0)
