import pygame as pg

#Button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    

    def draw(self, surface):

        action = False

        #get mouse position
        pos = pg.mouse.get_pos()
        
        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            # [0] :left click
            if pg.mouse.get_pressed()[0] and not self.clicked: 
                self.clicked = True
                action = True
                

        if not pg.mouse.get_pressed()[0]: #left btn is not clicked
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action