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
    [seviper.TEMPLATE_POKEMONS["カメックス"],
     seviper.TEMPLATE_POKEMONS["リザードン"],
     seviper.TEMPLATE_POKEMONS["フシギバナ"]]
)
p2_fighters[0].item = "くろいヘドロ"
battle = seviper.Battle(p1_fighters, p2_fighters)
battle_with_ui = battle.to_with_ui()
# battle_with_ui = battle_with_ui.push({"p1":"ギガドレイン", "p2":"れいとうビーム"})
# for ui in battle_with_ui.ui:
#     print(ui)

print("end")
battle_with_ui = battle_with_ui.push({"p1":"ギガドレイン", "p2":"リザードン"})
for ui in battle_with_ui.ui:
    print(ui)
