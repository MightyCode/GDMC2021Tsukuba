import json
import random
import _utils

class StructureManager:
    PATH = "data/structures/dependencies.json"


    def __init__(self, settlementData, resources):
        with open(StructureManager.PATH) as json_file:
           self.dependencies = json.load(json_file)
        self.settlementData = settlementData
        self.resources = resources

        self.numberOfStructuresForEachGroup = {}
        for group in self.dependencies.keys():
            self.numberOfStructuresForEachGroup[group] = 0

        self.villagerFirstNamesList = _utils.getFirstNamelist()
        self.villagerLastNamesList = _utils.getLastNamelist()

        self.checkDependencies()

    """
    Set the name of the last append structure in the table, attribute villager to it too if needed
    """
    def chooseOneStructure(self):
        sumWeight = 0
        for structure in self.allStructures :
            sumWeight += structure["weight"]

        randomValue = random.randint(0, sumWeight)

        for structure in self.allStructures :
            randomValue -= structure["weight"]
            if randomValue <= 0:
                self.choosedStructure(structure)
                break


    def choosedStructure(self, structure):
        self.settlementData["structures"][-1]["name"] = structure["name"]
        self.settlementData["structures"][-1]["type"] = structure["type"]
        
        self.numberOfStructuresForEachGroup[structure["group"]] += 1

        if structure["type"] == "houses":
            numberToAdd = self.resources.buildings[structure["name"]].info["villageInfo"]["villager"]
            self.settlementData["structures"][-1]["villagersId"] = []
            size = len(self.settlementData["villagerNames"])
            for i in range(numberToAdd):
                self.settlementData["villagerNames"].append(
                            _utils.getRandomVillagerNames(self.villagerFirstNamesList, 1)[0]
                            + _utils.getRandomVillagerNames(self.villagerLastNamesList, 1)[0]
                )
                self.settlementData["structures"][-1]["villagersId"].append(size + i)
            self.settlementData["freeVillager"] += numberToAdd


    def chooseOneHouse(self):
        pass
    def chooseOneFunctional(self):
        pass
    def chooseOneRepresentatives(self):
        pass


    def checkDependencies(self):
        # Make arrays empty
        self.houses = []
        self.functionals = []
        self.reprentatives = []
        self.allStructures = []

        # For each node of our structures tree
        for group in self.dependencies.keys():
            # Check if the group can be add
            conditions = True
            for condition in self.dependencies[group]["conditions"] :

                if not self.checkOneCondition(condition, self.dependencies[group]["conditions"][condition]):
                    # Go to the next group
                    conditions = False
                    break

            if not conditions:
                continue
            
            # Add all the structure of this group
            for structure in self.dependencies[group]["structures"]:
                data = { "name" : structure, "group" : group, "type" : self.dependencies[group]["type"], "weight" : 1 }

                if data["type"] == "houses" :
                    self.houses.append(data)
                elif data["type"] == "functionals" : 
                    self.functionals.append(data)
                elif data["type"] == "reprentatives" : 
                    self.reprentatives.append(data)
                self.allStructures.append(data)


    def checkOneCondition(self, name, conditionValues):
        valueToCheck = 0

        if name == "villagerNeeded" :
            valueToCheck =  self.settlementData["freeVillager"]
        # Ex : dirtResources, woordResources
        elif "Resources" in name:
            valueToCheck =  self.settlementData[name]
        elif name == "previous":
            valueToCheck = self.numberOfStructuresForEachGroup[conditionValues["name"]]


        if "min" in conditionValues:
            if valueToCheck < conditionValues["min"] :
                return False
        
        if "max" in conditionValues : 
            if valueToCheck > conditionValues["max"] :
                return False

        return True

