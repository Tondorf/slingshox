#!/usr/bin/env python3
# -*- coding: utf-8 *-*

import sys
import asyncio

from cozypygame import *
from definitions import *
from world import World
from controls import EventProcessor
from network import Client

# init pygame
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.joystick.init()
pygame.display.set_caption('')
print(dispXXX, dispYYY)
if not FULLSCREEN:
	display = pygame.display.set_mode((dispXXX, dispYYY))
else:
	display = pygame.display.set_mode((dispXXX, dispYYY), pygame.FULLSCREEN)
fpsClock = pygame.time.Clock()
tick = 0

if FULLSCREEN:
	pygame.mouse.set_visible(False)
pygame.event.set_blocked(pygame.MOUSEMOTION)

# initialize all the shit
world = World()

network = Client(world)

ep = EventProcessor()
world.ep = ep

#start_background_music('menu')


async def main_game_loop(loop):
	global tick
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
		await asyncio.sleep(0.01, loop=loop)
		fpsClock.tick(FPS)


async def start(loop):
	tasks = [network.handle(loop), main_game_loop(loop)]
	done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, loop=loop)

	for task in pending:
		task.cancel()


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(start(loop))
	loop.close()


# tidy up and quit
ep.quit_joysticks()
pygame.joystick.quit()
if FULLSCREEN:
	pygame.mouse.set_visible(True)
pygame.quit()
sys.exit(0)
