from random import randint


GAME_DIFFICULTY = {"Easy" : 1, "Medium" : 2, "Hard" : 3, "Impossible" : 4}
MAP_TYPE = None

MAP_SEED = 0  #0base/1g/2crash
print(MAP_SEED)
MAP_OCTAVE = 1

ALLY_AGE = 1

FOW_YESORNO = 1 #0 NO // 1 YES

TILE_SIZE = 32  #setup de la taille d'une tile // ne pas toucher merci
WORLD_SIZE = 50  #si changée, supprimer les fichiers de sauvegarde il faut

GAME_SPEED = [1000000000000, 1000, 700, 500, 300, 100, 1]
GAME_SPEED_NAMES = {1000000000000 : "pause", 1000 : "Snail", 700 : "Slow", 500 : "Normal", 300 : "Fast", 100 : "Lightning", 1 : "STEROIDS"}

CHEAT = True
GAP = 5

refreshminimapframe = 3
