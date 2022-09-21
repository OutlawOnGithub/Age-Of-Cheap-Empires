import pygame
import time

from entities.buildings.enemybarrack import EnemyBarrack
from entities.buildings.enemyarchery_range import EnemyArchery_range
from entities.buildings.enemystable import EnemyStable
from entities.buildings.enemyarmory import EnemyArmory
from entities.buildings.enemyfarm import EnemyFarm

from jeu import map

from utils.util_functions import *
from entities.units.unit import Unit
from entities.units.swordman import Swordman
from entities.units.worker import Worker
from entities.units.enemyunit import EnemyUnit
from entities.units.enemyworker import EnemyWorker
from entities.units.enemyswordman import EnemySwordman
from entities.units.enemybowman import EnemyBowman
from entities.units.enemyhorseman import EnemyHorseman
from jeu.resource_manager import ResourceManager
from entities.buildings import Archery_range, Armory, Barrack, EnemyTH, Farm, GoodTH, Mason, Sawmill, Stable, Building
from . import resource_manager


class IA_class:
    def __init__(self, map, resource_manager):

        self.resource_manager = resource_manager
        self.map = map
        self.wood_to_mine = self.scanwood((self.map.enemy_TH_x, self.map.enemy_TH_y), 10)
        #print(self.wood_to_mine)
        self.wood_to_mine2 = self.wood_to_mine[:]

        self.food_to_mine = self.scanfood((self.map.enemy_TH_x, self.map.enemy_TH_y), 13)
        #print(self.food_to_mine)
        self.food_to_mine2 = self.food_to_mine[:]

        self.gold_to_mine = self.scangold((self.map.enemy_TH_x, self.map.enemy_TH_y), 20)
        #print(self.gold_to_mine)
        self.gold_to_mine2 = self.gold_to_mine[:]

        self.stone_to_mine = self.scanstone((self.map.enemy_TH_x, self.map.enemy_TH_y), 20)
        #print(self.stone_to_mine)
        self.stone_to_mine2 = self.stone_to_mine[:]

        self.IA_workers = []
        self.IA_buildings = []
        self.IA_attackers = []


        self.IA_allybuildings = []

        self.an_enemy = EnemyWorker(self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1], self.map, self.map.resource_manager)
        #self.an_enemy.team = 2
        self.IA_workers.append(self.an_enemy)
        self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1]["troop"] = True
        self.z = 1
        self.y = 0
        self.x = 1
    def update(self):

        b1 = False
        x1 = []
        y1 = 0
        b2 = False
        x2 = []
        y2 = 0
        b3 = False
        x3 = []
        y3 = 0
        b4 = False
        x4 = []
        y4 = 0


        for a in self.map.buildings:
            for b in a:
                if (isinstance(b, Building)):
                    if b.name != "Town Hall" and b.name != "Enemy Town Hall":

                        self.IA_allybuildings.append(b)

        self.ia_allyb = list(set(self.IA_allybuildings))
        self.ia_allz = self.ia_allyb[:]
        #print(ia_allz)

        enemypos = self.IA_workers[0].tile["grid"][0], self.IA_workers[0].tile["grid"][1]

        #print(self.map.map[37][39])

        # print(self.scanwood(enemypos,4))

        if (self.resource_manager.enemy_resources.get("wood") > 500 and self.resource_manager.enemy_resources.get("stone") > 300 and self.resource_manager.enemy_resources.get("gold") > 400 and len(self.IA_buildings) < 1 and self.map.map[enemypos[0]-1][enemypos[1]-1]["tile"] == ""):
            #print("test")

            nearenemypos = enemypos[0] - 1, enemypos[1] - 1

            self.ent = EnemyBarrack(nearenemypos, self.resource_manager, self.map)
            #print(self.ent)
            #print(nearenemypos)
            #print(self.map.map[enemypos[0] - 2][enemypos[1] - 2])
            self.map.entities.append(self.ent)
            self.IA_buildings.append(self.ent)
            self.ent.in_construction = True
            self.map.buildings[enemypos[0]-1][enemypos[1]-1] = self.ent
            self.map.map[enemypos[0] - 1][enemypos[1] - 1]["troop"] = True
            b1 = True
            x1.append(self.map.map[enemypos[0] - 1][enemypos[1] - 1])
            y1 = x1[0]


        if b1 == True:
            y1["troop"] = True



            #self.map.update_mixed_matrix(enemypos[0] - 1, enemypos[1] - 1, True, "Barrack")
            #print( self.map.buildings[enemypos[0]-2][enemypos[1]-2])
            #print(self.map.enemy_TH_x, self.map.enemy_TH_y)



            #self.resource_manager.enemy_resources["wood"] -= 5000
            #print(self.IA_buildings)


        if (self.resource_manager.enemy_resources.get("wood") > 200 and self.resource_manager.enemy_resources.get("stone") > 900 and self.resource_manager.enemy_resources.get("gold") > 5000 and len(self.IA_buildings) ==1 and len(self.IA_workers) >1):
            enemypos2 = self.IA_workers[1].tile["grid"][0], self.IA_workers[1].tile["grid"][1]
            nearenemypos2 = enemypos2[0] + 1, enemypos2[1] + 1
            if self.map.map[enemypos2[0] + 1][enemypos2[1] + 1]["tile"] == "":


                self.ent = EnemyArchery_range(nearenemypos2, self.resource_manager, self.map)
                #print(self.ent)


                self.map.entities.append(self.ent)
                self.IA_buildings.append(self.ent)
                self.ent.in_construction = True
                self.map.buildings[enemypos2[0] + 1][enemypos2[1] + 1] = self.ent
                self.map.map[enemypos2[0] + 1][enemypos2[1] + 1]["troop"] = True
                b2 = True
                x2.append(self.map.map[enemypos2[0] + 1][enemypos2[1] + 1])
                y2 = x2[0]
        if b2 == True:
            y2["troop"] = True







        if (self.resource_manager.enemy_resources.get("wood") > 500 and self.resource_manager.enemy_resources.get("stone") > 500 and self.resource_manager.enemy_resources.get("gold") > 2000 and len(self.IA_buildings) ==2 and len(self.IA_workers) >2):
            enemypos3 = self.IA_workers[2].tile["grid"][0], self.IA_workers[2].tile["grid"][1]
            nearenemypos3 = enemypos3[0] - 1, enemypos3[1] - 1
            if self.map.map[enemypos3[0] - 1][enemypos3[1] - 1]["tile"] == "":
                self.ent = EnemyStable(nearenemypos3, self.resource_manager, self.map)
                self.map.entities.append(self.ent)
                self.IA_buildings.append(self.ent)
                self.ent.in_construction = True
                self.map.buildings[enemypos3[0] - 1][enemypos3[1] - 1] = self.ent
                self.map.map[enemypos3[0] - 1][enemypos3[1] - 1]["troop"] = True

                b3 = True
                x3.append(self.map.map[enemypos3[0] - 1][enemypos3[1] - 1])
                y3 = x3[0]
        if b3 == True:
            y3["troop"] = True


        if (self.resource_manager.enemy_resources.get("wood") > 1000 and self.resource_manager.enemy_resources.get("stone") > 1000 and len(self.IA_buildings) ==3 and len(self.IA_workers) >3):

            enemypos4 = self.IA_workers[3].tile["grid"][0], self.IA_workers[3].tile["grid"][1]
            nearenemypos4 = enemypos4[0] - 1, enemypos4[1] - 1
            if self.map.map[enemypos4[0] - 1][enemypos4[1] - 1]["tile"] == "":
                self.ent = EnemyArmory(nearenemypos4, self.resource_manager, self.map)
                self.map.entities.append(self.ent)
                self.IA_buildings.append(self.ent)
                self.ent.in_construction = True
                self.map.buildings[enemypos4[0] - 1][enemypos4[1] - 1] = self.ent
                self.map.map[enemypos4[0] - 1][enemypos4[1] - 1]["troop"] = True
                b4 = True
                x4.append(self.map.map[enemypos4[0] - 1][enemypos4[1] - 1])
                y4 = x4[0]
        if b4 == True:
            y4["troop"] = True





        # Worker qui spawn quand assez de nourriture jusqu'a un max de 5 workers
        if (self.resource_manager.enemy_resources.get("food") > 1000 and len(self.IA_workers) < 4):
            #print(self.resource_manager.enemy_resources.get("food"))
            self.rodolphe = EnemyWorker(self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1], self.map, self.map.resource_manager)
            #self.rodolphe.team = 2
            self.IA_workers.append(self.rodolphe)
            # rodolphe.mine()
            # self.map.enemies.append(self.an_enemy)
            self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1]["troop"] = True

        if (self.resource_manager.enemy_resources.get("food") > 100 and self.resource_manager.enemy_resources.get("gold") > 150 and len(self.IA_buildings) >0 and len(self.IA_attackers) < 1):
            #print(self.resource_manager.enemy_resources.get("food"))

            self.vladimir = EnemySwordman(self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1], self.map, self.map.resource_manager)
            #print(self.vladimir)
            #self.rodolphe.team = 2
            self.IA_attackers.append(self.vladimir)
            # rodolphe.mine()
            # self.map.enemies.append(self.an_enemy)
            self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1]["troop"] = True
            self.x = 1
            self.y = 0


            #print(self.vladimir)
            #self.vladimir.attack_building(self.ia_allyb[0])

        #print(self.IA_allybuildings)
        #print("liste1",self.ia_allyb)
        #print("liste2",self.ia_allz)
        #print(self.ia_allyb)
        if len(self.ia_allyb)>0 and len(self.ia_allz)>0 and len(self.IA_attackers)>0 and self.x != 2:
            #print("testattaque")
            self.z = 1
            if (self.ia_allyb[0] == self.ia_allz[0]) :
            # print("test3")
            # print(self.IA_attackers[0])
            # print(self.ia_allyb[0])

                self.IA_attackers[0].attack_building(self.ia_allyb[0])
                if len(self.IA_attackers) > 1 and len(self.ia_allz)>1  :
                    self.ia_allyb[0]
                    self.IA_attackers[1].attack_building(self.ia_allyb[1])
                if len(self.IA_attackers) > 2 and len(self.ia_allz)>2:
                    self.IA_attackers[2].attack_building(self.ia_allyb[2])

                self.x = 2

                #print("avabt pop l2",self.ia_allz)
                #print("avant pop l1",self.ia_allyb)
                self.ia_allyb.pop(0)
                self.IA_allybuildings = []
                #print("apres pop l1",self.ia_allyb)

        if len(self.ia_allyb) > 0:
            if (self.map.map[self.ia_allz[0].pos[0]][self.ia_allz[0].pos[1]]["collision"] == False):
                    #print("test5")
                    self.ia_allz.pop(0)
                    self.x = 1
                    #print("apres pop l2",self.ia_allz)

        if len(self.IA_attackers) > 0 and self.y == 0 and len(self.ia_allz)==0:
            self.y = 1
            self.IA_attackers[0].attack_building(self.map.TH)
            if len(self.IA_attackers) > 1:
                self.IA_attackers[1].attack_building(self.map.TH)
                if len(self.IA_attackers) > 2:
                    self.IA_attackers[2].attack_building(self.map.TH)

        #print(self.IA_attackers)
        if len(self.IA_attackers)>0:


            for i in (self.IA_attackers):

                if i.is_dead:
                    self.IA_attackers.remove(i)
                    if i.name == "enemy swordman":
                        if (self.resource_manager.enemy_resources.get(
                                "food") > 100 and self.resource_manager.enemy_resources.get("gold") > 150 and len(
                            self.IA_buildings) > 0 and len(self.IA_attackers) < 3):
                            # print(self.resource_manager.enemy_resources.get("food"))

                            self.vladimir = EnemySwordman(
                                self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1],
                                self.map, self.map.resource_manager)
                            # print(self.vladimir)
                            # self.rodolphe.team = 2
                            self.IA_attackers.append(self.vladimir)
                            # rodolphe.mine()
                            # self.map.enemies.append(self.an_enemy)
                            self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1]["troop"] = True
                            self.x = 1
                            self.y = 0

                    elif i.name == "enemy bowman":
                        if (self.resource_manager.enemy_resources.get(
                                "food") > 100 and self.resource_manager.enemy_resources.get(
                                "gold") >150 and self.resource_manager.enemy_resources.get("wood") > 100 and len(
                                self.IA_buildings) > 1 and len(self.IA_attackers) < 2):
                            # print(self.resource_manager.enemy_resources.get("food"))
                            self.vladimir = EnemyBowman(self.map.map[self.map.enemy_TH_x][self.map.enemy_TH_y + 1],
                                                        self.map, self.map.resource_manager)

                            self.IA_attackers.append(self.vladimir)

                            self.map.map[self.map.enemy_TH_x][self.map.enemy_TH_y + 1]["troop"] = True
                            self.x = 1
                            self.y = 0

                    elif i.name == "enemy horseman":
                        if (self.resource_manager.enemy_resources.get(
                                "food") > 100 and self.resource_manager.enemy_resources.get("gold") > 300 and len(
                                self.IA_buildings) >= 3 and len(self.IA_attackers) < 3):
                            # print(self.resource_manager.enemy_resources.get("food"))
                            self.vladimir = EnemyHorseman(
                                self.map.map[self.map.enemy_TH_x + 1][self.map.enemy_TH_y + 1], self.map,
                                self.map.resource_manager)
                            # print(self.vladimir)
                            # self.rodolphe.team = 2
                            self.IA_attackers.append(self.vladimir)
                            # rodolphe.mine()
                            # self.map.enemies.append(self.an_enemy)
                            self.map.map[self.map.enemy_TH_x + 1][self.map.enemy_TH_y + 1]["troop"] = True
                            self.x = 1
                            self.y = 0























        






        if (self.resource_manager.enemy_resources.get("food") > 100 and self.resource_manager.enemy_resources.get("gold") > 100 and self.resource_manager.enemy_resources.get("wood") > 100 and len(self.IA_buildings) >1 and len(self.IA_attackers) < 2):
            #print(self.resource_manager.enemy_resources.get("food"))
            self.vladimir = EnemyBowman(self.map.map[self.map.enemy_TH_x ][self.map.enemy_TH_y + 1], self.map, self.map.resource_manager)
            #print(self.vladimir)
            #self.rodolphe.team = 2
            self.IA_attackers.append(self.vladimir)
            # rodolphe.mine()
            # self.map.enemies.append(self.an_enemy)
            self.map.map[self.map.enemy_TH_x ][self.map.enemy_TH_y + 1]["troop"] = True
            self.x = 1
            self.y = 0
            #self.IA_attackers[0].attack_building(self.ia_allyb[1])
            #self.IA_attackers[1].attack_building(self.ia_allyb[1])




        if (self.resource_manager.enemy_resources.get("food") > 100 and self.resource_manager.enemy_resources.get("gold") > 300  and len(self.IA_buildings) >=3 and len(self.IA_attackers) < 3):
            #print(self.resource_manager.enemy_resources.get("food"))
            self.vladimir = EnemyHorseman(self.map.map[self.map.enemy_TH_x+1][self.map.enemy_TH_y + 1], self.map, self.map.resource_manager)
            #print(self.vladimir)
            #self.rodolphe.team = 2
            self.IA_attackers.append(self.vladimir)
            # rodolphe.mine()
            # self.map.enemies.append(self.an_enemy)
            self.map.map[self.map.enemy_TH_x +1 ][self.map.enemy_TH_y + 1]["troop"] = True
            self.x = 1
            self.y = 0






        if (bool(self.IA_workers) and bool(self.food_to_mine) and bool(self.food_to_mine2)):

            if (self.food_to_mine[0] == self.food_to_mine2[0] and bool(self.food_to_mine) and bool(self.food_to_mine2)):

                self.IA_workers[0].mine(self.food_to_mine[0])
                self.food_to_mine.pop(0)
                #print(self.food_to_mine)

                # self.rodolphe.mine(self.wood_to_mine[0])

            if (self.food_to_mine2[0]["collision"] == False):
                self.food_to_mine2.pop(0)

        if (bool(self.IA_workers) and bool(self.wood_to_mine) and bool(self.wood_to_mine2) and len(self.IA_workers)>1):

            if (self.wood_to_mine[0] == self.wood_to_mine2[0]):


                self.IA_workers[1].mine(self.wood_to_mine[0])

                self.wood_to_mine.pop(0)
                #print(self.wood_to_mine)

                # self.rodolphe.mine(self.wood_to_mine[0])

            if (self.wood_to_mine2[0]["collision"] == False):
                self.wood_to_mine2.pop(0)

        if (bool(self.IA_workers) and bool(self.stone_to_mine) and bool(self.stone_to_mine2) and len(self.IA_workers) > 2):

            if (self.stone_to_mine[0] == self.stone_to_mine2[0]):
                self.IA_workers[2].mine(self.stone_to_mine[0])

                self.stone_to_mine.pop(0)
                #print(self.stone_to_mine)

                # self.rodolphe.mine(self.wood_to_mine[0])

            if (self.stone_to_mine2[0]["collision"] == False):
                self.stone_to_mine2.pop(0)

        if (bool(self.IA_workers) and bool(self.gold_to_mine) and bool(self.gold_to_mine2) and len(self.IA_workers) > 3):

            if (self.gold_to_mine[0] == self.gold_to_mine2[0]):
                self.IA_workers[3].mine(self.gold_to_mine[0])

                self.gold_to_mine.pop(0)
                #print(self.gold_to_mine)

                # self.rodolphe.mine(self.wood_to_mine[0])

            if (self.gold_to_mine2[0]["collision"] == False):
                self.gold_to_mine2.pop(0)


    def scanfood(self, position, area=3):
        position = (position[0] + area - 2, position[1] + area - 2)
        # print(position)
        food_list = []

        for a in range(2 * area - 3):
            x = position[0] - a
            # print(x)
            for b in range(2 * area - 3):
                y = position[1] - b
                # print(y)
                if (x > 49 or y > 49):
                    pass
                else:

                    if self.map.map[x][y]["tile"] == "food":
                        food_list.append(self.map.map[x][y])

        return food_list


    def scan_ally(self, position, area=3):
        position = (position[0] + area - 2, position[1] + area - 2)
        # print(position)
        ally_list = []

        for a in range(2 * area - 3):
            x = position[0] - a
            # print(x)
            for b in range(2 * area - 3):
                y = position[1] - b
                # print(y)
                if (x > 49 or y > 49):
                    pass
                else:

                    if self.map.map[x][y]["troop"] == "True":
                        ally_list.append(self.map.map[x][y])

        return ally_list

    def scanwood(self, position, area=3):
        position = (position[0] + area - 2, position[1] + area - 2)
        # print(position)
        wood_list = []

        for a in range(2 * area - 3):
            x = position[0] - a
            # print(x)
            for b in range(2 * area - 3):
                y = position[1] - b
                # print(y)
                if (x > 49 or y > 49):
                    pass
                else:

                    if self.map.map[x][y]["tile"] == "wood":
                        wood_list.append(self.map.map[x][y])

        return wood_list

    def scanstone(self, position, area=3):
        position = (position[0] + area - 2, position[1] + area - 2)
        # print(position)
        stone_list = []

        for a in range(2 * area - 3):
            x = position[0] - a
            # print(x)
            for b in range(2 * area - 3):
                y = position[1] - b
                # print(y)
                if (x > 49 or y > 49):
                    pass
                else:

                    if self.map.map[x][y]["tile"] == "stone":
                        stone_list.append(self.map.map[x][y])

        return stone_list

    def scangold(self, position, area=3):
        position = (position[0] + area - 2, position[1] + area - 2)
        # print(position)
        gold_list = []

        for a in range(2 * area - 3):
            x = position[0] - a
            # print(x)
            for b in range(2 * area - 3):
                y = position[1] - b
                # print(y)
                if (x > 49 or y > 49):
                    pass
                else:

                    if self.map.map[x][y]["tile"] == "gold":
                        gold_list.append(self.map.map[x][y])

        return gold_list

    # self.an_enemy.mine(self.food_tiles[2])

    # print(ResourceManager.enemy_resources.get("food"))

    
        # print(self.scanwood((self.map.enemy_TH_x,self.map.enemy_TH_y),6))
        """posfood = self.scanfood(enemypos)
        if posfood[2] == True:
            self.an_enemy.mine(self.map.map[posfood[0]][posfood[1]])
            """

        ''' spawn unité si resource suffisante mais probleme compatibilité pour le moment"
        #print(self.resource_manager.resources.get("food"))
        if (self.resource_manager.resources.get("food")>50):
                self.an_enemy = Worker(self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1], self.map)
                self.map.enemies.append(self.an_enemy)
                print(self.map.enemies[-1])
                self.map.map[self.map.enemy_TH_x - 1][self.map.enemy_TH_y + 1]["troop"] = True
                self.resource_manager.resources["food"] -= 50



        #wood mining
        if (self.wood_tiles[0] == self.wood_list[0] and bool(self.wood_list)):
            # print(self.enemy_resources[0])
            self.an_enemy.mine(self.wood_tiles[0])
            self.wood_list.pop(0)
        if (self.wood_tiles[0]["collision"] == False):
            self.wood_tiles.pop(0)


        # gold mining
        if (self.gold_tiles[0] == self.gold_list[0] and bool(self.gold_list) and bool(self.map.enemies)):
            self.map.enemies[-1].mine(self.gold_tiles[0])
            self.gold_list.pop(0)
        if (self.gold_tiles[0]["collision"] == False):
            self.gold_tiles.pop(0)

        # stone mining
        if (self.stone_tiles[0] == self.stone_list[0] and bool(self.stone_list) and bool(self.map.enemies)):
            self.map.enemies[-1].mine(self.stone_tiles[0])
            self.stone_list.pop(0)
        if (self.stone_tiles[0]["collision"] == False):
            self.stone_tiles.pop(0)





        '''
        # print(food_tiles[1])
        # an_enemy.mine(food_tiles[1])

    def looking_for_food(self):
        food_tiles = []
        for a in self.map:
            for tile in a:
                if tile['tile'] == "food":
                    food_tiles.append(tile)

        return food_tiles


'''
# ENEMY USEFULL FUNCTION UwU


Ce qui serai bien de faire apres l'ajout des fonctions spawn chez ennemi et chez allié: 
il faudrai affecter une team "allié" a chaque unité crée par la fonction de spawn_ally_unit et une team "ennemi" a chaque unité crée par spawn_enemy_unit

Ce qu'il faut faire pour l'IA en pseudo code et francais  :

Routine du BOT :

Construction premier batiment:
Conditions:

si il y a moins que un certain nombre de ce batiment
et que l'on a les ressource pour en construire
=> effectuer les constructions

Formation de villageois:
Conditions:

si il y en a moins qu'un certains nombre
et que l'on a les ressources disponibles
=> former des villageois

Objecitf principal du bot ,  passer à l'age suivant :

definir % de villageois a la Recherche de nourritures(Baies) et a la recolte de bois on va dire pour l'instant 60% sur la nourriture et 40% sur le bois
Condition: 2 batiments(a definir lequels) construit et au moins 500 de nourriture dans les stocks

Ainsi en code   Si (age_actuel==1ere age):
                    villageois sur la nourriture 60%
                    villageois sur le bois 40%
                    villageois sur la pierre  0%
                    villageois sur l'or 0%

Possibilité d'envoyer un soldat en exploration de maniere aleatoire

'''


