from .enemyunit import *


class EnemySwordman(EnemyUnit):

    def __init__(self,tile, map, resource_manager):
        super().__init__(tile, map, 60, resource_manager) # hp_max = 60
        image = pg.image.load("assets/graphics/enemy_diamond_swordman.png").convert_alpha()
        self.name = "enemy swordman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 4
        self.movingspeed = self.age*0.75*6
        self.hp = self.age*0.75*60
        self.maxhp = self.age*0.75*60
        self.atkdmg = self.age*0.75*20

        self.resource_manager.EN_apply_cost_to_resource_troop(self.name)
        
