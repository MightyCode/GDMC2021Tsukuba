# GDMC2021Tsukuba

To have a debug mode and save world modification you need to have a config/config.json file and to put "debugMode" : true at the root of the json file.
If debugMode is set as true, it will save modification done to the world in a file named temp.txt. If it exists it will create several file named such as : temp_0.txt, temp_1.txt, ...
notice that it will be very much slower with debugMode.

Launch python "_generateSettlement.py" , the main script, to generate our settlements. <br/><br/>
Build a Minecraft Settlement, by Tsukuba Team (2021) <br/>

usage: _generateSettlement.py [-h] [-p | -c x0 y0 z0 x1 y1 z1] [-a A] [-r [R]] <br/>
optional arguments: <br/>
  -h, --help            show this help message and exit <br/>
  -p, --player          build the settlement around the player's current location <br/>
  -c x0 y0 z0 x1 y1 z1, --coordinates x0 y0 z0 x1 y1 z1 <br/>
                        build the settlement on the area defined by these coordinates <br/>
  -a A, --radius A      Radius for building area, only meaningful with -p <br/>
  -r [R], --remove [R]  Remove all structure if debug was activated, temp.txt if r specified, elsewhere file name: -r temp_0.txt <br/>
  
_Exemple :_ <br/>
python .\_generateSettlement.py -p -a 150 <br/>
  
  
Then, if debugMode in config/config.json is set as True, you can remove the construction with : <br/>
python .\_generateSettlement.py -r r
  
  
## Current bugs
Sometimes due to library https interface, the program stops, saying that too many sockets were created.
