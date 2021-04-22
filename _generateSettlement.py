import random
import math

VILLAGER_NAME_PATH = "data/names/"
CONSONANTS = [chr(i+97) for i in range(26)] + ["", ""]
# I put those last two spaces in the consonants list so that the program can generate
# words with consecutive vowels
VOWELS = ["a", "e", "i", "o", "u"]

def get_name_list():
    with open(VILLAGER_NAME_PATH + "villagerNames.txt", "r") as f:
        # return the split results, which is all the words in the file.
        return f.read().split(";")

def getRandomVillagerNames(villagerNamesList, number):
    listOfRandomVillagers = []
    listOfVillagers = villagerNamesList
    for i in range(number):
        # get a random name from the list of names
        randomName = random.choice(listOfVillagers)
        # add the random name to the list of random villagers
        listOfRandomVillagers.append(randomName)
        # delete the random name from the list of all villagers so we don't get the same name twice
        del listOfVillagers[listOfVillagers.index(randomName)]
    return listOfRandomVillagers

def randVowel():
    letter = random.choice(VOWELS)
    return letter

def randCons():
    consonant = random.choice(CONSONANTS)
    return consonant

def getRandomWord():
    word = []
    randRange = random.randint(3,4)
    letter = randVowel()
    word = letter.upper()
    for i in range(randRange):
        letter = randVowel()
        word += letter
        letter = randCons()
        word += letter
    word = "".join(str(x) for x in word) #to convert the list to a string
    return word #returns a random word

villageData = {}
villagerNamesList = get_name_list()
villageData["villageName"] = getRandomWord()
villageData["villagerNames"] = getRandomVillagerNames(villagerNamesList, 15)
print("Here's a random village name: ")
print(getRandomWord())
print("Here's random villager names : ")
print(villageData["villagerNames"])
