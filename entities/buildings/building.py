import pygame as pg
from jeu.map import *

class Building:
    def __init__(self, pos, resource_manager, hp_max, map, hud=None, team=1):
        self.team = team
        self.pos = pos
        self.map = map
        self.age = self.map.allyage
        self.resource_manager = resource_manager
        self.hp_max = self.age*0.75*hp_max
        self.fieldofview = 5
        self.age = self.map.allyage
        self.in_construction = False
        self.construct = False
        self.construc_cooldown = pg.time.get_ticks()
        self.construc_time = 3 # 3*game_speed
        self.hud = hud
        if map:
            self.map = map
            self.update_vision_matrix = map.update_vision_matrix(self.pos, self.fieldofview)

    def die(self):
        self.map.map[self.pos[0]][self.pos[1]]["collision"] = False
        self.map.buildings[self.pos[0]][self.pos[1]] = None
        self.map.mixed_matrix[self.pos[1]][self.pos[0]] = 1
        if self in self.map.entities:
            self.map.entities.remove(self)
        if self in self.map.entities:
            self.map.buildings.remove(self)


    def update(self):
        now = pg.time.get_ticks()
        if self.in_construction:
            self.hud.creerworker = False
            self.hud.creerswordman = False
            self.hud.creerbowman = False
            self.hud.creerhorseman = False
            self.hud.ageup = False
        if self.in_construction and self.construct:
            if now - self.construc_cooldown > self.construc_time*self.map.GAME_SPEED :
                #self.map.buildings[self.pos[0]][self.pos[1]] = self
                self.in_construction = False
                self.construc_cooldown = now