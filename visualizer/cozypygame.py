#!/usr/bin/env python3
# -*- coding: utf-8 *-*

# No game logic here, just helper functions

import pygame
from pygame.locals import *

# def getimagepath(img):
# 	return 'image/' + str(img) + '.png'
# 	# also care for other extensions
# 	# TODO: recursively search the pic folder
#
# def getimageobject(img):
# 	if img[-4:] == ".png":
# 		return pygame.image.load(img)
# 	else:
# 		return pygame.image.load(getimagepath(img))

POOL = {}


def load_image_cached(img):
	try:
		# print("CACHE HIT!")
		return POOL[img]
	except Exception:
		# print("Caching...")
		POOL[img] = pygame.image.load(img).convert_alpha()
		return POOL[img]


def isDownPress(e):
	return e.type == KEYDOWN


def enum(*seq, **named):
	# don't even ask
	return type('Enum', (), dict(list(zip(seq, list(range(len(seq))))), **named))


def draw_text(surf, text, font, pos, color):
	"""render some text. pos is the _middle_ of the boundary box"""
	label = font.render(text, 1, color)
	posi = label.get_rect(centerx=pos[0], centery=pos[1])
	surf.blit(label, posi)


SUBCACHE = {}


def subimage(img, totalX, totalY, x, y):
	key = (img, totalX, totalY, x, y)
	if key in SUBCACHE:
		# print("SUBIMAGE CACHE HIT")
		return SUBCACHE[key]
	pic = load_image_cached(img)
	oneX = pic.get_width() / totalX
	oneY = pic.get_height() / totalY
	r = Rect((x * oneX, y * oneY), (oneX, oneY))
	# return pygame.transform.chop(pic, r)
	SUBCACHE[key] = pic.subsurface(r)
	# print("SUBIMAGE CACHING!")
	return SUBCACHE[key]


SOUNDPOOL = {}


def load_sound(filename):
	if filename not in SOUNDPOOL:
		SOUNDPOOL[filename] = pygame.mixer.Sound(filename)
	return SOUNDPOOL[filename]


def play_sound(filename):
	load_sound(filename).play()


def stop_background_music():
	pygame.mixer.music.stop()


# pygame.mixer.music.unload()

def start_background_music(music):
	pygame.mixer.music.load('music/%s.mp3' % music)
	pygame.mixer.music.play(-1)


def circle_collide(pos1, r1, pos2, r2):
	(x1, y1) = pos1
	(x2, y2) = pos2
	return ((x2 - x1) ** 2 + (y1 - y2) ** 2) <= ((r1 + r2) ** 2)


def argmax(list):
	return max(range(len(list)), key=list.__getitem__)
