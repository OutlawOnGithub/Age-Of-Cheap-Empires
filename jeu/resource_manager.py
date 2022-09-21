import pygame as pg
from utils.save import *



class ResourceManager:

    def __init__(self, start_resources_player, start_resources_AI):

        self.start_resources_player = start_resources_player
        self.start_resources_AI = start_resources_AI
        # print("In RM : \n")
        # print(self.start_resources_player)

        cpt = 0
        for e in self.start_resources_player:
            if e.isdigit():
                cpt += 1

        # print(cpt)
        # print(len(self.start_resources_player))

        cpt1 = 0
        for e in self.start_resources_AI:
            if e.isdigit():
                cpt1 += 1
        # print(cpt1)
        # print(len(self.start_resources_AI))

        if cpt == len(self.start_resources_player):
            # print("[RM] You have set start values for player\n")
            self.wood = int(self.start_resources_player[0])
            self.stone = int(self.start_resources_player[1])
            self.food = int(self.start_resources_player[2])
            self.gold = int(self.start_resources_player[3])

            self.resources = {
                "wood": self.wood,
                "stone": self.stone,
                "food": self.food,
                "gold": self.gold
            }
        else:
            # print("[RM] Default values for player\n")

            self.resources = {
                "wood": 400,
                "stone": 400,
                "food": 1000,
                "gold": 100
            }
            
        if cpt1 == len(self.start_resources_AI):
            # print("[RM] You have set start values for AI\n")
            self.wood2 = int(self.start_resources_AI[0])
            self.stone2 = int(self.start_resources_AI[1])
            self.food2 = int(self.start_resources_AI[2])
            self.gold2 = int(self.start_resources_AI[3])
        
            self.enemy_resources = {
                "wood": self.wood2,
                "stone": self.stone2,
                "food": self.food2,
                "gold": self.gold2
            }
        else:
            # print("[RM] Default values for AI\n")
            self.enemy_resources = {
            "wood": 400,
            "stone": 400,
            "food": 1000,
            "gold": 10
        }

        #costs
        self.costs = {
            "Sawmill": {"wood": 300, "stone": 300},
            "Mason": {"wood": 300, "stone": 500},
            "Farm": {"wood": 500, "stone": 500},
            "Barrack": {"wood": 500, "stone": 300, "gold": 400},
            "Archery range": {"wood": 200, "stone": 900, "gold": 1000},
            "Stable": {"wood": 500, "stone": 500, "gold": 900},
            "Armory": {"wood": 1000, "stone": 1000},
            "Town Hall": {"wood": 0, "stone": 0},

            "EnemyBarrack": {"wood": 500, "stone": 500, "gold": 500},
            "EnemyArcheryRange": {"wood": 200, "stone": 900, "gold": 5000},
            "EnemyStable": {"wood": 500, "stone": 500, "gold": 900},
            "EnemyArmory": {"wood": 1000, "stone": 1000},
            "EnemyFarm": {"wood": 500, "stone": 500},
            "EnemyTownHall": {"wood": 0, "stone": 0},


            "worker" : {"food": 100},
            "swordman" : {"food": 100, "gold":150},
            "bowman" : {"food": 100, "gold" : 100, "wood": 100},
            "horseman" : {"food": 100, "gold" : 300},
            "herobrine": {"food": 0},

            "enemy worker" : {"food": 1000},
            "enemy swordman" : {"food": 100, "gold":150},
            "enemy bowman" : {"food": 100, "gold" : 100, "wood": 100},
            "enemy horseman" : {"food": 100, "gold" : 300},
            "herobrine": {"food": 0}
            
        }

    def apply_cost_to_resource(self, building):                #buildings
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

    def EN_apply_cost_to_resource(self, building):               #enemy buildings
        for enemy_resource, cost in self.costs[building].items():
            self.enemy_resources[enemy_resource] -= cost

    def EN_is_affordable(self, building):
        affordable = True
        for enemy_resource, cost in self.costs[building].items():
            if cost > self.enemy_resources[enemy_resource]:
                affordable = False
        return affordable



    def apply_cost_to_resource_troop(self, troop):            #troops/workers
        for resource, cost in self.costs[troop].items():
            self.resources[resource] -= cost

    def is_affordable_troop(self, troop):
        affordable = True
        for resource, cost in self.costs[troop].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

    def EN_apply_cost_to_resource_troop(self, troop):              #enemy troops
        for enemy_resource, cost in self.costs[troop].items():
            self.enemy_resources[enemy_resource] -= cost

    def EN_is_affordable_troop(self, troop):
        affordable = True
        for enemy_resource, cost in self.costs[troop].items():
            if cost > self.enemy_resources[enemy_resource]:
                affordable = False
        return affordable


