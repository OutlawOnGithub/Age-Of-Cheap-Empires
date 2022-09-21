import pygame as pg
from utils.button import Button
from utils.save import save, file_manager
from utils.settings import *
import sys
from utils.util_functions import draw_text


class Menu:

    def __init__(self, screen, game):
        self.save = save()
        self.screen = screen
        self.game = game
        self.width = self.screen.get_size()[0]
        self.height = self.screen.get_size()[1]

        self.running = True
        self.playing = False
        self.menuing = True
        self.optioning = False
        self.loading_selection = False

        background = pg.image.load('assets/menu/background.png').convert_alpha()
        background = pg.transform.scale(background,screen.get_size())
        screen.blit(background,(0,0))

        self.load_images()

    def draw_menu(self):
        for event in pg.event.get():
            if self.start_button.draw(self.screen) or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.playing = True
                self.menuing = False

        if self.exit_button.draw(self.screen):
            pg.quit()
            sys.exit()

        if self.option_button.draw(self.screen):
            self.optioning = True

        if self.save_button.draw(self.screen):
            new_save = save()
            new_save.save_resources(self.game.resource_manager.resources)
            if hasattr(self.game,'map'):
                new_save.save_Map(self.game.map.map) #IF HAS ATTR MAP ...
                new_save.save_buildings(self.game.map.buildings) #NEED TO SAVE LIST OF POSITION
                new_save.save_entities(self.game.map.workers)
            file = file_manager()
            file.create_save()

        if self.load_button.draw(self.screen):
            self.loading_selection = True

    def draw_options(self):
        background = pg.image.load('assets/menu/option_background.png').convert_alpha()
        background = pg.transform.scale(background,self.screen.get_size())
        self.screen.blit(background,(0,0))
        title = pg.image.load('assets/menu/options_menu.png').convert_alpha()
        self.screen.blit(title,((self.width-title.get_size()[0])/2,0))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.optioning = False
                return True

        if self.game.cheat:
            if self.cheatson_button.draw(self.screen):
                self.game.cheat = False
        else:
            if self.cheatsoff_button.draw(self.screen):
                self.game.cheat = True
        
        if not hasattr(self.game, 'map'):
            draw_text(self.screen,str(self.game.mapsize),50,(255,255,255),\
            (self.width/2+0.5*self.mapsize_img.get_width()+self.plus_img.get_width(),self.height*0.375))
            if self.game.mapsize<200:
                if self.plus_button.draw(self.screen):
                    self.game.mapsize +=10
            if self.game.mapsize>50:
                if self.minus_button.draw(self.screen):
                    self.game.mapsize -=10
            if self.mapsize_button.draw(self.screen):
                pass


        if self.exit_button.draw(self.screen):
            pg.quit()
            sys.exit()


    def draw_loads(self):#a modifier
        background = pg.image.load('assets/menu/option_background.png').convert_alpha()
        background = pg.transform.scale(background,self.screen.get_size())
        self.screen.blit(background,(0,0))
        #title = pg.image.load('assets/menu/options_menu.png').convert_alpha()
        #self.screen.blit(title,((self.width-title.get_size()[0])/2,0))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.optioning = False
                return True

        if self.exit_button.draw(self.screen):
            pg.quit()
            sys.exit()
        if self.save1_button.draw(self.screen):
            #time.sleep(0.1)
            self.save.load_back(1) # just file management i think
            self.game.map.map = self.save.load_Map()
            self.game.buildings = self.save.load_buildings()
            self.game.resource_manager.resources = self.save.load_resources()
            self.game.workers = self.save.load_entities()
            print(self.game.buildings)
            print("entities",self.game.workers)
            self.game.map.reinstantiate_worker(self.game.map,self.game.workers)
            self.game.map.reinstantiate_building(self.game.map,self.game.buildings)
        if self.save2_button.draw(self.screen):

            self.save.load_back(2) # just file management i think
            self.game.map.map = self.save.load_Map()
            self.game.buildings = self.save.load_buildings()
            self.game.resource_manager.resources = self.save.load_resources()
            self.game.workers = self.save.load_entities()
            self.game.map.reinstantiate_worker(self.game.map,self.game.workers)
            self.game.map.reinstantiate_building(self.game.map,self.game.buildings)

        if self.save3_button.draw(self.screen):
            self.save.load_back(3)
            self.game.map.map = self.save.load_Map()
            self.game.buildings = self.save.load_buildings()
            self.game.resource_manager.resources = self.save.load_resources()
            self.game.workers = self.save.load_entities()
            self.game.map.reinstantiate_worker(self.game.map,self.game.workers)
            self.game.map.reinstantiate_building(self.game.map,self.game.buildings)



    def load_images(self):
        #load button images
        start_img = pg.image.load('assets/menu/play.png').convert_alpha()
        exit_img = pg.image.load('assets/menu/exit.png').convert_alpha()
        option_img = pg.image.load('assets/menu/options.png').convert_alpha()
        save_img = pg.image.load('assets/menu/save.png').convert_alpha()
        load_img = pg.image.load('assets/menu/load.png').convert_alpha()
        save1_img = pg.image.load('assets/menu/save1.png').convert_alpha()
        save2_img = pg.image.load('assets/menu/save2.png').convert_alpha()
        save3_img = pg.image.load('assets/menu/save3.png').convert_alpha()
        cheatson_img = pg.image.load('assets/menu/CheatsON.png').convert_alpha()
        cheatsoff_img = pg.image.load('assets/menu/CheatsOFF.png').convert_alpha()
        self.plus_img = pg.image.load('assets/menu/plus.png').convert_alpha()
        minus_img = pg.image.load('assets/menu/minus.png').convert_alpha()
        self.mapsize_img = pg.image.load('assets/menu/mapsize.png').convert_alpha()
        
        #create button instances
        self.start_button = Button(self.width*0.085, self.height*0.818, start_img, 0.8)
        self.exit_button = Button(self.width*0.765, self.height*0.818, exit_img, 0.8)
        self.option_button = Button(self.width*0.085, self.height*0.1, option_img, 0.8)
        self.save_button = Button(self.width*0.8, self.height*0.1, save_img, 0.25)
        self.load_button = Button(self.width*0.610, self.height*0.12, load_img, 0.7)
        self.loading_button = Button(self.width*0.4,self.height*0.3,start_img,0.8)
        self.save1_button = Button(self.width*0.4,self.height*0.3,save1_img,0.8)
        self.save2_button = Button(self.width*0.4,self.height*0.5,save2_img,0.8)
        self.save3_button = Button(self.width*0.4,self.height*0.7,save3_img,0.8)
        self.cheatson_button = Button((self.width-cheatson_img.get_width())/2,self.height*0.2,cheatson_img,1)
        self.cheatsoff_button = Button((self.width-cheatsoff_img.get_width())/2,self.height*0.2,cheatsoff_img,1)
        self.mapsize_button = Button((self.width-self.mapsize_img.get_width()-self.plus_img.get_width())/2,self.height*0.35,self.mapsize_img,1)
        self.plus_button = Button(self.width/2+0.5*self.mapsize_img.get_width(),self.height*0.35,self.plus_img,1)
        self.minus_button = Button(self.width/2+0.5*self.mapsize_img.get_width(),self.height*0.40,minus_img,1)
        
