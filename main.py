import pygame as pg
from jeu.game import Game
from utils.menu import Menu
import sys

def main():

    # implement image/clock/sound
    pg.init()
    # pg.mixer.init()
    screen = pg.display.set_mode()
    clock = pg.time.Clock()
    pg.display.set_caption("Age of Cheap Empires - TD1STI3AG2 ")

    # main music
    # pg.mixer.music.load('assets/menu/music.mp3')
    # pg.mixer.music.set_volume(0.7)
    # pg.mixer.music.play(loops = -1)

    game = Game(screen, clock)
    menu = Menu(screen, game)

    start_resources_player = 'default'
    start_resources_AI = 'default'

    while menu.running:
        menu = Menu(screen, game)
        
        while menu.menuing:
            if menu.optioning:
                out = menu.draw_options()
                # print("out:\n", out)
                if out is not None and out[0]:
                    menu = Menu(screen, game)
                    start_resources_player = out[1]
                    start_resources_AI = out[2]
            elif menu.loading_selection:
                if menu.draw_loads():
                    menu = Menu(screen,game)
            else:
                menu.draw_menu()
            pg.display.update()

        if not hasattr(game,'resource_manager'):
            game.initiate_resource_manager(start_resources_player, start_resources_AI)
        if not hasattr(game,'hud'):
            game.initiate_hud()
        if not hasattr(game, 'map'):
            game.initiate_map()
        if not hasattr(game,'IA'):
            game.initiate_IA()
        while menu.playing:
            menu.menuing = game.run()
            menu.playing = False

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
