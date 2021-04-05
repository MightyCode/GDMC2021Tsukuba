import random
import interfaceUtils

# Add text to a sign
def setSignText(x, y, z, line1 = "", line2 = "", line3 = "", line4 = ""):
    l1 = 'Text1:\'{"text":"'+line1+'"}\''
    l2 = 'Text2:\'{"text":"'+line2+'"}\''
    l3 = 'Text3:\'{"text":"'+line3+'"}\''
    l4 = 'Text4:\'{"text":"'+line4+'"}\''
    blockNBT = "{"+l1+","+l2+","+l3+","+l4+"}"
    interfaceUtils.runCommand("data merge block {} {} {} ".format(x, y, z)
                              + blockNBT)

# Add items to a chest
# Items is a list of [item string, item quantity]
def addItemChest(x, y, z, items):
    for id,v in enumerate(items):
        command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                               "container."+str(id),
                                                               v[0],
                                                               v[1])
        interfaceUtils.runCommand(command)

# Create a book item from a text

def makeBookItem(text, title = "", author = "", desc = ""):
    booktext = "pages:["
    while len(text) > 0:
        page = text[:15*23]
        text = text[15*23:]
        bookpage = "'{\"text\":\""
        while len(page) > 0:
            line = page[:23]
            page = page[23:]
            bookpage += line+"\\\\n"
        bookpage += "\"}',"
        booktext += bookpage

    booktext = booktext + "],"

    booktitle = "title:\""+title+"\","
    bookauthor = "author:\""+author+"\","
    bookdesc = "display:{Lore:[\""+desc+"\"]}"

    return "written_book{"+booktext+booktitle+bookauthor+bookdesc+"}"


# x position, z position, x size, z size
area = (0, 0, 128, 128)  # default build area if build area is not set

interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")

# see if a build area has been specified
# you can set a build area in minecraft using the /setbuildarea command
buildArea = interfaceUtils.requestBuildArea()
if buildArea != -1:
    x1 = buildArea["xFrom"]
    z1 = buildArea["zFrom"]
    x2 = buildArea["xTo"]
    z2 = buildArea["zTo"]
    # print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)

# Experiment 1: Find the highest non-air block and build a platform there

cx = int(area[0] + area[2]/2)
cz = int(area[1] + area[3]/2)

## Find highest non-air block
## Note that in real construction, you want to ignore "transparent" blocks,
## Such as leaves, snow, grass, etc.
cy = 255
while interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:air':
    cy -= 1
cy += 10

## Building the platform.
for dx in range(11):
    for dz in range(11):
        interfaceUtils.placeBlockBatched(cx+dx-5, cy, cz+dz-5, "minecraft:cobblestone")
interfaceUtils.sendBlocks()

# Add signs
interfaceUtils.setBlock(cx, cy+1, cz, "minecraft:oak_sign[rotation={}]".format(random.randint(0,9)))
setSignText(cx, cy+1, cz, "Line One", "Line 2")

interfaceUtils.setBlock(cx+3, cy+1, cz, "minecraft:bricks")
interfaceUtils.setBlock(cx+2, cy+1, cz, "minecraft:oak_wall_sign[facing=west]")
setSignText(cx+2, cy+1, cz, "", "This is a wall sign")

# Add chest with items
interfaceUtils.setBlock(cx-3, cy+1, cz, "minecraft:chest")
book = makeBookItem("A very smol book", title = "", author = "", desc = "A book")
print(book)
items = [["minecraft:iron_axe", 1], ["minecraft:diamond", 10], [book, 1]]
addItemChest(cx-3, cy+1, cz, items)

# TODO: Add a book to a lectern
