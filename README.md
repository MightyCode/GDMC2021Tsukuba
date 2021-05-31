# GDMC2021
Tsukuba Team

To run this project be sure to have the http interface mod (available here : https://github.com/nilsgawlik/gdmc_http_interface) , please run generatesettlement.py after setting in minecraft a setbuildarea of your choice. You can also use some argument if you do not want to set a build area directly in minecraft :
  
use :

-p, --player          build the settlement around the player's current location
  
-c x0 y0 z0 x1 y1 z1, --coordinates x0 y0 z0 x1 y1 z1
   build the settlement on the area defined by these coordinates</p>
   
-b, --buildarea       Build the settlement using a pre-existing buildArea (equivalent to not putting any argument
  
 -a A, --radius A      Radius for building area, only meaningful with -p
  
 -r [R], --remove [R]  Remove all structure if debug was activated, temp.txt if r specified, elsewhere file name: -r temp_0.txt
  
example :

python .\_generateSettlement.py -p -a 150 
 
To activate the debug mode and save world modification, you need to set debugMode as True in the config/config.json file
notice that it will be very much slower with debugMode.

**Description :**
This Minecraft Settlement Generator is generating a coherent minecraft village, with unique interaction between villagers and a Tree enhancement of House, and with each new House generated after a new chunk discovery would have the possibly to be more advanced than the previous one.

**What it does concretely :**
Based on the size of the area the player has set, the program will decide if it will try to generate X village within there is Y Houses if the area is larger than 250 block. Then it will decide on the location of the first house of the first village. From that, it will then place houses at a random distance (but acceptable) from each other in connected area, discovering new chunk after an other and adding materials unlocked thanks to that. When the program decide to place a new house, it will look at houses already built and ressources available to then decide which house will be built.


**Future of this program :**
We want to work on interaction between villages, implement new houses, make more uniqueness villages based on more detailed ressources and use the interaction between villages to upgrade each villages "together" (or not if they are ennemies).
