from entities.buildings.enemybuilding import EnemyBuilding


class EnemyArmory(EnemyBuilding):
    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, 700, map) # hp_max = 700
        self.name = "EnemyArmory"
        self.lore = " : Research and Developpement"
        self.hp = self.age*0.75*700
        self.maxhp = self.age*0.75*700
        self.fieldofview = 5
        self.resource_manager.EN_apply_cost_to_resource(self.name)
        
        
