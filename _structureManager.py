import json

class StructureManager:
    PATH = "data/structures/dependencies.json"

    def __init__(self, settlementData, resources):
        with open(StructureManager.PATH) as json_file:
           self.dependencies = json.load(json_file)
        self.settlementData = settlementData
        self.resources = resources
        self.settlementData["freeVillager"] = 0

        self.numberOfStructuresForEachGroup = {}
        for group in self.dependencies.keys():
            self.numberOfStructuresForEachGroup[group] = 0

        self.checkDependencies()

    """
    Set the name of the last append structure in the table, attribute villager to it too if needed
    """
    def chooseOneStructure(self):
        pass


    def checkDependencies(self):
        # Make arrays empty
        self.houses = []
        self.functionals = []
        self.reprentatives = []

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
                data = { "name" : structure, "group" : group }

                if self.dependencies[group]["type"] == "houses" :
                    self.houses.append(data)
                elif self.dependencies[group]["type"] == "functionals" : 
                    self.functionals.append(data)
                elif self.dependencies[group]["type"] == "reprentatives" : 
                    self.reprentatives.append(data)


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

