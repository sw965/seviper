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

def random_trainer(battle):
    return random.choice(battle.p1_fighters.legal_action_cmds())

battle_with_ui = init_battle.to_with_ui()
mcts_trainer = mcts.new_trainer(16, math.sqrt(2), mcts.Eval.new_random_playout())

p1_win_count = 0
game_num = 1
for i in range(game_num):
    winner = init_battle.playout(mcts_trainer, random_trainer)
    if winner == seviper.WINNER_P1:
        p1_win_count += 1
    print(i)

print(float(p1_win_count) / float(game_num))

#boa.dump_pickle(ui_history, "C:/Python35/pyckage/seviper/text.pkl")
pokemon1 = seviper.new_venusaur()
pokemon2 = seviper.new_charizard()
pokemon3 = seviper.new_blastoise()

fighters = seviper.Fighters([pokemon1, pokemon2, pokemon3])
battle = seviper.Battle(fighters, fighters)
c = np.array(battle.two_d_feature_list())
print(c.shape)

b = np.array(fighters.two_d_feature_list())
print(b.shape)

a = np.array(pokemon1.two_d_feature_list())
print(a.shape)

s = ""
for ui in ui_history:
    print(ui)

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
