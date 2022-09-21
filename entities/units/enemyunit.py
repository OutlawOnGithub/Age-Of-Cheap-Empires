import pygame as pg
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from jeu.map import *
from utils.settings import WORLD_SIZE


class EnemyUnit:

    def __init__(self, tile, map, hp_max, resource_manager, team=2):
        self.map = map
        self.is_dead = False
        self.map.entities.append(self)
        self.tile = tile
        self.destx=self.map.map[tile["grid"][0]]
        self.desty=self.map.map[tile["grid"][1]]

        self.age = 1

        self.temp_atk_unit = None
        self.attacked_unit = None
        self.attacked_building = None
        self.temp_atk_building = None
        self.team=team
        self.hp_max = hp_max

        self.resource_manager = resource_manager

        #pathfinding

        self.map.workers[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()
        self.create_path()

    def set_destination(self,tile):
        self.map.map[self.destx[0]["grid"][0]][self.desty[0]["grid"][0]]["troop"] = False
        self.destx=self.map.map[tile["grid"][0]]
        self.desty=self.map.map[tile["grid"][1]]


    def create_path(self):  # permet la creation d'un chemin qui prend en compte les obstacles + fait déplacer aux coordonnées x et y
        searching_for_path = True
        self.attacked_unit = None
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


    def change_tile(self, new_tile):
        self.map.workers[self.tile["grid"][0]][self.tile["grid"][1]] = None # Delete the worker from the tile's workers list
        self.map.map[self.tile["grid"][0]][self.tile["grid"][1]]["troop"] = False # Troop no more here
        self.map.mixed_matrix[self.tile["grid"][1]][self.tile["grid"][0]] = 1 # No more collision
    
        self.map.workers[new_tile[0]][new_tile[1]] = self  # new position where the worker will move
        self.tile = self.map.map[new_tile[0]][new_tile[1]] # updating self.tile
        self.map.map[self.tile["grid"][0]][self.tile["grid"][1]]["troop"] = True # There's a troop here
        self.map.mixed_matrix[self.tile["grid"][1]][self.tile["grid"][0]] = 0 # Collision here
    
    def attack(self, unit):
        self.temp_mine_tile = None
        self.attacked_unit = unit
        self.temp_atk_unit = self.attacked_unit
        if self.is_close(unit.tile) and self.team != unit.team:
            unit.hp -= self.atkdmg
        if unit.hp<=0:
            self.attacked_unit.die()
            self.attacked_unit = None            
        else: self.go_close(unit.tile) 
    
    def attack_building(self, building):
        self.temp_mine_tile = None
        self.temp_building = None
        self.temp_atk_unit = None
        self.attacked_building = building
        self.temp_atk_building = self.attacked_building
        if (abs(self.tile["grid"][0]-building.pos[0])<2 and abs(self.tile["grid"][1]-building.pos[1])<2):
            building.hp -= self.atkdmg
        else: 
            self.go_close(self.map.map[building.pos[0]][building.pos[1]])
        if building.hp<=0:
            if isinstance(building,EnemyTH) or isinstance(building,GoodTH):
                return 
            self.attacked_building.die()
            self.attacked_building = None 
            self.temp_atk_building = None
    
    def die(self):
        self.map.map[self.tile["grid"][0]][self.tile["grid"][1]]["troop"] = False
        self.map.workers[self.tile["grid"][0]][self.tile["grid"][1]]=None
        self.map.mixed_matrix[self.tile["grid"][1]][self.tile["grid"][0]] = 1
        if self in self.map.entities:
            self.map.entities.remove(self)
        if self in self.map.entities:
            self.map.workers.remove(self)
        self.is_dead = True  

    def is_close(self,tile):
        return True if (abs(self.tile["grid"][0]-tile["grid"][0])<2 and abs(self.tile["grid"][1]-tile["grid"][1])<2) \
            else False

    def go_close(self,tile,axis1=[-1,0,1]):
        
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
        else:
            axis1.extend([max(axis1)+1,-max(axis1)-1])
            for temp_tile in [self.map.map[tile["grid"][0]+x][tile["grid"][1]+y] for x in axis1 for y in axis1 if abs(x)+abs(y)>=max(axis1)]:
                self.go_close(tile,axis1)
        
               

    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > self.map.GAME_SPEED:
            # attacking
            if self.attacked_unit: self.attack(self.attacked_unit)
            elif self.temp_atk_unit:
                if self.is_close(self.temp_atk_unit.tile): self.attack(self.temp_atk_unit)
            
            # attacking buildings
            if self.attacked_building: self.attack_building(self.attacked_building)
            elif self.temp_atk_building and self.is_close(self.map.map[self.temp_atk_building.pos[0]][self.temp_atk_building.pos[1]]): 
                self.attack_building(self.temp_atk_building)
            
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
        #self.map.update_vision_matrix((self.tile["grid"][0],self.tile["grid"][1]),self.fieldofview)
