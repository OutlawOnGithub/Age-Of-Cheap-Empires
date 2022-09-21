from entities.buildings.enemybuilding import EnemyBuilding


class EnemyStable(EnemyBuilding):
    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, 500, map) # hp_max = 500
        self.name = "EnemyStable"
        self.lore = " : Trains your horsemen"
        self.hp = self.age*0.75*500
        self.maxhp = self.age*0.75*500
        self.fieldofview = 5
        self.resource_manager.EN_apply_cost_to_resource(self.name)
        
