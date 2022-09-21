from entities.buildings.enemybuilding import EnemyBuilding


class EnemyArchery_range(EnemyBuilding):
    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, 500, map) # hp_max = 500
        self.name = "EnemyArcheryRange"
        self.lore = " : Trains your bowmen"
        self.hp = self.age*0.75*500
        self.maxhp = self.age*0.75*500
        self.fieldofview = 5
        self.resource_manager.EN_apply_cost_to_resource(self.name)
        
