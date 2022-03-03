import seviper
import numpy as np
import pprint

p1_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["フシギバナ"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["カメックス"]])

p2_fighters = seviper.Fighters([seviper.TEMPLATE_POKEMONS["カメックス"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["フシギバナ"]])

print(p1_fighters[0].to_feature_array().shape)
print(p1_fighters.to_feature_array())
print(38 * 37)

battle = seviper.Battle(p1_fighters, p2_fighters)
print(len(battle.damage_probability_distribution()))
