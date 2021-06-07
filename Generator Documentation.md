# General explanation

The main file which makes the generation working is *generateSettlement.py*.
The generator work in 5 steps, *generator.py* is mainly use.


. The script generateSettlement inits data of the main dictionnary **settlementData**.
. Then the script searchs what should be the next structure using *structureManager.py* and find its position with *floodFill.py*.
. After that, the scripts creates the lore of the village, likes main books describing the village or a register of villagers.
. The creation of lore finished, generateSettlement uses *road.py* to create roads.
. Finally each structure is finally builded and decorations are placed. 

The idea is to -> find every informations for the village.
-> Then build.


Note : 
1. Structure = big batiment which takes more than 3 blocks long.
2. Decoration = little structure with 1 or 2 blocks long (ex : haybale block). It maked the village more lifely.


# Description of each file.

## generation/*resources.py*

This resources class stores each loaded files. 
To make the systeme easier, instance of generated structure class is also store on the structures.

## generation/*resourcesLoader.py*

This utility class preload the instance of resource class with every structure and lootTable used for the generation.

## *testStructures.py*

This test file if the most useful file to test one structure
You just have to change in this line **structure = resources.structures["xxx"]** where xxx is the name of your structure