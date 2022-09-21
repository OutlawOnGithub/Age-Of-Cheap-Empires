import pygame as pg


def draw_text(screen, text, size, color, pos):

    font = pg.font.SysFont(None, size)                    #police par défaut
    text_surface = font.render(text, True, color)         
    text_rect = text_surface.get_rect(topleft=pos)        #get rekt lol

    screen.blit(text_surface, text_rect)
    
    
def spawn_enemy_unit(self,enemy):
    an_enemy = enemy(self.map.map[self.map.enemy_TH_x][self.map.enemy_TH_y + 1], self.map)
    self.map.workers.append(an_enemy)
    self.map.map[self.map.enemy_TH_x][self.map.enemy_TH_y + 1]["troop"] = True

def spawn_ally_unit(self,ally):
    an_ally = ally(self.map.map[self.map.ally_TH_x][self.map.ally_TH_y + 1], self.map)
    self.map.workers.append(an_ally)
    self.map.map[self.map.ally_TH_x][self.map.ally_TH_y + 1]["troop"] = True
