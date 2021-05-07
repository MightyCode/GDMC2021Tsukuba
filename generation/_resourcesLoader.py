from generation.structures.generated.generatedQuarry import * 

def loadAllResources(resources) : 
    # Loads structures

    resources.loadStructures("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
    resources.loadStructures("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
    resources.loadStructures("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
    resources.loadStructures("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

    resources.loadStructures("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
    resources.loadStructures("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
    resources.loadStructures("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse2.json", "mediumhouse2")
    resources.loadStructures("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1")

    resources.loadStructures("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json", "mediumwindmill")
    resources.loadStructures("functionals/lumberjachut/basiclumberjachut.nbt", "functionals/lumberjachut/basiclumberjachut.json", "basiclumberjachut")
    resources.loadStructures("functionals/farm/basicfarm.nbt", "functionals/farm/basicfarm.json", "basicfarm")

    resources.addGeneratedStructures(GeneratedQuarry(),  "functionals/quarry/basicgeneratedquarry.json", "basicGeneratedQuarry")

    # Load lootTable
    resources.loadLootTable("functionals/windmill.json", "windmill")
    resources.loadLootTable("functionals/basiclumberjachut.json", "basiclumberjachut")
    resources.loadLootTable("functionals/basicfarm.json", "basicfarm")