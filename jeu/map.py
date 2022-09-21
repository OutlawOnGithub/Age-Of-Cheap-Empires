import pygame as pg
import random
import noise
import time
from math import sqrt
from utils.sprite import dict_buildings, dict_workers, dict_diamond_buildings, dict_diamond_workers
from utils.util_functions import draw_text
from utils.settings import *
from utils.save import *

from entities.buildings import Archery_range, Armory, Barrack, EnemyTH, Farm, GoodTH, Mason, Sawmill, Stable, enemyth
from entities.units import Bowman, Horseman, Swordman, Worker



class Map:

    def __init__(self, screen, resource_manager, entities, hud, mapsize, width, height, camera,a=3):
        self.i = 0
        self.screen = screen
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.mapsize = mapsize
        self.width = width
        self.height = height
        self.camera = camera

        self.allyage = 1


        self.perlin_scale_wood = mapsize / 2
        self.perlin_scale_stone = mapsize / 14
        self.perlin_scale_gold = mapsize / 15
        self.perlin_scale_food = mapsize / 16
        self.perlin_scale_water = mapsize / 3

        self.GAME_SPEED = GAME_SPEED[2]

        self.grass_tiles = pg.Surface(
            (mapsize * TILE_SIZE * 2, mapsize * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()

        self.tiles = self.load_images()

        if 0: self.load_save() # mettre à 0 pour désactiver l'auto_save
        else:
            self.map = self.create_map()

            self.buildings = [[None for x in range(self.mapsize)] for y in range(self.mapsize)]

        self.vision_matrix = self.create_vision_matrix()
        self.mixed_matrix = self.create_mixed_matrix()  # contains both collision and water tiles

        self.workers = [[None for x in range(self.mapsize)] for y in range(self.mapsize)]

        ### Placing TH's 
        # -> The entry of the troops needs to be empty.
        # [self.ally_TH_x][self.ally_TH_y]: GoodTH position
        # Positions of spawned troop:
        # [self.ally_TH_x][self.ally_TH_y+1]: Worker
        # [self.ally_TH_x-1][self.ally_TH_y+1]: Swordman
        # [self.ally_TH_x+1][self.ally_TH_y+1] : Bowman
        # [self.ally_TH_x][self.ally_TH_y-2] : Horseman

        self.ally_TH_x, self.ally_TH_y = random.randint(4,10),random.randint(4,10) # to place the GoodTH around the top of the map
        self.enemy_TH_x, self.enemy_TH_y = self.mapsize-self.ally_TH_x, self.mapsize-self.ally_TH_y

        while self.map[self.ally_TH_x][self.ally_TH_y]["water"] or self.map[self.ally_TH_x][self.ally_TH_y]["collision"]\
            or self.map[self.enemy_TH_x][self.enemy_TH_y]["water"] or self.map[self.enemy_TH_x][self.enemy_TH_y]["collision"]:
            self.ally_TH_x, self.ally_TH_y = random.randint(4,10),random.randint(4,10)
            self.enemy_TH_x, self.enemy_TH_y = self.mapsize-self.ally_TH_x, self.mapsize-self.ally_TH_y


        self.clear_around_TH(3)


        #GoodTH
        render_pos = self.map[self.ally_TH_x][self.ally_TH_y]["render_pos"]
        pos =[self.ally_TH_x,self.ally_TH_y]
        self.map[self.ally_TH_x][self.ally_TH_y]["collision"] = True
        self.TH = GoodTH(pos, self.resource_manager, self)
        self.entities.append(self.TH)
        self.buildings[self.ally_TH_x][self.ally_TH_y] = self.TH
        self.update_mixed_matrix(self.ally_TH_x,self.ally_TH_y, True, "Town Hall")
        self.update_vision_matrix((self.ally_TH_x,self.ally_TH_y),self.TH.fieldofview)

        #EnnemyTH
        render_pos = self.map[self.enemy_TH_x][self.enemy_TH_y]["render_pos"]
        pos =[self.enemy_TH_x,self.enemy_TH_y]
        self.map[self.enemy_TH_x][self.enemy_TH_y]["collision"] = True
        self.enemyTH = EnemyTH(pos, self.resource_manager)  
        self.entities.append(self.enemyTH)
        self.buildings[self.enemy_TH_x][self.enemy_TH_y] = self.enemyTH
        self.update_mixed_matrix(self.enemy_TH_x, self.enemy_TH_y, True, "EnemyTownHall")

        for grid_x in range(self.mapsize):
            for grid_y in range(self.mapsize):
                map_tile = self.map[grid_x][grid_y]
                self.draw_grass(map_tile)

        
        # examined tiles and troops after a left click
        self.temp_tile = None
        self.examine_tile = None
        self.examine_troop = None

        self.whaleimage = pg.image.load("assets/graphics/whale.png").convert_alpha()
        self.fogofwar = pg.image.load("assets/graphics/fogofwar.png").convert_alpha()
        self.fogofwar.set_alpha(1000*FOW_YESORNO)

        # to know if we are placing a building. If this is the case, we can't examine a tile
        self.placing_building = False
        
    def set_all_tiles_value(self, pos1, pos2, collision, tile_type):
        # Set tiles and collisions value from pos1 to pos2 according to condition value (True or False)
        v = sqrt(((pos2[0]-pos1[0])**2 + (pos2[0]-pos1[0])**2)/2)
        v = int(v) + 1
        for x in range(v):
            for y in range(v):
                x_ = pos1[0] + x
                y_ = pos1[1] + y
                self.update_mixed_matrix(x_, y_, collision, tile_type)

    def clear_around_TH(self, area): 
        # Clear all the tiles (tile = "" and no collision) around and on the THs positions. 
        # The area fix the limit of the cleaning. ex: area = 2 -> all the tiles from a distance of 2 or less from the TH are cleaned
        self.set_all_tiles_value((self.ally_TH_x-area,self.ally_TH_y-area), (self.ally_TH_x+area,self.ally_TH_y+area), False, "")
        self.set_all_tiles_value((self.enemy_TH_x-area,self.enemy_TH_y-area), (self.enemy_TH_x+area,self.enemy_TH_y+area), False, "")

    def too_far_TH(self, position, area=3):
        position = (position[0] + area - 2, position[1] + area - 2)
        # print(position)
        too_far_list = []

        for a in range(2 * area - 3):
            x = position[0] - a
            # print(x)
            for b in range(2 * area - 3):
                y = position[1] - b
                # print(y)
                if (x > 49 or y > 49):
                    pass
                else:

                        too_far_list.append(self.map[x][y]["grid"])
        return too_far_list


               

    def update(self, camera):

        mouse_pos = pg.mouse.get_pos()
        global mouse_action
        mouse_action = pg.mouse.get_pressed()
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

        if -1<grid_pos[0]<self.mapsize and -1<grid_pos[1]<self.mapsize:

            if mouse_action[2]: # right click, cancel the selection
                self.examine_tile = None
                self.examine_troop = None
                self.hud.examined_tile = None
                self.hud.examined_troop = None
                self.placing_building = False
                
            # creating troops
            if self.hud.creerworker and self.resource_manager.is_affordable("worker"):
                aworker = Worker(self.map[self.ally_TH_x][self.ally_TH_y+1], self, self.resource_manager)
                self.workers.append(aworker)
                self.map[self.ally_TH_x][self.ally_TH_y+1]["troop"] = True
                time.sleep(.1)
            
            if self.hud.creerswordman and self.resource_manager.is_affordable("swordman"):
                aswordman = Swordman(self.map[self.ally_TH_x-1][self.ally_TH_y+1], self, self.resource_manager)  
                self.workers.append(aswordman)
                self.map[self.ally_TH_x-1][self.ally_TH_y+1]["troop"] = True
                time.sleep(.1)
            
            if self.hud.creerbowman and self.resource_manager.is_affordable("bowman"):
                abowman = Bowman(self.map[self.ally_TH_x+1][self.ally_TH_y+1], self, self.resource_manager)   
                self.workers.append(abowman)
                self.map[self.ally_TH_x+1][self.ally_TH_y+1]["troop"] = True
                time.sleep(.1)

            if self.hud.creerhorseman and self.resource_manager.is_affordable("horseman"):
                ahorseman = Horseman(self.map[self.ally_TH_x][self.ally_TH_y-2], self, self.resource_manager)  
                self.workers.append(ahorseman)
                self.map[self.ally_TH_x][self.ally_TH_y-2]["troop"] = True
                time.sleep(.1)

            if self.hud.ageup and self.resource_manager.resources["wood"]>5000 and self.resource_manager.resources["stone"]>5000 and self.resource_manager.resources["food"]>5000 and self.resource_manager.resources["gold"]>10000:
                self.resource_manager.resources["wood"] -= 5000
                self.resource_manager.resources["stone"] -= 5000
                self.resource_manager.resources["food"] -= 5000
                self.resource_manager.resources["gold"] -= 5000
                # for x in range(self.mapsize): 
                #     for y in range(self.mapsize):
                #         if self.buildings[x][y] != None:
                #             buildcoo = self.buildings[x][y].pos
                #             print(buildcoo)
                #             if self.buildings[x][y].name == "Barrack":
                #                 self.buildings[x][y] = None
                #                 ent = Barrack(buildcoo, self.resource_manager, self)
                
                self.allyage = 2

            if mouse_action[0] and (self.workers[grid_pos[0]][grid_pos[1]] is not None) \
            and self.examine_troop is None and not self.placing_building: # left clicking on a worker to examine it
                
                self.examine_troop=self.workers[grid_pos[0]][grid_pos[1]]
                self.examine_troop_tile=(grid_pos[0],grid_pos[1])             
                time.sleep(.1)

            
            if self.examine_troop is not None and self.examine_troop.team == 1: # selected worker's actions on left click
                if self.examine_troop.hp<=0: # unselecting a dead unit
                    self.examine_troop,self.hud.examined_troop = None,None
                #if mouse_action[0] and self.buildings[grid_pos[0]][grid_pos[1]] is None:
                    #moving
                if mouse_action[0] and self.can_place_tile(grid_pos):
                    if not (self.map[grid_pos[0]][grid_pos[1]]["collision"] or self.map[grid_pos[0]][grid_pos[1]]["water"] or self.buildings[grid_pos[0]][grid_pos[1]]) and self.workers[grid_pos[0]][grid_pos[1]] is None:
                        self.examine_troop.set_destination(self.map[grid_pos[0]][grid_pos[1]])
                        self.examine_troop.create_path()

                    # mining/going to a bloc
                    elif self.map[grid_pos[0]][grid_pos[1]]["resources"]!=0: 
                        if self.examine_troop.name=="worker" or self.examine_troop.name=="herobrine":
                            self.examine_troop.mine_tile = self.map[grid_pos[0]][grid_pos[1]]
                        else: self.examine_troop.go_close(self.map[grid_pos[0]][grid_pos[1]])

                    # attacking
                    elif self.workers[grid_pos[0]][grid_pos[1]] is not None and self.workers[grid_pos[0]][grid_pos[1]]!=self.examine_troop:
                        self.examine_troop.attacked_unit = self.workers[grid_pos[0]][grid_pos[1]]

                    # attacking building
                    elif self.buildings[grid_pos[0]][grid_pos[1]] is not None and self.buildings[grid_pos[0]][grid_pos[1]].team!=self.examine_troop.team:
                        self.examine_troop.attacked_building = self.buildings[grid_pos[0]][grid_pos[1]]

                            

            self.temp_tile = None

            if self.hud.selected_tile is not None: # selecting a building from hud
                self.hud.examined_troop, self.examine_troop = None,None

                if self.can_place_tile(grid_pos):
                    
                    self.placing_building = True
                    img = self.hud.selected_tile["image"].copy()
                    img.set_alpha(100)

                    render_pos = self.map[grid_pos[0]][grid_pos[1]]["render_pos"]
                    iso_poly = self.map[grid_pos[0]][grid_pos[1]]["iso_poly"]
                    collision = self.map[grid_pos[0]][grid_pos[1]]["collision"]
                    water = self.map[grid_pos[0]][grid_pos[1]]["water"]
                    troop = self.map[grid_pos[0]][grid_pos[1]]["troop"]
                    grid = self.map[grid_pos[0]][grid_pos[1]]["grid"]
                    if(grid in self.too_far_TH((self.ally_TH_x,self.ally_TH_y),10)):
                        #print("ok")
                        too_far = False
                    else:
                        too_far = True

                    #print(tuple(grid))

                    """print(self.too_far_TH((self.ally_TH_x,self.ally_TH_y),3)[1]["grid"])
                    print(self.too_far_TH((self.ally_TH_x, self.ally_TH_y), 3)[2]["grid"])
                    print(self.too_far_TH((self.ally_TH_x, self.ally_TH_y), 3)[3]["grid"])
                    print(self.too_far_TH((self.ally_TH_x, self.ally_TH_y), 3)[4]["grid"])
                    print(self.too_far_TH((self.ally_TH_x, self.ally_TH_y), 3)[5]["grid"])
                    print(self.too_far_TH((self.ally_TH_x, self.ally_TH_y), 3)[6]["grid"])
                    print(self.too_far_TH((self.ally_TH_x, self.ally_TH_y), 3)[7]["grid"])"""



                    #if(self.map[grid_pos[0],self.map[[grid_pos[1]]) in list:

                    #too_far = self.too_far_area



                    self.temp_tile = {
                        "image": img,
                        "render_pos": render_pos,
                        "iso_poly": iso_poly,
                        "collision": collision,
                        "water": water,
                        "troop" : troop,
                        "grid" : grid,



                    }
                    # placing buildings
                    if mouse_action[0] and not collision and not water and not troop and not too_far: # valid tile
                        self.placing_building = True
                        if self.hud.selected_tile["name"] == "Sawmill":
                            ent = Sawmill(grid_pos, self.resource_manage, self)
                            ent.in_construction = True
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Mason":
                            ent = Mason(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Farm":
                            ent = Farm(grid_pos, self.resource_manager, self)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Town Hall":
                            ent = GoodTH(grid_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "EnemyTownHall":
                            ent = EnemyTH(grid_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Barrack":
                            ent = Barrack(grid_pos, self.resource_manager, self, self.hud)
                            ent.in_construction = True
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Archery range":
                            ent = Archery_range(grid_pos, self.resource_manager, self, self.hud)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Stable":
                            ent = Stable(grid_pos, self.resource_manager, self, self.hud)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)
                        elif self.hud.selected_tile["name"] == "Armory":
                            ent = Armory(grid_pos, self.resource_manager, self, self.hud)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # self.update_vision_matrix(ent.pos, ent.fieldofview)

                        ent.in_construction = True
                        self.map[grid_pos[0]][grid_pos[1]]["collision"] = True # adding collision on map
                        self.mixed_matrix[grid_pos[1]][grid_pos[0]] = 0 # adding collision on mixed_matrix
                        #self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
                        self.hud.selected_tile = None # reset the selection
                        self.placing_building = False


            else: # not selecting an object from hud
                if self.can_place_tile(grid_pos) and not self.placing_building:
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    worker = self.workers[grid_pos[0]][grid_pos[1]]
                    if mouse_action[0] and (building is not None): # examinating a building
                        if isinstance(self.examine_troop,Worker) and building.in_construction == True:
                            self.examine_troop.build(building)
                        self.examine_tile = grid_pos
                        self.hud.examined_tile = building
                        self.hud.examined_troop = None
                        self.draw_hp_bar = True
                        self.examine_troop = None
                    if mouse_action[0] and (worker is not None): # examinating a worker
                        self.examine_troop_tile = grid_pos
                        self.hud.examined_troop = self.examine_troop
                        self.hud.examined_tile = None
                        self.draw_hp_bar = True

    def draw_grass(self, map_tile):
        tiletype = map_tile['tile']
        render_pos = map_tile["render_pos"]
        if tiletype == "water":
            self.grass_tiles.blit(self.tiles["water"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        elif tiletype == "sand":
            self.grass_tiles.blit(self.tiles["sand"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        else:
            self.grass_tiles.blit(self.tiles["block"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))
        
    
        for x in range(self.mapsize):
            for y in range(self.mapsize):
                render_pos = self.map[x][y]["render_pos"]
                # draw map tiles
                tile = self.map[x][y]["tile"]
                if not self.vision_matrix[x][y]:
                    screen.blit(self.fogofwar,
                                (render_pos[0]-1 + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                render_pos[1]-1 - (70 - TILE_SIZE) + camera.scroll.y))
                else:           
                    if tile != "" and tile != "water" and tile != "sand":
                        screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                    render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    elif tile == "water" and self.map[x][y]["whale"]:
                            screen.blit(self.whaleimage,
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                    render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    
                    # draw buildings
                    building = self.buildings[x][y]
                    worker = self.workers[x][y]

                    if building is not None:
                        worker = None
                        for building_name in dict_buildings:
                            if building.name == building_name:
                                if self.allyage == 1:
                                    image = pg.image.load(dict_buildings[building_name])
                                    if building.in_construction:
                                        image.set_alpha(100)

                                    screen.blit(image,
                                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                        render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                                    if not building.in_construction:
                                        # draw hp bar for all finished buildings
                                        x_ = render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x
                                        y_ =  render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y
                                        back_building_position = [x_+image.get_width()/2-building.maxhp/20, y_-10, building.maxhp/10, 5]
                                        building_position = [x_+image.get_width()/2-building.maxhp/20, y_-10, building.hp/10, 5]
                                        pg.draw.rect(screen, (220, 220, 220) , back_building_position)
                                        pg.draw.rect(screen, (71, 209, 71) , building_position)
                                    
                                else:
                                    image = pg.image.load(dict_diamond_buildings[building_name])
                                    if building.in_construction:
                                        image.set_alpha(100)

                                    screen.blit(image,
                                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                        render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                                    if not building.in_construction:
                                        # draw hp bar for all finished buildings
                                        x_ = render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x
                                        y_ =  render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y
                                        back_building_position = [x_+image.get_width()/2-building.maxhp/20, y_-10, building.maxhp/10, 5]
                                        building_position = [x_+image.get_width()/2-building.maxhp/20, y_-10, building.hp/10, 5]
                                        pg.draw.rect(screen, (220, 220, 220) , back_building_position)
                                        pg.draw.rect(screen, (71, 209, 71) , building_position)
                                   
                                if self.hud.examined_tile is not None and self.hud.examined_tile.team == 1:
                                    if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                                            mask = pg.mask.from_surface(image).outline()
                                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                    y + render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                                for x, y in mask]
                                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)
                                           
                    
                    # draw workers
                    mouse_pos = pg.mouse.get_pos()
                    grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                    
                    if worker is not None:
                        building = None
                        for worker_name in dict_workers:
                            if worker.name == worker_name:
                                if self.allyage == 1:
                                    imageworker = pg.image.load(dict_workers[worker_name])
                                    screen.blit(imageworker,
                                                (render_pos[0]+32 + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                render_pos[1]-16 - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y))

                                    # draw hp bar for all the troops
                                    x_ = render_pos[0]+32 + self.grass_tiles.get_width() / 2 + camera.scroll.x
                                    y_ = render_pos[1]-16 - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y
                                    back_worker_position = [x_+worker.image.get_width()/2-worker.maxhp/2, y_-10, worker.maxhp, 5]
                                    worker_position = [x_+worker.image.get_width()/2-worker.maxhp/2, y_-10, worker.hp, 5]
                                    pg.draw.rect(screen, (220, 220, 220) , back_worker_position)
                                    pg.draw.rect(screen, (71, 209, 71) , worker_position)
                                
                                else:
                                    imageworker = pg.image.load(dict_diamond_workers[worker_name])
                                    screen.blit(imageworker,
                                            (render_pos[0]+32 + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                            render_pos[1]-16 - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y))

                                    # draw hp bar for all the troops
                                    x_ = render_pos[0]+32 + self.grass_tiles.get_width() / 2 + camera.scroll.x
                                    y_ = render_pos[1]-16 - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y
                                    back_worker_position = [x_+worker.image.get_width()/2-worker.maxhp/2, y_-10, worker.maxhp, 5]
                                    worker_position = [x_+worker.image.get_width()/2-worker.maxhp/2, y_-10, worker.hp, 5]
                                    pg.draw.rect(screen, (220, 220, 220) , back_worker_position)
                                    pg.draw.rect(screen, (71, 209, 71) , worker_position)
                                
                               

                                if self.hud.examined_troop is not None and self.hud.examined_troop.team == 1: # examinating a troop
                                    if (x == self.examine_troop.tile["grid"][0]) and (y == self.examine_troop.tile["grid"][1]):
                                        image=self.examine_troop.image
                                        mask = pg.mask.from_surface(image).outline()
                                        mask = [(x + render_pos[0]+32 + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                    y + render_pos[1]-16 - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                                for x, y in mask]
                                        pg.draw.polygon(screen, (40, 165, 250), mask, 2) # to hilight the selected troop
               

        if self.temp_tile is not None:
            # Maintain the spawning place of the troops at "troop" = True
            # Because we don't want to place buildings at these positions
            self.map[self.ally_TH_x][self.ally_TH_y+1]["troop"] = True
            self.map[self.ally_TH_x-1][self.ally_TH_y+1]["troop"] = True
            self.map[self.ally_TH_x+1][self.ally_TH_y+1]["troop"] = True
            self.map[self.ally_TH_x][self.ally_TH_y-2]["troop"] = True

            self.map[self.enemy_TH_x][self.enemy_TH_y+1]["troop"] = True
            self.map[self.enemy_TH_x-1][self.enemy_TH_y+1]["troop"] = True
            self.map[self.enemy_TH_x+1][self.enemy_TH_y+1]["troop"] = True
            self.map[self.enemy_TH_x][self.enemy_TH_y-2]["troop"] = True          

            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"] or self.temp_tile["water"] or self.temp_tile["troop"]: # can't place a building here
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3) # red contouring
            else: # can place it
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3) # white contouring
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        mouse_pos = pg.mouse.get_pos()
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if (grid_pos[0] >= 0 and grid_pos[1] >= 0):
            draw_text(screen, str(grid_pos), 30, (255, 255, 255), (mouse_pos[0] + 15, mouse_pos[1] - 15))
        else:
            draw_text(screen, "(X, X)", 30, (255, 255, 255), (mouse_pos[0] + 15, mouse_pos[1] - 15))


    def draw_hp_bar(self, screen, render_pos, worker, camera):
         # draw hp bar of the attacked unit
        x_ = render_pos[0]+32 + self.grass_tiles.get_width() / 2 + camera.scroll.x
        y_ = render_pos[1]-16 - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y
        back_worker_position = [x_, y_-10, 20, 5]
        worker_position = [x_, y_-10, worker.hp, 5]
        pg.draw.rect(screen, (220, 220, 220) , back_worker_position)
        pg.draw.rect(screen, (71, 209, 71) , worker_position)

    def create_map(self):

        map = []
        r_noise = random.randint(25,35)
        for grid_x in range(self.mapsize):
            map.append([])
            for grid_y in range(self.mapsize):
                map_tile = self.grid_to_map(grid_x, grid_y, r_noise)
                map[grid_x].append(map_tile)
                self.draw_grass(map_tile)
        return map

    def grid_to_map(self, grid_x, grid_y, r_noise):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        
        r = random.randint(1, 100)
        #r_octave=random.randint(1,9)
        #rndnoise = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale, octaves=MAP_OCTAVE, base = MAP_SEED) #octavess pour la "naturalité" des forêts
        #rndnoisewater = 100 * noise.pnoise2(grid_x / self.perlin_scale_water, grid_y / self.perlin_scale_water, base = MAP_SEED)

        
        perlin_wood = 100 * noise.pnoise2(grid_x/(self.perlin_scale_wood), grid_y/self.perlin_scale_wood, octaves=MAP_OCTAVE, base=MAP_SEED)
        perlin_stone = 100 * noise.pnoise2(grid_x/self.perlin_scale_stone, grid_y/self.perlin_scale_stone, base=MAP_SEED)
        perlin_food = 100 * noise.pnoise2(grid_x/self.perlin_scale_food, grid_y/self.perlin_scale_food, base=MAP_SEED)
        perlin_gold = 100 * noise.pnoise2(grid_x/self.perlin_scale_gold, grid_y/self.perlin_scale_gold, base=MAP_SEED)
        perlin_water = 100 * noise.pnoise2(grid_x/self.perlin_scale_water, grid_y/self.perlin_scale_water, octaves=MAP_OCTAVE, base=MAP_SEED)

        if(perlin_water >= 60) or (perlin_water <= -40):
            tile = "water"
        elif (perlin_wood >= 70) or (perlin_wood <= -7):
            tile = "wood"
        elif(perlin_water <= 60 and perlin_water >=52) or (perlin_water >= -40 and perlin_water <= -32):
            tile = "sand"
        elif(perlin_stone >= 80) or (perlin_stone <= -50):
            tile = "stone"
        elif(perlin_food >= 70) or (perlin_food <= -40):
            tile = "food"
        elif(perlin_gold >= 100) or (perlin_gold <= -50):
            tile = "gold"
        else:
            tile = ""
        
        # if (rndnoise >= r_noise):
        #     tile = "wood"
        # elif (rndnoisewater <= -r_noise+10):
        #     tile = "water"
        # elif (rndnoisewater >= -r_noise+10 and rndnoisewater <= -r_noise+10+300*(1/self.mapsize)): #to differentiate world tile from what's on them
        #     tile = "sand"
        # else:
        #     # if r == 1:
        #     #    tile = "beeg_wood"
        #     if rndnoise >= 2 and rndnoise <= 2.3:        #not too much stone
        #         tile = "stone"
        #     elif rndnoise <= -2 and rndnoise >= -2.2:       #gold rarer than stone
        #         tile = "gold"
        #     elif rndnoise >= 6 and rndnoise <= 6.1:       #single woods kinda rare
        #         tile = "wood"
        #     elif (rndnoise <= r_noise-1 and rndnoise >= r_noise-2) or rndnoise >= 6.1 and rndnoise <= 6.6:   #bush près des arbres
        #         tile = "food"
        #     else:
        #         tile = ""

        out = {
            "grid" : [grid_x, grid_y],
            "cart_rect" : rect,
            "iso_poly" : iso_poly,
            "render_pos" : [minx, miny],
            "tile" : tile,
            "collision" : True if tile == "wood" or tile == "gold" or tile == "stone" or tile == "food" else False,
            "water" : True if tile == "water" else False,
            "resources" : 1000 if (tile == "wood" or tile == "food") else (5000 if tile == "gold" or tile == "stone" else 0),
            "whale" : True if (tile == "water" and random.randint(1,10000) == 1) else False,
            "troop": False,
            "too_far" : False
        }
        return out

    def create_mixed_matrix(self):
        # to manage the obstacles : collision and water (used for pathfinding)
        # 1: Empty  0: Occupied
        mixed_matrix = [[1 for x in range(self.mapsize)] for y in range(self.mapsize)]
        for x in range(self.mapsize):
            for y in range(self.mapsize):
                if self.map[x][y]["collision"] or self.map[x][y]["water"]:
                    mixed_matrix[y][x]=0
        return mixed_matrix

    def update_mixed_matrix(self, x, y, condition, tile_type):
        # condition = True or False
        self.map[x][y]["tile"] = tile_type
        self.map[x][y]["collision"] = condition
        self.mixed_matrix[y][x] = int(not condition)

    def create_vision_matrix(self):
        return [[0 for x in range(self.mapsize+10)] for y in range(self.mapsize+10)]

    def update_vision_matrix(self, coords, fov):
        for x in range(-fov+1, fov+1):
            for y in range (-fov+1, fov+1):
                self.vision_matrix[coords[0]+x][coords[1]+y] = 1


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    

    def load_images(self):

        # chargement des images
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        sawmill = pg.image.load("assets/graphics/sawmill.png").convert_alpha()
        mason = pg.image.load("assets/graphics/mason.png").convert_alpha()
        wood = pg.image.load("assets/graphics/tree.png").convert_alpha()
        stone = pg.image.load("assets/graphics/stone.png").convert_alpha()
        birch = pg.image.load("assets/graphics/birch.png").convert_alpha()
        beeg_wood = pg.image.load("assets/graphics/beeg_tree.png").convert_alpha()
        gold = pg.image.load("assets/graphics/gold.png").convert_alpha()
        farm = pg.image.load("assets/graphics/farm.png").convert_alpha()
        townhall = pg.image.load("assets/graphics/townhall.png").convert_alpha()
        enemytownhall = pg.image.load("assets/graphics/enemytownhall.png").convert_alpha()
        water = pg.image.load("assets/graphics/water.png").convert_alpha()
        sand = pg.image.load("assets/graphics/sand.png").convert_alpha()
        Barrack = pg.image.load("assets/graphics/Barrack.png").convert_alpha()
        Archery_range = pg.image.load("assets/graphics/Archery_range.png").convert_alpha()
        Stable = pg.image.load("assets/graphics/Stable.png").convert_alpha()
        Armory = pg.image.load("assets/graphics/armory.png").convert_alpha()
        whale = pg.image.load("assets/graphics/whale.png").convert_alpha()
        food = pg.image.load("assets/graphics/berry_bush.png").convert_alpha()

        images = {
            "sawmill": sawmill,
            "mason": mason,
            "wood": wood,
            "stone": stone,
            "block": block,
            "birch": birch,
            "beeg_wood": beeg_wood,
            "gold": gold,
            "farm": farm,
            "Town Hall": townhall,
            "EnemyTownHall": enemytownhall,
            "water": water,
            "sand": sand,
            "Barrack": Barrack,
            "Archery range": Archery_range,
            "Stable": Stable,
            "Armory": Armory,
            "whale": whale,
            "food": food
        }

        return images

    def can_place_tile(self, grid_pos):
        # check if we can place a tile
        # can place a tile if the mouse is not on a hud or outside the map
        mouse_on_panel = False
        if self.vision_matrix[grid_pos[0]][grid_pos[1]]:
            vision = True
        else : vision = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        map_bounds = (0 <= grid_pos[0] <= self.mapsize) and (0 <= grid_pos[1] <= self.mapsize)

        if map_bounds and not mouse_on_panel and vision:
            return True
        else:
            return False

    def mouse_to_grid_remastered(self,x,y):
        map_x = x - self.grass_tiles.get_width() / 2
        map_y = y
        cart_y = (2* map_y - map_x) / 2
        cart_x = cart_y + map_x
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x +51, grid_y - 50

    def mouse_to_grid(self, x, y, scroll):
        # transform to map position (removing camera scroll and offset)
        map_x = x - scroll.x - self.grass_tiles.get_width() / 2
        map_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * map_y - map_x) / 2
        cart_x = cart_y + map_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    # def mouse_to_grid_reversed(self,x,y,scroll):
    #     map_x = x - scroll.x - self.grass_tiles.get_width() / 2
    #     map_y = y - scroll.y
    #     # transform to cart (inverse of cart_to_iso)
    #     cart_y = (2 * map_y - map_x) / 2
    #     cart_x = cart_y + map_x
    #     # transform to grid coordinates
    #     grid_x = int(cart_x // TILE_SIZE)
    #     grid_y = int(cart_y // TILE_SIZE)
    #     return grid_x, grid_y

    def load_save(self):
        new_save = save()
        try:
            self.map=new_save.load_Map()
            for grid_x in range(self.mapsize):
                for grid_y in range(self.mapsize):
                    tiletype = self.map[grid_x][grid_y]['tile']
                    render_pos = self.map[grid_x][grid_y]['render_pos']
                    if tiletype =='water':
                        self.grass_tiles.blit(self.tiles["water"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
                    elif tiletype == "sand":
                        self.grass_tiles.blit(self.tiles["sand"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

                    else:
                        self.grass_tiles.blit(self.tiles["block"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        except FileNotFoundError:
            self.map = self.create_map()
            new_save.save_Map(self.map)

        except EOFError:
            self.map = self.create_map()
        
        new_save = save()
        try:
            self.map=new_save.load_Map()
            for grid_x in range(self.mapsize):
                for grid_y in range(self.mapsize):
                    tiletype = self.map[grid_x][grid_y]['tile']
                    render_pos = self.map[grid_x][grid_y]['render_pos']
                    if tiletype =='water':
                        self.grass_tiles.blit(self.tiles["water"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
                    elif tiletype == "sand":
                        self.grass_tiles.blit(self.tiles["sand"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

                    else:
                        self.grass_tiles.blit(self.tiles["block"],(render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        except FileNotFoundError:
            self.map = self.create_map()
            new_save.save_Map(self.map)

        except EOFError:
            self.map = self.create_map()
        
        new_save = save()

        buildings = [[None for x in range(self.mapsize)] for y in range(self.mapsize)]

        try:
            self.buildings=new_save.load_buildings()
        except FileNotFoundError:
            new_save.save_buildings(buildings)
            self.buildings = buildings
        except EOFError:
           self.buildings = buildings

        
