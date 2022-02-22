import seviper
import numpy as np
import pprint

p1_fighters = [seviper.TEMPLATE_POKEMONS["フシギバナ"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["カメックス"]]

p2_fighters = [seviper.TEMPLATE_POKEMONS["カメックス"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["フシギバナ"]]


battle = seviper.Battle(seviper.Fighters(p1_fighters), seviper.Fighters(p2_fighters))
battle_image = battle.to_image()
for i, image_2d in enumerate(battle_image):
    print(str(i) + "番目!")
    pprint.pprint(image_2d)
    print("------")
    print("------")
    print("------")
    print("------")
    print("------")
