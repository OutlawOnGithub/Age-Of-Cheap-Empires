from .unit import *

class Bowman(Unit):

    def __init__(self,tile, map, resource_manager):
        super().__init__(tile, map, 30, resource_manager) # hp_max = 30
        image = pg.image.load("assets/graphics/bowman.png").convert_alpha()
        self.name = "bowman"
        self.image = pg.transform.scale(image, (image.get_width(), image.get_height()))

        self.fieldofview = 4
        self.movingspeed = self.age*0.75*8
        self.hp = self.age*0.75*30
        self.maxhp = self.age*0.75*30
        self.atkdmg = self.age*0.75*15

        self.resource_manager.apply_cost_to_resource_troop(self.name)



    def is_at_range(self,tile):
        return True if (abs(self.tile["grid"][0]-tile["grid"][0])+abs(self.tile["grid"][1]-tile["grid"][1]))<5 \
            else False

    def go_at_range(self,tile,axis1=[-2, -1, 0, 1, 2]):
        temp_dist=500
        end_tile=None
        for temp_tile in [self.map.map[tile["grid"][0]+x][tile["grid"][1]+y] for x in axis1 for y in axis1 if (abs(x)+abs(y)>=max(axis1) and
        0<tile["grid"][0]+x<WORLD_SIZE and 0<tile["grid"][1]+y<WORLD_SIZE)]:
            if 0<=temp_tile["grid"][1]<WORLD_SIZE and 0<=temp_tile["grid"][0]<WORLD_SIZE:
                if not (self.map.map[temp_tile["grid"][0]][temp_tile["grid"][1]]["collision"] \
                or self.map.map[temp_tile["grid"][0]][temp_tile["grid"][1]]["water"] or self.map.map[temp_tile["grid"][0]][temp_tile["grid"][1]]["troop"]):
                    self.set_destination(temp_tile)
                    self.create_path()
                    if self.runs<temp_dist:
                        temp_dist=self.runs
                        end_tile=temp_tile
        if end_tile :
            self.set_destination(end_tile)
            self.create_path()

    def attack(self, unit):
        self.attacked_unit = unit
        self.temp_atk_unit = self.attacked_unit
        if self.is_at_range(unit.tile):
            unit.hp -= self.atkdmg
        else: self.go_at_range(unit.tile)
        if unit.hp<=0:
            self.attacked_unit.die()
            self.attacked_unit = None

    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > self.map.GAME_SPEED:
            # attacking
            if self.attacked_unit: self.attack(self.attacked_unit)
            elif self.temp_atk_unit:
                if self.is_at_range(self.temp_atk_unit.tile): self.attack(self.temp_atk_unit)
            
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
