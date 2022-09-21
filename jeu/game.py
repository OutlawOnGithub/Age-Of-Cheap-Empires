import pygame as pg
import sys
from .map import Map
from utils.settings import *
from utils.util_functions import draw_text,spawn_enemy_unit,spawn_ally_unit
from .camera import Camera
from .hud import Hud , Minimap
from .resource_manager import ResourceManager
from entities.units.worker import Herobrine
from .IA import *


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.cheat = CHEAT
        self.mapsize = WORLD_SIZE

        #victoire/defaite
        self.victoire = 1
        self.defaite = 1

        # entities
        self.entities = []

        # camera
        self.camera = Camera(self.width, self.height)
        self.camera.scroll.x = -int(31.6*WORLD_SIZE - 600)
        self.camera.scroll.y = WORLD_SIZE

    def initiate_resource_manager(self, start_resources_player, start_resources_AI):
        # resource manager
        # print("In initiate_resource_manager() :\n")
        # print(start_resources_player)
        # print(start_resources_AI)
        self.resource_manager = ResourceManager(start_resources_player, start_resources_AI)
        
    def initiate_hud(self):
        # hud
        self.hud = Hud(self.resource_manager, self.width, self.height)

    def initiate_map(self):
        # Map
        self.map = Map(
            self.screen, self.resource_manager, self.entities, self.hud,
            self.mapsize, self.width, self.height, self.camera
        )
        self.minimap = Minimap(self.map, self.width,self.height,self.mapsize)
    
    def initiate_IA(self):
        self.IA = IA_class(self.map, self.resource_manager)



    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(100)
            if self.events():
                self.playing=False
                return True
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:  # condition de victoire
                    self.map.enemyTH.hp = 0




                if event.key == pg.K_F12: # condition de défaite
                    self.map.TH.hp = 0

                if event.key == pg.K_ESCAPE:
                    return True
                if self.cheat:
                    if event.key == pg.K_F1:
                        self.map.workers.append(Herobrine(self.map.map[self.map.ally_TH_x+1][self.map.ally_TH_y+1], self.map, self.map.resource_manager))
                        self.map.map[self.map.ally_TH_x+1][self.map.ally_TH_y+1]["troop"] = True

                    if event.key == pg.K_F2:
                        for n in self.resource_manager.resources:
                            self.resource_manager.resources[n] +=10000

                    if event.key == pg.K_F3:
                        for n in self.resource_manager.resources:
                            if self.resource_manager.resources[n]-10000>=0:
                                self.resource_manager.resources[n] -=10000
                            else: self.resource_manager.resources[n]=0

                    if event.key == pg.K_F4:
                        for i in range(len(GAME_SPEED)):
                            if self.map.GAME_SPEED==GAME_SPEED[i]:
                                x=i
                        if x < len(GAME_SPEED)-1:
                            self.map.GAME_SPEED=GAME_SPEED[x+1]
                        else: self.map.GAME_SPEED=GAME_SPEED[0]

                    if event.key == pg.K_F5:
                        vision_range = range(len(self.map.vision_matrix))
                        for x in vision_range:
                            self.map.vision_matrix[x] = [1] * len(self.map.vision_matrix[x])

                    if event.key == pg.K_F6:
                        vision_range = range(len(self.map.vision_matrix))
                        for x in vision_range:
                            self.map.vision_matrix[x] = [0] * len(self.map.vision_matrix[x])
                        for x in range(len(self.map.buildings)):
                            for y in range(len(self.map.buildings)):
                                if self.map.buildings[x][y] is not None and self.map.buildings[x][y].team==1:
                                    self.map.update_vision_matrix((x,y),self.map.buildings[x][y].fieldofview)
            # if event.type == pg.MOUSEBUTTONDOWN:

    def update(self):

        self.camera.update()
        for e in self.entities:
            e.update()
            self.hud.end_V(self.screen)
        self.hud.update()
        self.map.update(self.camera)
        self.IA.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.camera)
        self.hud.draw(self.screen)
        self.minimap.update(self.screen)
        if self.map.enemyTH.hp <= 0 and self.victoire :  # condition de victoire
            #print("VICTORY")
            self.defaite = 0
            mouse_action = pg.mouse.get_pressed()
            self.map.GAME_SPEED = 1000000000000
            self.hud.end_V(self.screen)
            if mouse_action[0]:
                sys.exit()



        if self.map.TH.hp <= 0 and self.defaite :  # condition de défaite
            #print("DEFAITE")
            self.victoire = 0

            mouse_action = pg.mouse.get_pressed()
            self.map.GAME_SPEED = 1000000000000
            self.hud.end_D(self.screen)
            if mouse_action[0]:
                sys.exit()



        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 1)
        )
        if self.cheat:
            draw_text(self.screen,"Cheats ON",25,(255, 255, 255),(75, 1))
            draw_text(self.screen,"F1 Herobrine | ",25,(255, 255, 255),(10, 20))
            draw_text(self.screen,"F2-F3 +-10k resources | ",25,(255, 255, 255),(130, 20))
            draw_text(self.screen,"F4 Game speed : " + GAME_SPEED_NAMES[self.map.GAME_SPEED] + " | ",25,(255, 255, 255),(320, 20))
            draw_text(self.screen,"F5 No fog | ",25,(255, 255, 255),(555, 20))
            draw_text(self.screen,"F6 Reset fog | ",25,(255, 255, 255),(645, 20))

        pg.display.flip()
