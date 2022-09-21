import pygame as pg

class EnemyBuilding:
    def __init__(self, pos, resource_manager, hp_max, map=None, team=2):
        self.is_dead = False
        self.team = team
        self.pos = pos
        self.resource_manager = resource_manager
        self.hp_max = hp_max
        self.age = 1
        self.fieldofview = 5
        self.in_construction = False
        self.construct = False
        self.construc_cooldown = pg.time.get_ticks()
        self.construc_time = 3 # 3*game_speed
        if map:
            self.map = map
            self.map.update
            #self.update_vision_matrix = map.update_vision_matrix(self.pos, self.fieldofview)

    def die(self):
        self.map.map[self.pos[0]][self.pos[1]]["collision"] = False
        self.map.buildings[self.pos[0]][self.pos[1]] = None
        self.map.mixed_matrix[self.pos[1]][self.pos[0]] = 1
        if self in self.map.entities:
            self.map.entities.remove(self)
        if self in self.map.entities:
            self.map.buildings.remove(self)
        self.is_dead = True

    def update(self):
        now = pg.time.get_ticks()
        if self.in_construction :

            if now - self.construc_cooldown > self.construc_time*self.map.GAME_SPEED :

                #self.map.buildings[self.pos[0]][self.pos[1]] = self
                #self.update_vision_matrix
                self.in_construction = False

                self.construc_cooldown = now
