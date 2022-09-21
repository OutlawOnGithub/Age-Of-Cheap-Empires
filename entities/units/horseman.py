from .unit import *

class Horseman(Unit):

    def __init__(self,tile, map, resource_manager):
        super().__init__(tile, map, 50, resource_manager) # hp_max = 50
        image = pg.image.load("assets/graphics/horseman.png").convert_alpha()
        self.name = "horseman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))
        
        self.fieldofview = 5
        self.movingspeed = self.age*0.75*12
        self.hp = self.age*0.75*50
        self.maxhp = self.age*0.75*50
        self.atkdmg = self.age*0.75*25

        self.resource_manager.apply_cost_to_resource_troop(self.name)
        
