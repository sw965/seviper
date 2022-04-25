import seviper
import numpy as np
import pprint
import random

p1_fighters = seviper.Fighters(
    [seviper.TEMPLATE_POKEMONS["フシギバナ"],
     seviper.TEMPLATE_POKEMONS["リザードン"],
     seviper.TEMPLATE_POKEMONS["カメックス"]]
)

p2_fighters = seviper.Fighters(
    [seviper.TEMPLATE_POKEMONS["フシギバナ"],
     seviper.TEMPLATE_POKEMONS["リザードン"],
     seviper.TEMPLATE_POKEMONS["カメックス"]]
)

init_battle = seviper.Battle(p1_fighters, p2_fighters)
print(38 * 38)
print(init_battle.to_feature_array_3d().shape)
# def random_trainer(battle):
#     return random.choice(battle.p1_fighters.legal_action_commands())
#
# game_num = 512
# win_count = 0
# draw_count = 0
# for i in range(game_num):
#     winner = init_battle.playout(random_trainer, random_trainer)
#     if winner == seviper.WINNER_P1:
#         win_count += 1
#     elif winner == seviper.DRAW:
#         draw_count += 1
#
# print(win_count / game_num)
# print(1 - (win_count / game_num))
# print(draw_count / game_num)
