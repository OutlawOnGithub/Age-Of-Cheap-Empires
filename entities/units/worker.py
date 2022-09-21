from .unit import *

class Worker(Unit):

    def __init__(self, tile, map, resource_manager):
        super().__init__(tile, map, 20, resource_manager) # hp_max = 20
        image = pg.image.load("assets/graphics/worker.png").convert_alpha()
        self.name = "worker"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 3
        self.movingspeed = self.age*0.75*5
        self.hp = self.age*0.75*20
        self.maxhp = self.age*0.75*20
        self.tile = tile
        self.atkdmg = self.age*0.75*2
        

        self.mine_tile = None
        self.temp_mine_tile = None
        self.building = None
        self.temp_building = None

        

    def create_path(self):  # permet la creation d'un chemin qui prend en compte les obstacles + fait déplacer aux coordonnées x et y
        searching_for_path = True
        self.mine_tile = None
        self.attacked_unit = None
        self.building = None
        self.attacked_building = None

        while searching_for_path:

            dictx = self.destx[0] # a remplacer par la coordonnée de la case de destination souhaité,grid_pos présent dans map(grid_pos[0]) qui correspond a la case sur laquelle la souris est + condition clique bouton souris(simple)
            dicty = self.desty[0] # a remplacer par la coordonnée de la case souhaité grid_pos présent dans map(grid_pos[1])
            x = dictx["grid"][0]
            y = dicty["grid"][0]

            dest_tile = self.map.map[x][y]
            if not (dest_tile["collision"] or dest_tile["water"]): # valid destination
                self.grid = Grid(matrix=self.map.mixed_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                # To mention that there will be a troop on this tile (to prevent from placing a building here)
                dest_tile["troop"] = True
                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                self.path_index = 0
                self.path, self.runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def mine(self, tile):
        self.temp_atk_unit = None
        self.temp_building = None
        self.temp_atk_building = None
        self.mine_tile = tile
        self.temp_mine_tile = self.mine_tile
        if self.is_close(self.map.map[tile["grid"][0]][tile["grid"][1]]):
            if tile["collision"]:
                self.map.resource_manager.resources[self.map.map[tile["grid"][0]][tile["grid"][1]]["tile"]] += 50
                self.map.map[tile["grid"][0]][tile["grid"][1]]["resources"] -= 50
            if self.map.map[tile["grid"][0]][tile["grid"][1]]["resources"] == 0:
                self.map.map[tile["grid"][0]][tile["grid"][1]]["tile"] = ""
                self.map.map[tile["grid"][0]][tile["grid"][1]]["collision"] = False
                self.map.mixed_matrix[tile["grid"][1]][tile["grid"][0]] = 1
                self.mine_tile = None
        else: 
            self.go_close(self.map.map[tile["grid"][0]][tile["grid"][1]])
    
    def build(self, building):
        self.temp_atk_unit = None
        self.mine_tile = None
        if (abs(self.tile["grid"][0]-building.pos[0])<2 and abs(self.tile["grid"][1]-building.pos[1])<2):
            building.construct = True
            if not building.in_construction: 
                self.building = None
                self.temp_building = None
        else: 
            self.go_close(self.map.map[building.pos[0]][building.pos[1]])
            self.temp_building = building


    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > self.map.GAME_SPEED:
            # mining
            if self.mine_tile: self.mine(self.mine_tile)
            elif self.temp_mine_tile and self.is_close(self.temp_mine_tile): self.mine(self.temp_mine_tile)
                
            # attacking
            if self.attacked_unit: self.attack(self.attacked_unit)
            elif self.temp_atk_unit and self.is_close(self.temp_atk_unit.tile): self.attack(self.temp_atk_unit)

            # attacking buildings
            if self.attacked_building: self.attack_building(self.attacked_building)
            elif self.temp_atk_building and self.is_close(self.map.map[self.temp_atk_building.pos[0]][self.temp_atk_building.pos[1]]): 
                self.attack_building(self.temp_atk_building)

            # building
            if self.building: self.build(self.building)
            elif self.temp_building and self.is_close(self.map.map[self.temp_building.pos[0]][self.temp_building.pos[1]]): self.build(self.temp_building)

            # moving
            if self.path_index>=len(self.path):
                self.go_close(self.map.map[self.destx[0]["grid"][0]][self.desty[0]["grid"][0]])
            new_pos = self.path[self.path_index]
            self.change_tile(new_pos)
            if self.path_index<len(self.path)-1: 
                self.create_path()
                self.path_index += 1
            self.move_timer = now
            if self.path_index == len(self.path):
                self.create_path()
        self.map.update_vision_matrix((self.tile["grid"][0],self.tile["grid"][1]),self.fieldofview)

class Herobrine(Worker):
    def __init__(self, tile, map, resource_manager):
        super().__init__(tile, map, resource_manager)
        image = pg.image.load("assets/graphics/herobrine.png").convert_alpha()
        self.name = "herobrine"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 10
        self.movingspeed = 5
        self.hp = 999
        self.maxhp = 999
        self.atkdmg = 100
        self.tile = tile
        

        self.mine_tile = None
        self.temp_mine_tile = None
        self.building = None
        self.temp_building = None

        self.resource_manager.apply_cost_to_resource_troop(self.name)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > self.map.GAME_SPEED/2:
            # mining
            if self.mine_tile: self.mine(self.mine_tile)
            elif self.temp_mine_tile and self.is_close(self.temp_mine_tile): self.mine(self.temp_mine_tile)
                
            # attacking
            if self.attacked_unit: self.attack(self.attacked_unit)
            elif self.temp_atk_unit and self.is_close(self.temp_atk_unit.tile): self.attack(self.temp_atk_unit)

            # attacking buildings
            if self.attacked_building: self.attack_building(self.attacked_building)
            elif self.temp_atk_building and self.is_close(self.map.map[self.temp_atk_building.pos[0]][self.temp_atk_building.pos[1]]): 
                self.attack_building(self.temp_atk_building)

            # building
            if self.building: self.build(self.building)
            elif self.temp_building and self.is_close(self.map.map[self.temp_building.pos[0]][self.temp_building.pos[1]]): self.build(self.temp_building)

            # moving
            if self.path_index>=len(self.path):
                self.go_close(self.map.map[self.destx[0]["grid"][0]][self.desty[0]["grid"][0]])
            new_pos = self.path[self.path_index]
            self.change_tile(new_pos)
            if self.path_index<len(self.path)-1: 
                self.create_path()
                self.path_index += 1
            self.move_timer = now
            if self.path_index == len(self.path):
                self.create_path()
        self.map.update_vision_matrix((self.tile["grid"][0],self.tile["grid"][1]),self.fieldofview)



        
