from .enemyunit import *

class EnemyBowman(EnemyUnit):

    def __init__(self,tile, map, resource_manager):
        super().__init__(tile, map, 30, resource_manager) # hp_max = 30
        image = pg.image.load("assets/graphics/enemy_bowman.png").convert_alpha()
        self.name = "enemy bowman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 4
        self.movingspeed = self.age*0.75*8
        self.hp = self.age*0.75*30
        self.maxhp = self.age*0.75*30
        self.atkdmg = self.age*0.75*15

        self.resource_manager.EN_apply_cost_to_resource_troop(self.name)
        
