import seviper
import numpy as np
import pprint

p1_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["フシギバナ"],
                                seviper.TEMPLATE_POKEMONS["リザードン"],
                                seviper.TEMPLATE_POKEMONS["カメックス"]])

p2_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["リザードン"],
                                seviper.TEMPLATE_POKEMONS["カメックス"],
                                seviper.TEMPLATE_POKEMONS["フシギバナ"]])

battle = seviper.Battle(p1_fighters, p2_fighters)
battle_with_ui = battle.new_with_ui()
battle_with_ui = battle_with_ui.push({"p1":"やどりぎのタネ", "p2":"かえんほうしゃ"})

for ui in battle_with_ui.ui:
    print(ui)

# accum_uis = []
#
# battle, uis = seviper.p2_action(battle, "かえんほうしゃ")
# accum_uis += uis
#
# battle, uis = seviper.BattleUIsMaker.p1_action(battle, "ギガドレイン")
# accum_uis += uis
#
# for ui in accum_uis:
#     print(ui)

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
