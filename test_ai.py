import seviper
import numpy as np
import pprint
import random
import boa
import copy
import math
import seviper.mcts as mcts
import seviper.base_data as base_data

p1_fighters = seviper.Fighters(
    [seviper.TEMPLATE_POKEMONS["フシギバナ"](),
     seviper.TEMPLATE_POKEMONS["リザードン"](),
     seviper.TEMPLATE_POKEMONS["カメックス"]()]
)

p2_fighters = seviper.Fighters(
    [seviper.TEMPLATE_POKEMONS["フシギバナ"](),
     seviper.TEMPLATE_POKEMONS["リザードン"](),
     seviper.TEMPLATE_POKEMONS["カメックス"]()]
)

init_battle = seviper.Battle(p1_fighters, p2_fighters)
adpd = init_battle.all_damage_probability_distribution()["p1_attack"]
for key, value in adpd[1][0].items():
    print(key, value)

feature = init_battle.feature()
for i, d in enumerate(feature):
    print("i = ", i, d)
