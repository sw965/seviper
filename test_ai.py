import seviper
import numpy as np
import pprint
print(seviper.MIN_PRIORITY_RANK)
print(seviper.MAX_PRIORITY_RANK)
team = seviper.Team([seviper.TEMPLATE_POKEMONS["フシギバナ"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["カメックス"]])

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
battle, uis = seviper.BattleUIsMaker.move_use(battle, seviper.STRUGGLE, True)

for ui in uis:
    print(ui)

# count = 0
# count2 = 0
# game_num = 12
# for i in range(game_num):
#     winner = battle.one_game(random_trainer, random_trainer, 128)
#     if winner == seviper.WINNER_P1:
#         count += 1
#
#     if winner == seviper.DRAW:
#         count2 += 1
#
# print(float(count) / float(game_num))
# print(float(count2) / float(game_num))
# print(1 - (float(count) / float(game_num)))
#
# feature_array = battle.to_feature_array_3d(128)
# print(feature_array.shape)
# print(feature_array.ndim)
