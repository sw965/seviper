import seviper
import numpy as np
import pprint
print(seviper.MIN_PRIORITY_RANK)
print(seviper.MAX_PRIORITY_RANK)
p1_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["フシギバナ"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["カメックス"]])

p2_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["カメックス"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["フシギバナ"]])

import random
def random_trainer(battle):
    return random.choice(battle.p1_fighters.legal_action_commands())

battle = seviper.Battle(p1_fighters, p2_fighters)
print(battle.one_game(random_trainer, random_trainer))
feature_list = battle.to_feature_array_3d()
print(feature_list.shape)
print(feature_list.ndim)
