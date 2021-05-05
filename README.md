# GDMC2021Tsukuba

To have a debug mode and save world modification you should have a config/config.json file. With "debugMode" : true at the root of the json file.
If debugMode = true, it will save modification done to the world in file named temp.txt. If it exists, temp_0.txt, temp_1.txt, ...

Lauch python _generateSettlement.py, the main script, to generate our settlements. 
If you want to undo modification, add option r (= temp.txt) or the name of the file.
Ex : 
python _generateSettlement.py r
python _generateSettlement.py temp_1.txt
