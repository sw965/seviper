import seviper
import numpy as np
import pprint

p1_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["フシギバナ"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["カメックス"]])

p2_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["カメックス"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["フシギバナ"]])

print(p1_fighters.legal_action_commands())
battle = seviper.Battle(p1_fighters, p2_fighters)
print(battle.all_damage_probability_distribution())
battle.to_feature_list()
