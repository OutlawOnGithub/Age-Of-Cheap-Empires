from entities.buildings.building import Building


class Armory(Building):
    def __init__(self, pos, resource_manager, map, hud):
        super().__init__(pos, resource_manager, 700, map, hud) # hp_max = 700
        self.name = "Armory"
        self.lore = " : Research and Developpement"
        self.hp = self.age*0.75*700
        self.maxhp = self.age*0.75*700
        self.fieldofview = 5
        
        self.resource_manager.apply_cost_to_resource(self.name)
        