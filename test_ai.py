import seviper.parts as parts
import seviper.battle as battle
import seviper.ai as ai


p1_fighters = [battle.TEMPLATE_POKEMONS["フシギバナ"],
               battle.TEMPLATE_POKEMONS["リザードン"],
               battle.TEMPLATE_POKEMONS["カメックス"]]

p2_fighters = [battle.TEMPLATE_POKEMONS["カメックス"],
               battle.TEMPLATE_POKEMONS["リザードン"],
               battle.TEMPLATE_POKEMONS["フシギバナ"]]


battle_manager = battle.Manager(p1_fighters, p2_fighters)
ai.ImageBattle()
