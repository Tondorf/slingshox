#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from pygame.locals import *
from cozypygame import enum

FULLSCREEN = 0
DEVEL = 1

FPS = 30

EvAct = enum('Up', 'Down', 'Left', 'Right', 'Submit', 'Exit', 'Pause')

# variable initiations
MENU_KEYS = {K_LEFT: EvAct.Left, K_RIGHT: EvAct.Right, K_DOWN: EvAct.Down, K_UP: EvAct.Up, K_RETURN: EvAct.Submit, K_SPACE: EvAct.Submit, K_ESCAPE: EvAct.Exit}
INGAME_KEYS = {K_ESCAPE: EvAct.Exit, K_PAUSE: EvAct.Pause}
PLAYER_1_KEYS = {K_LEFT: EvAct.Left, K_RIGHT: EvAct.Right}
PLAYER_2_KEYS = {K_z: EvAct.Left, K_y: EvAct.Left, K_x: EvAct.Right} # y is treated like z because Z and Y are swapped on German keyboards
PLAYER_3_KEYS = {K_n: EvAct.Left, K_m: EvAct.Right}
PLAYER_4_KEYS = {K_KP4: EvAct.Left, K_KP6: EvAct.Right, K_4: EvAct.Left, K_6: EvAct.Right}  # also include 4 and 6 so that brush 4 can be controlled on keyboards without a numpad

# | for sets is union
CONTROL_KEYS = MENU_KEYS.keys() | INGAME_KEYS.keys()
MOVEMENT_KEYS = PLAYER_1_KEYS.keys() | PLAYER_2_KEYS.keys() | PLAYER_3_KEYS.keys() | PLAYER_4_KEYS.keys()
KEYS = CONTROL_KEYS | MOVEMENT_KEYS
