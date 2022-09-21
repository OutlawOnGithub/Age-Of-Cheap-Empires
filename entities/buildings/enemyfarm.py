from entities.buildings.enemybuilding import EnemyBuilding


class EnemyFarm(EnemyBuilding) :

    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, 350, map) # hp_max = 350
        self.name = "Enemy Farm"
        self.lore = " : Generates Food over time."
        self.hp = self.age*0.75*350
        self.maxhp = self.age*0.75*350
        self.fieldofview = 3
        self.resource_manager.EN_apply_cost_to_resource(self.name)
        
