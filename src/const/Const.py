# -*- coding: utf-8 -*-

'''
Created on Mar 10, 2013

@author: dstu
'''

import colors
from delvelibConst import *

# Global constants

TITLE = "Chronicles of Ériu"

########################
#
# World Map
#
########################

WORLD_MAP_WIDTH = 55
WORLD_MAP_HEIGHT = 93

NUM_KINGDOMS = 5
NUM_REGIONS = 40
REGIONS_CLAIMED_PERCENT = 0.75
REGIONS_PER_KINGDOM = int(NUM_REGIONS*REGIONS_CLAIMED_PERCENT/NUM_KINGDOMS)

MIN_TOWNS_PER_REGION = 2
MAX_TOWNS_PER_REGION = 5
REGION_TILES_PER_CITY = 30
MIN_TOWN_SPACING = 2
STARTING_TOWN_SPACING = 5

NUM_RIVERS = 5
MIN_RIVER_LENGTH = 3
RIVER_TILES_PER_BRIDGE = 15
BRIDGE_SPACING = 7
assert RIVER_TILES_PER_BRIDGE > 2*BRIDGE_SPACING # Stupid check
LAKE_CHANCE_PER_RIVER = 1 # 0.5
LAKE_CHANCE_PER_TILE = 0.3
LAKE_RADIUS = 2 # Actual size will be (2*rad + 1)^2
LAKE_DIAMETER = 2*LAKE_RADIUS + 1

DUNGEON_CHANCE = 0.1 # Chance for a map tile to get a dungeon

########################
#
# Dungeon Generation
#
########################

# Some dungeon generation constants

# These can all go when the new wang tile stuff gets working
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
DUNGEON_MARGIN = 2
MAX_ROOMS_AND_CORRIDORS = 100
ROOM_CHANCE = 75

TOWN_CELL_WIDTH = 40
TOWN_CELL_HEIGHT = 40

# Max monsters per room
MAX_ROOM_MONSTERS = 3

# Max items per room
MAX_ROOM_ITEMS = 2

#ROOM_MAX_SIZE = 3
#ROOM_MIN_SIZE = 1
#MAX_ROOMS = 3
#DUNGEON_MARGIN = 0
