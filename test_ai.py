import seviper
import numpy as np
import pprint
import random
import boa
import copy
import math
import seviper.mcts as mcts

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
    return random.choice(battle.p1_fighters.legal_action_commands())

battle_with_ui = init_battle.to_with_ui()
mcts_trainer = mcts.new_trainer(1960, math.sqrt(2), mcts.Eval.new_random_playout())
s, a, ui_history, winner = battle_with_ui.one_game(mcts_trainer, mcts_trainer)
boa.dump_pickle(ui_history, "C:/Python35/pyckage/seviper/text.pkl")

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
