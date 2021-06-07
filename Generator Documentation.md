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


## *benchmarkTimeForBuilding.py*

This test file will construct a certain amount of same structure and show time took for construction


## *generateSettlement.py*

This script run the main procedure and main steps to create the village


## generation/*generator.py*

This script gathers functionalities that could be in *generateSettlement.py* but placed here for more readability


## generation/*chestGeneration.py*

This class file objectif is to generate a chest's content located at certain position. 
It uses look table, and additionnal object which are items that must be added to the chest independently of the loot table


## generation/*structureManager.py*

This class will fill settlementData with the next structure that should be added. 
The method to choose structure is a technological tree.
Image of the technological tree is on documentation folder.
Each structure group has a prerequisite to be available.
 
After that, each strucure available has a weight depending of its type, or if the previous choosen structure was the same; then the random choose the next.
