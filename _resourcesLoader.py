def loadAllResources(resources) : 
    # Loads structures

    resources.loadBuildings("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
    resources.loadBuildings("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
    resources.loadBuildings("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
    resources.loadBuildings("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

    resources.loadBuildings("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
    resources.loadBuildings("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
    resources.loadBuildings("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse2.json", "mediumhouse2")
    resources.loadBuildings("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1")
    resources.loadBuildings("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json", "mediumwindmill")
    resources.loadBuildings("functionals/lumberjachut/basiclumberjachut.nbt", "functionals/lumberjachut/basiclumberjachut.json", "basiclumberjachut")

    # Load lootTable
    resources.loadLootTable("functionals/windmill.json", "windmill")
    resources.loadLootTable("functionals/basiclumberjachut.json", "basiclumberjachut")