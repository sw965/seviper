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
team_builder = seviper.TeamBuilder()
