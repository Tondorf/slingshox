# -*- coding: utf-8 *-*

from pygame.locals import *
from cozypygame import enum

FULLSCREEN = 0
DEVEL = 1

XXX = 1000
YYY = XXX

dispXXX = int(XXX * 1.2)
dispYYY = int(YYY)

FPS = 30

EvAct = enum('Up', 'Down', 'Left', 'Right', 'Submit', 'Exit', 'Pause')

# variable initiations
MENU_KEYS = {K_LEFT: EvAct.Left, K_RIGHT: EvAct.Right, K_DOWN: EvAct.Down, K_UP: EvAct.Up, K_RETURN: EvAct.Submit, K_SPACE: EvAct.Submit, K_ESCAPE: EvAct.Exit}
INGAME_KEYS = {K_ESCAPE: EvAct.Exit, K_PAUSE: EvAct.Pause}
PLAYER_1_KEYS = {K_LEFT: EvAct.Left, K_RIGHT: EvAct.Right, K_SPACE: EvAct.Submit}
PLAYER_2_KEYS = {K_z: EvAct.Left, K_y: EvAct.Left, K_x: EvAct.Right} # y is treated like z because Z and Y are swapped on German keyboards
PLAYER_3_KEYS = {K_n: EvAct.Left, K_m: EvAct.Right}
PLAYER_4_KEYS = {K_KP4: EvAct.Left, K_KP6: EvAct.Right, K_4: EvAct.Left, K_6: EvAct.Right}  # also include 4 and 6 so that brush 4 can be controlled on keyboards without a numpad

# | for sets is union
CONTROL_KEYS = MENU_KEYS.keys() | INGAME_KEYS.keys()
MOVEMENT_KEYS = PLAYER_1_KEYS.keys() | PLAYER_2_KEYS.keys() | PLAYER_3_KEYS.keys() | PLAYER_4_KEYS.keys()
KEYS = CONTROL_KEYS | MOVEMENT_KEYS

# SNES-like joystick
#   Cross X=0: links=-1 rechts=1
#   Cross Y=1: oben=-1 unten=1
#   Buttons: A=1 B=2 X=0 Y=3   L=4 R=5   Select=8 Start=9
SNES_AXIS_X = 0
SNES_AXIS_Y = 1
SNES_A = 1
SNES_B = 2
SNES_X = 0
SNEX_Y = 3
SNES_L = 4
SNES_R = 5
SNES_Select = 8
SNEX_Start = 9
