import unittest
import seviper.battle as battle

class Pokemon(unittest.TestCase):
    def test_template_venusaur(self):
        venusaur = battle.TEMPLATE_POKEMONS["フシギバナ"]
        self.assertEqual(venusaur.max_hp, 187)
        self.assertEqual(venusaur.atk, 91)
        self.assertEqual(venusaur.defe, 103)
        self.assertEqual(venusaur.sp_atk, 120)
        self.assertEqual(venusaur.sp_def, 167)
        self.assertEqual(venusaur.speed, 101)
        self.assertEqual(venusaur.nature, "おだやか")
        self.assertEqual(venusaur.moveset["ギガドレイン"].max, 16)

    def test_template_charizard(self):
        charizard = battle.TEMPLATE_POKEMONS["リザードン"]
        self.assertEqual(charizard.speed, 167)
        self.assertEqual(charizard.max_hp, 154)
        self.assertEqual(charizard.atk, 93)
        self.assertEqual(charizard.defe, 98)
        self.assertEqual(charizard.sp_atk, 161)
        self.assertEqual(charizard.sp_def, 105)
        self.assertEqual(charizard.moveset["オーバーヒート"].max, 8)

    def test_template_blastoise(self):
        blastoise = battle.TEMPLATE_POKEMONS["カメックス"]
        self.assertEqual(blastoise.max_hp, 155)
        self.assertEqual(blastoise.atk, 92)
        self.assertEqual(blastoise.defe, 120)
        self.assertEqual(blastoise.sp_atk, 150)
        self.assertEqual(blastoise.sp_def, 125)
        self.assertEqual(blastoise.speed, 130)
        self.assertEqual(blastoise.moveset["からをやぶる"].max, 24)

class Manager(unittest.TestCase):
    def test_damage(self):
        p1_fighters = [battle.TEMPLATE_POKEMONS["フシギバナ"],
                       battle.TEMPLATE_POKEMONS["リザードン"],
                       battle.TEMPLATE_POKEMONS["カメックス"]]
        p2_fighters = [battle.TEMPLATE_POKEMONS["カメックス"],
                       battle.TEMPLATE_POKEMONS["リザードン"],
                       battle.TEMPLATE_POKEMONS["フシギバナ"]]

        test_num = 1280

        def test1():
            battle_manager = battle.Manager(p1_fighters, p2_fighters)
            results = [battle_manager.push(["ギガドレイン", "なみのり"]) for _ in range(test_num)]

            p1_expected_damages = [23, 24, 25, 26, 27, 34, 35, 36, 37, 38, 39, 40, 41]
            #くろいヘドロの回復量 = 11
            p1_expected_damages = [damage - 11 for damage in p1_expected_damages]
            p2_expected_damages = [84, 86, 90, 92, 96, 98, 122, 126, 128, 132, 134, 138, 140, 144, 146]

            p1_expected_current_hps = [187 - damage for damage in p1_expected_damages]
            p2_expected_current_hps = [155 - damage for damage in p2_expected_damages]

            self.assertTrue(all([battle_manager.p1_fighters[0].current_hp in p1_expected_current_hps \
                                 for battle_manager in results]))
            self.assertTrue(all([battle_manager.p2_fighters[0].current_hp in p2_expected_current_hps \
                                 for battle_manager in results]))

            p1_min_current_hp_result = min([battle_manager.p1_fighters[0].current_hp for battle_manager in results])
            p1_max_current_hp_result = max([battle_manager.p1_fighters[0].current_hp for battle_manager in results])
            p2_min_current_hp_result = min([battle_manager.p2_fighters[0].current_hp for battle_manager in results])
            p2_max_current_hp_result = max([battle_manager.p2_fighters[0].current_hp for battle_manager in results])

            self.assertEqual(p1_min_current_hp_result, 157)
            self.assertEqual(p1_max_current_hp_result, 175)
            self.assertEqual(p2_min_current_hp_result, 9)
            self.assertEqual(p2_max_current_hp_result, 71)

        def test2():
            battle_manager = battle.Manager(p1_fighters, p2_fighters)
            battle_manager = battle.push(["カメックス", "からをやぶる"])


        test1()

if __name__ == "__main__":
    unittest.main()
