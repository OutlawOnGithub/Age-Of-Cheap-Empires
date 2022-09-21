from entities.buildings.building import Building


class Sawmill(Building):

    def __init__(self, pos, resource_manager, map):
        super().__init__(pos, resource_manager, 350, map) # hp_max = 350
        self.name = "Sawmill"
        self.lore = " : Generates Wood over time."
        self.hp = self.age*0.75*350
        self.maxhp = self.age*0.75*350
        self.fieldofview = 3
        self.resource_manager.apply_cost_to_resource(self.name)
        
