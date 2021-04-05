#! /usr/bin/python

import interfaceUtils as iU
import numpy as np
import random

from worldLoader import WorldSlice

# Load the map in a numpy array, check for areas above a certain high.
# Floodfill those to find different peaks
# Filter areas that do not have 3x3

build_area = iU.makeBuildArea()
print(build_area)

slice = WorldSlice(build_area)
hmb = slice.heightmaps['MOTION_BLOCKING_NO_LEAVES']
# Heightmaps
# ["MOTION_BLOCKING", "MOTION_BLOCKING_NO_LEAVES", "OCEAN_FLOOR", "WORLD_SURFACE"]

## List the highest blocks

_h = np.where(hmb == np.amax(hmb))
highest = list(zip(_h[0], _h[1]))

for coord in highest:
    cx = coord[0]+build_area[0] # Note that the heightmap is relative
    cz = coord[1]+build_area[1] # Note that the heightmap is relative
    cy = hmb[coord[0], coord[1]]-1
    block = iU.getBlock(cx, cy, cz)
    print("Highest block at ({}, {}): {}".format(cx, cz, block))

# Building a cairn at a random highest point:
target = np.array(random.choice(highest))

## adding offsets
print("Building Cairn at {}".format(target+build_area[:2]))

# Build Things:
_y = hmb[target[0], target[1]]

for _i in range(-1,2):
    for _j in range(-1,2):
        x, z = target + build_area[:2] + (_i,_j)

        # Netherrack base
        for y in range(40, _y):
            iU.placeBlockBatched(x, y, z, "minecraft:netherrack")

        #build nether fence around it, and glowstone middle pillar.
        if (_i or _j):
            iU.placeBlockBatched(x, _y-1, z, "minecraft:nether_bricks")
            iU.placeBlockBatched(x, _y, z, "minecraft:nether_brick_fence")
        else:
            iU.placeBlockBatched(x, _y, z, "minecraft:glowstone")
            iU.placeBlockBatched(x, _y+1, z, "minecraft:glowstone")
            iU.placeBlockBatched(x, _y+2, z, "minecraft:glowstone")
            iU.placeBlockBatched(x, _y+3, z, "minecraft:nether_brick_slab")

iU.sendBlocks()
