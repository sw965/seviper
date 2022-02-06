import unittest
import seviper.battle as battle

class Manager(unittest.TestCase):
    def test_battle(self):
        p1_fighters = [battle.TEMPLATE_POKEMONS["フシギバナ"],
                       battle.TEMPLATE_POKEMONS["リザードン"],
                       battle.TEMPLATE_POKEMONS["カメックス"]]
        p2_fighters = [battle.TEMPLATE_POKEMONS["カメックス"],
                       battle.TEMPLATE_POKEMONS["リザードン"],
                       battle.TEMPLATE_POKEMONS["フシギバナ"]]
        print(p1_fighters[0].current_hp)
        print(p2_fighters[0].current_hp)
        init_battle_manager = battle.Manager(p1_fighters, p2_fighters)
        print(init_battle_manager)
        battle_manager = init_battle_manager.push(["ギガドレイン", "なみのり"])
        print(battle_manager.p1_fighters[0].current_hp)
        print(battle_manager.p2_fighters[0].current_hp)
        print(init_battle_manager)

if __name__ == "__main__":
    unittest.main()
