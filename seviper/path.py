import os

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = BASE_DIRECTORY + "/data/"

ALL_POKE_NAMES = DATA_FOLDER + "all_poke_names.txt"
ALL_MOVE_NAMES = DATA_FOLDER + "all_move_names.txt"
ALL_ITEMS = DATA_FOLDER + "all_items.txt"
ONE_HIT_KO_MOVE_NAMES = DATA_FOLDER + "one_hit_ko_move_names.txt"
HALF_HEAL_MOVE_NAMES = DATA_FOLDER + "half_move_names.txt"

POKEDEX = DATA_FOLDER + "pokedex/"
MOVEDEX = DATA_FOLDER + "movedex/"
NATUREDEX = DATA_FOLDER + "naturedex.json"
TYPEDEX = DATA_FOLDER + "typedex.json"

POKETETU_DATA_FOLDER = BASE_DIRECTORY + "/poketetu/data/"
POKETETU_POKEDEX = POKETETU_DATA_FOLDER + "pokedex/"
POKETETU_MOVEDEX = POKETETU_DATA_FOLDER + "movedex/"
POKETETU_LEARNSET = POKETETU_DATA_FOLDER + "learnset/"

IMAGE_FOLDER = BASE_DIRECTORY + "/image/"
POKE_GIF = IMAGE_FOLDER + "gif/"
POKE_GIF_NORMAL = POKE_GIF + "normal/"
POKE_GIF_MIRROR = POKE_GIF + "mirror/"
