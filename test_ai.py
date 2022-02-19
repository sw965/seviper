import seviper.src as seviper
import seviper.ai
import numpy as np

p1_fighters = [seviper.TEMPLATE_POKEMONS["フシギバナ"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["カメックス"]]

p2_fighters = [seviper.TEMPLATE_POKEMONS["カメックス"],
               seviper.TEMPLATE_POKEMONS["リザードン"],
               seviper.TEMPLATE_POKEMONS["フシギバナ"]]


battle_manager = seviper.BattleManager(p1_fighters, p2_fighters)
image_battle = seviper.ai.ImageBattle(battle_manager)

array = np.array(image_battle.get())
print(array.shape)

for base_hp in seviper.ai.Features.BASE_HP:
    print(ai.FeatureValueTable.BASE_HP[base_hp])
