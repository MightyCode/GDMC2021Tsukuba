import sys
import lib.interfaceUtils as interfaceUtils
import collections, numpy


interface = interfaceUtils.Interface()

listOfBlocks = numpy.array([])

# x position, z position, x size, z size
area = (0, 0, 128, 128)  # default build area if build area is not set

interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")


# see if a build area has been specified
# you can set a build area in minecraft using the /setbuildarea command
buildArea = interfaceUtils.requestBuildArea()
if buildArea == -1:
    exit()
x1 = buildArea[0]
z1 = buildArea[2]
x2 = buildArea[3]
z2 = buildArea[5]
# print(buildArea)
area = (x1, z1, x2 - x1, z2 - z1)

# Find the highest non-air block and build the quarry there

cx = int(area[0] + area[2]/2)
cz = int(area[1] + area[3]/2)

## Find highest non-air block
## Note that in real construction, you want to ignore "transparent" blocks,
## Such as leaves, snow, grass, etc.
cy = 255
while interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:air' :
    cy -= 1


## Building the quarry.
for dy in range(11):
    for dx in range(11):
        for dz in range(11):
            block = interfaceUtils.getBlock(cx+dx, cy-dy, cz+dz)
            listOfBlocks = numpy.append(listOfBlocks, block)
            interfaceUtils.setBlock(cx+dx, cy-dy, cz+dz, "minecraft:air")
interfaceUtils.sendBlocks()

print(collections.Counter(listOfBlocks))
print("Done")
