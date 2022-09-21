from entities.buildings.building import Building


class Barrack(Building):
    def __init__(self, pos, resource_manager, map, hud):
        super().__init__(pos, resource_manager, 500, map, hud) # hp_max = 500
        self.name = "Barrack"
        self.lore = " : Trains your infantry"
        self.hp = self.age*0.75*500
        self.maxhp = self.age*0.75*500
        self.fieldofview = 5
        
        self.resource_manager.apply_cost_to_resource(self.name)
       
