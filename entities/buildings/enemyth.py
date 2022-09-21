from entities.buildings.enemybuilding import EnemyBuilding


class EnemyTH(EnemyBuilding):

    def __init__(self, pos, resource_manager):
        super().__init__(pos, resource_manager, 1500) # hp_max = 1500
        self.name = "EnemyTownHall"
        self.lore = " : The main building of the enemy's city."
        self.hp = self.age*0.75*1500
        self.maxhp = self.age*0.75*1500
    
    def update(self):
        pass