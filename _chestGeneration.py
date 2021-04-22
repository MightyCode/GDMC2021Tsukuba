class ChestGeneration:
    def __init__(self, resources, interface):
        self.resources = resources
        self.interface = interface
    
    def generate(self, x, y, z, lootTableName):
        lootTable = self.resources.lootTables[lootTableName]