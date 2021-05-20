import random as rd
import pandas as pd
import numpy as np
import lib.interfaceUtils as interfaceUtils
import lookup



"""
Return the text of the book of the village presentation
"""
def createTextOfPresentationVillage(villageName, villagerNames, structuresNumber, structuresNames):
    textVillagePresentationBook = (
            '\f\\\\s--------------\\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '   Welcome to      \\\\n'
           f' {villageName} \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '--------------')
    textVillagePresentationBook += ('\f\\\\s---------------\\\\n')
    textVillagePresentationBook += ('There are '
        f'{len(villagerNames)} villagers in this village\\\\n')
    textVillagePresentationBook += ('---------------\\\\n\f')
    textVillagePresentationBook += ('\f\\\\s---------------\\\\n'
                      'There are '
                      f'{structuresNumber} structures : \\\\n')
    for i in range(len(structuresNames)):
        if i <= 10:
            textVillagePresentationBook += (f'{structuresNames[i]["name"]} ')
        if i % 10 == 0:
            textVillagePresentationBook += ('-----------------\\\\n\f')
        if i > 10:
            textVillagePresentationBook += (f'{structuresNames[i]["name"]} ')
    textVillagePresentationBook += ('---------------\\\\n\f')
    
    return textVillagePresentationBook

"""
Return the text of the book of the villagers names and professions
"""
def createTextForVillagersNames(listOfVillagers):
    textVillagerNames = ('\f\\\\s-----------------\\\\n')
    for i in range(len(listOfVillagers)):
        if i <= 6: 
            textVillagerNames += (f'{listOfVillagers[i]}       \\\\n')
        if i % 6 == 0:
            textVillagerNames += ('-----------------\\\\n\f')
        if i > 6:
            textVillagerNames += (f'{listOfVillagers[i]}       \\\\n')
    textVillagerNames += ('-----------------\\\\n\f')
    return textVillagerNames

def addResourcesFromChunk(resources, settlementData, biome):
    if biome == "-1":
        return
        
    dictResources = resources.biomesBlocks[biome]
    if "woodResources" in dictResources:
        settlementData["woodResources"] += dictResources["woodResources"]
    if "dirtResources" in dictResources:
        settlementData["dirtResources"] += dictResources["dirtResources"]
    if "stoneResources" in dictResources:
        settlementData["stoneResources"] += dictResources["stoneResources"]


"""
Return result and word
result 0 -> No balise founded
result 1 -> Balise founded and replacement succeful
result -1 -> Error
"""
def changeNameWithBalise(name, changementsWord):
    index = name.find("*")
    if index != -1 :
        secondIndex = name.find("*", index+1)
        if secondIndex == -1:
            return [-1, name]

        word = name[index +1 : secondIndex]
        added = False
        for key in changementsWord.keys():
            if key == word:
                added = True
                return [1, name.replace("*" + word + "*", changementsWord[key])]
                        
        # If the balise can't be replace
        if not added:
            return [-1, name]
    
    else:
        return  [0, name]


def addBookToLectern(x, y, z, bookData):
    command = (f'data merge block {x} {y} {z} '
                    f'{{Book: {{id: "minecraft:written_book", '
                    f'Count: 1b, tag: {bookData}'
                    '}, Page: 0}')

    response = interfaceUtils.runCommand(command)
    if not response.isnumeric():
        print(f"{lookup.TCOLORS['orange']}Warning: Server returned error "
            f"upon placing book in lectern:\n\t{lookup.TCOLORS['CLR']}"
            f"{response}")

"""
Spawn a villager at his house if unemployed or at his building of work
"""
def spawnVillagerForStructure(settlementData, structureData, position):
    for id in structureData["villagersId"]:
        if (structureData["type"] == "houses" and settlementData["villagerProfession"][id] == "Unemployed") or (structureData["type"] != "houses" and settlementData["villagerProfession"][id] != "Unemployed") : 
            # get a random level for the profession of the villager (2: Apprentice, 3: Journeyman, 4: Expert, 5: Master)
            randomProfessionLevel = rd.randint(2, 5)

            spawnVillager(position[0], position[1], position[2], "minecraft:villager", 
                settlementData["villagerNames"][id], settlementData["villagerGameProfession"][id], randomProfessionLevel, settlementData["biomeName"])

VILLAGER_NAME_PATH = "data/names/"
NUMBER = 5
MIN_SIZE = 4
MAX_SIZE = 15

# -------------------------------------------------------- generate random villagers names

def getFirstNamelist():
    with open(VILLAGER_NAME_PATH + "villagerFirstNames.txt", "r") as f:
        # return the split results, which is all the words in the file.
        return f.read().replace("\n", "").split(";")

def getLastNamelist():
    with open(VILLAGER_NAME_PATH + "villagerLastNames.txt", "r") as f:
        # return the split results, which is all the words in the file.
        return f.read().replace("\n", "").split(";")

def getRandomVillagerNames(villagerNamesList, number):
    listOfRandomVillagers = []
    listOfVillagers = villagerNamesList
    for i in range(number):
        # get a random name from the list of names
        randomName = rd.choice(listOfVillagers)
        # add the random name to the list of random villagers
        listOfRandomVillagers.append(randomName)
        # delete the random name from the list of all villagers so we don't get the same name twice
        del listOfVillagers[listOfVillagers.index(randomName)]
    return listOfRandomVillagers


# -------------------------------------------------------- generate random village name
def initialize():
    with open (VILLAGER_NAME_PATH + "Lexique-query.tsv") as f:
        #Extract data
        dicto = pd.read_csv (f, sep = "\t")

        # Creation of the vector which contains all the words (delete missed values and duplicates)
        words = dicto.Word.dropna().unique()

        # Add the char ' ' at the end of words to mark the end
        for i in range(words.shape[0]):
            words[i] = words[i] + ' '

        # Cleaning de la data en remplacant les caractères spéciaux ou rares par des caractères plus communs
        # Cleaning of the data by replacing specials or rare chars by common chars
        clean_words = []
        for word in words:
            clean_word = word
            for letter in word:
                if letter == 'ã' or letter == 'â' or letter == 'à':
                    clean_word = clean_word.replace(letter, 'a')
                if letter == 'ï' or letter == 'î' or letter == 'ï':
                    clean_word = clean_word.replace(letter, 'i')
                if letter == 'û' or letter == 'ù' or letter == 'ü':
                    clean_word = clean_word.replace(letter, 'u')
                if letter == '-' or letter == '.':
                    clean_word = clean_word.replace(letter, '')
                if letter == 'ö' or letter == 'ô':
                    clean_word = clean_word.replace(letter, 'o')
                if letter == 'ñ':
                    clean_word = clean_word.replace(letter, 'n')
            clean_words.append(clean_word)
        #print(clean_words)



        # Creation of a list grouping all the used chars
        carac = set()
        for word in clean_words:
            for letter in word:
                carac.add(letter)
        carac = list(carac)
        last_ind = carac.index(' ')
        last_ind = np.array(last_ind, dtype=object)
        #print(carac)
        #print(last_ind)



        # Creation of a tensor of dimension 2, the rows and the columns represent the letters in the order of carac
        # At the intersection [i][j] is the number of times the letter in j is found after the letter in i
        arr1 = np.zeros([len(carac), len(carac)], dtype=object)
        for word in clean_words:
            for i in range(len(word) - 1):
                letter_index = carac.index(word[i])
                next_index = carac.index(word[i + 1])
                arr1[letter_index][next_index] += 1
        


        # Creation of a tensor of dimension 3, the rows and the columns represent the letters in the order of carac
        # At the intersection [i][j][k] is the number of times the letter in k is found after the letter in i and j
        arr2 = np.zeros([len(carac), len(carac), len(carac)], dtype=object)
        for word in clean_words:
            if len(word) > 2:
                for i in range(len(word) - 2):
                    letter_index = carac.index(word[i])
                    index_plus1 = carac.index(word[i + 1])
                    index_plus2 = carac.index(word[i + 2])
                    arr2[letter_index][index_plus1][index_plus2] += 1
        

        # Modification of arr1 by dividing each entry by the sum of the line
        # to have a vlaue of sum of 1
        i = 0
        arr_last1 = []
        for row in arr1:
            arr_temp = []
            summ = sum(row)
            if summ != 0:
                for item in row:
                    arr_temp.append(item/summ)
                arr_last1.append(arr_temp)
            else:
                arr_last1.append(row)
        arr_last1 = np.array(arr_last1, dtype=object)


        # Modification of arr2 by dividing each entry by the sum of the line
        # to have a vlaue of sum of 1
        i = 0
        arr_last2 = []
        for col in arr2:
            arr_temp2 = []
            for row in col:
                arr_temp1 = []
                summ = sum(row)
                if summ != 0:
                    for item in row:
                        arr_temp1.append(item/summ)
                    arr_temp2.append(arr_temp1)
                else:
                    arr_temp2.append(row)
            arr_last2.append(arr_temp2)
        arr_last2 = np.array(arr_last2, dtype=object)
        #print(arr_last2[0][2])
        #print(arr2[0][2])

        # Creation of two lists which regroup the cumulated probs of letters and their index in carac for vision 1
        arr_cum1 = []
        arr_ind1 = []
        for i, row in enumerate(arr_last1):
            arr_ind_temp = []
            arr_cum_temp = []
            summ = 0
            for j, item in enumerate(row):
                if item > 0:
                    summ += item
                    arr_ind_temp.append(j)
                    arr_cum_temp.append(summ)
            arr_ind1.append(arr_ind_temp)
            arr_cum1.append(arr_cum_temp)
        arr_cum1 = np.array(arr_cum1, dtype=object)
        arr_ind1 = np.array(arr_ind1, dtype=object)
        #print(arr_ind1)
        #print(arr_cum1)

        # Creation of two matrices which regroup the cumuluated probs of letter and their index in carac by vision 2
        arr_cum2 = []
        arr_ind2 = []
        for i, col in enumerate(arr_last2):
            arr_ind_temp2 = []
            arr_cum_temp2 = []
            for j, row in enumerate(col):
                arr_ind_temp1 = []
                arr_cum_temp1 = []
                summ = 0
                for k, item in enumerate(row):
                    if item > 0:
                        summ += item
                        arr_ind_temp1.append(k)
                        arr_cum_temp1.append(summ)
                arr_ind_temp2.append(arr_ind_temp1)
                arr_cum_temp2.append(arr_cum_temp1)
            arr_ind2.append(arr_ind_temp2)
            arr_cum2.append(arr_cum_temp2)
        arr_cum2 = np.array(arr_cum2, dtype=object)
        arr_ind2 = np.array(arr_ind2, dtype=object)
        #print(arr_ind2)
        #print(arr_cum2)

        # Creation of a list of charac by which a word start
        arr_temp = np.zeros([len(carac)])
        for word in clean_words:
            index = carac.index(word[0])
            arr_temp[index] += 1
        arr_deb = arr_temp/sum(arr_temp)

        arr_ind_pre = [] 
        arr_cum_pre = []
        summ = 0
        for i, el in enumerate(arr_deb):
            if el != 0:
                summ += el
                arr_ind_pre.append(i)
                arr_cum_pre.append(summ)
        arr_cum_pre = np.array(arr_cum_pre, dtype=object)
        arr_ind_pre = np.array(arr_ind_pre, dtype=object)
        f.close()   
        return arr_cum_pre, arr_ind_pre, carac, arr_cum1, arr_ind1, arr_cum2, arr_ind2, last_ind


# Generation of random name
def generateVillageName():
    arr_cum_pre, arr_ind_pre, carac, arr_cum1, arr_ind1, arr_cum2, arr_ind2, last_ind = initialize()
    word = []
    # Generation of first letter
    random = rd.random()
    for i, car in enumerate(arr_cum_pre):
        if random <= car:
            seed = arr_ind_pre[i]
            break
    word.append(carac[seed])

    # Generation of second letter
    random = rd.random()
    for i, car in enumerate(arr_cum1[seed]):
        if random <= car:
            seed = arr_ind1[seed][i]
            break

    # Generation of following letters
    cond = True
    while cond:
        word.append(carac[seed])
        previous_letter1 = carac.index(word[-1])
        previous_letter2 = carac.index(word[-2])
        random = rd.random()
        for i, car in enumerate(arr_cum2[previous_letter2][previous_letter1]):
            if random <= car:
                seed = arr_ind2[previous_letter2][previous_letter1][i]
                break
        if seed == last_ind:
            cond = False
    name = ""
    for let in word:
        if let != '':
            name += let
    if len(name) > MIN_SIZE and len(name) < MAX_SIZE:
        return name
    else:
        return generateVillageName()
        # print(let, end ='')
    # print("\n")
    # return name


def spawnVillager(x, y, z, entity, name, profession, level, type):
    command = "summon " + entity + " " + str(x) + " " + str(y) + " " + str(z) + " "
    command += "{VillagerData:{profession:" + profession + ",level:" + str(level) + ",type:" + type + "},CustomName:""\"\\" + '"' + str(name) + "\\" +'""' + "}"

    interfaceUtils.runCommand(command)
    
# Add items to a chest
# Items is a list of [item string, item quantity]
def addItemChest(x, y, z, items):
    for id,v in enumerate(items):
        command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                               "container."+str(id),
                                                               v[0],
                                                               v[1])
        interfaceUtils.runCommand(command)

def getHighestNonAirBlock(cx, cy, cz):
    cy = 255
    IGNORED_BLOCKS = [
        'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:lava',
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves', 'minecraft:dark_oak_leaves'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow', 'minecraft:poppy', 'minecraft:pissenlit', 'minecraft:seagrass' , 'minecraft:dandelion' ,'minecraft:blue_orchid',
        'minecraft:allium', 'minecraft:azure_bluet', 'minecraft:red_tulip', 'minecraft:orange_tulip', 'minecraft:white_tulip', 'minecraft:pink_tulip',
        'minecraft:oxeye_daisy', 'minecraft:cornflower', 'minecraft:lily_of_the_valley', 'minecraft:brown_mushroom', 'minecraft:red_mushroom',
        'minecraft:sunflower', 'minecraft:peony', 'minecraft:dead_bush', "minecraft:cactus", "minecraft:sugar_cane", 'minecraft:fern']
    ## Find highest non-air block
    while interfaceUtils.getBlock(cx, cy, cz) in IGNORED_BLOCKS:
        cy -= 1
    return cy

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
            bookpage += line + "\\\\n"
        bookpage += "\"}',"
        booktext += bookpage

    booktext = booktext + "],"

    booktitle = "title:\""+title+"\","
    bookauthor = "author:\""+author+"\","
    bookdesc = "display:{Lore:[\""+desc+"\"]}"
    return "written_book{"+booktext+booktitle+bookauthor+bookdesc+"}"

def strToDictBlock(block):
    expended = {}
    parts = block.split["["]
    expended["Name"] = parts[0]
    expended["Properties"] = {}

    if len(parts) > 1:
        subParts = parts[1].split(",")
        for i in subParts:
            subsubParts = i.split("=")
            expended["Properties"][subsubParts[0]] = subsubParts[1]

    return expended

def compareTwoDictBlock(a, b):
    if a["Name"] != b["Name"]:
        return False
    if len(a.keys()) != len(b.keys()):
        return False

    for key in a.keys() :
        if not b.keys().contains(key):
            return False
        
        if a[key] != b[key]:
            return False

    return True
