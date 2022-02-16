import seviper.parts as parts
import seviper.battle as battle
import seviper.ai as ai
import numpy as np

p1_fighters = [battle.TEMPLATE_POKEMONS["フシギバナ"],
               battle.TEMPLATE_POKEMONS["リザードン"],
               battle.TEMPLATE_POKEMONS["カメックス"]]

p2_fighters = [battle.TEMPLATE_POKEMONS["カメックス"],
               battle.TEMPLATE_POKEMONS["リザードン"],
               battle.TEMPLATE_POKEMONS["フシギバナ"]]


battle_manager = battle.Manager(p1_fighters, p2_fighters)
image_battle = ai.ImageBattle(battle_manager)

array = np.array(image_battle.get())
print(array.shape)

for base_hp in ai.Features.BASE_HP:
    print(ai.FeatureValueTable.BASE_HP[base_hp])
