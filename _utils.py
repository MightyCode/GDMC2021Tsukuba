import random as rd
import math
import pandas as pd
import numpy as np


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
        dicto = pd.read_csv (f, sep = "\t")

        #Extract data
        # dicto = pd.read_csv( VILLAGER_NAME_PATH + "Lexique-query.tsv", sep ="\t")

        # Creation of the vector which contains all the words (delete missed values and duplicates)
        words = dicto.Word.dropna().unique()

        # Ajout du caractère ' ' à la fin des mots pour marquer la fin
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
        #print(carac)
        #print(last_ind)



        # Creation of a tensor of dimension 2, the rows and the columns represent the letters in the order of carac
        # At the intersection [i] [j] is the number of times the letter in j is found after the letter in i
        arr1 = np.zeros([len(carac), len(carac)])
        for word in clean_words:
            for i in range(len(word) - 1):
                letter_index = carac.index(word[i])
                next_index = carac.index(word[i + 1])
                arr1[letter_index][next_index] += 1


        # Creation of a tensor of dimension 3, the rows and the columns represent the letters in the order of carac
        # At the intersection [i][j][k] is the number of times the letter in k is found after the letter in i and j
        arr2 = np.zeros([len(carac), len(carac), len(carac)])
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
        arr_last1 = np.array(arr_last1)

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
        arr_last2 = np.array(arr_last2)
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
        #print(arr_deb)
        #print(arr_cum_pre)
        #print(arr_ind_pre)
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



def strToDictBlock(block) :
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


def convertNbtBlockToStr(blockPalette, rotation, flip):
    block = blockPalette["Name"].value + "["

    if "Properties" in blockPalette.keys():
        for key in blockPalette["Properties"].keys():
            block += self.convertProperty(key, blockPalette["Properties"][key].value, rotation, flip) + ","
  
        block = block[:-1] 
    block += "]"
    return block


def compareTwoDictBlock(a, b):
    if a["Name"] != b["Name"]:
        return false
    
    if len(a.keys()) != len(b.keys()):
        return false

    for key in a.keys() :
        if not b.keys().contains(key):
            return False
        
        if a[key] != b[key]:
            return False

    return true
