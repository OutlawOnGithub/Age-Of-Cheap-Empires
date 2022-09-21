from entities.buildings.building import Building


class GoodTH(Building):

    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, 1500, map) # hp_max = 1500
        self.name = "Town Hall"
        self.lore = " : The main building of your new city."
        self.hp = self.age*0.75*1500
        self.maxhp = self.age*0.75*1500
        self.fieldofview = 10
        


    def update(self):
        pass