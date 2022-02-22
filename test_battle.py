import unittest
import seviper

class Pokemon(unittest.TestCase):
    def test_template_venusaur(self):
        venusaur = seviper.TEMPLATE_POKEMONS["フシギバナ"]
        self.assertEqual(venusaur.max_hp, 187)
        self.assertEqual(venusaur.atk, 91)
        self.assertEqual(venusaur.defe, 103)
        self.assertEqual(venusaur.sp_atk, 120)
        self.assertEqual(venusaur.sp_def, 167)
        self.assertEqual(venusaur.speed, 101)
        self.assertEqual(venusaur.nature, "おだやか")
        self.assertEqual(venusaur.moveset["ギガドレイン"].max, 16)

    def test_template_charizard(self):
        charizard = seviper.TEMPLATE_POKEMONS["リザードン"]
        self.assertEqual(charizard.speed, 167)
        self.assertEqual(charizard.max_hp, 154)
        self.assertEqual(charizard.atk, 93)
        self.assertEqual(charizard.defe, 98)
        self.assertEqual(charizard.sp_atk, 161)
        self.assertEqual(charizard.sp_def, 105)
        self.assertEqual(charizard.moveset["オーバーヒート"].max, 8)

    def test_template_blastoise(self):
        blastoise = seviper.TEMPLATE_POKEMONS["カメックス"]
        self.assertEqual(blastoise.max_hp, 155)
        self.assertEqual(blastoise.atk, 92)
        self.assertEqual(blastoise.defe, 120)
        self.assertEqual(blastoise.sp_atk, 150)
        self.assertEqual(blastoise.sp_def, 125)
        self.assertEqual(blastoise.speed, 130)
        self.assertEqual(blastoise.moveset["からをやぶる"].max, 24)

class Manager(unittest.TestCase):
    def test_damage(self):
        p1_fighters = [seviper.TEMPLATE_POKEMONS["フシギバナ"],
                       seviper.TEMPLATE_POKEMONS["リザードン"],
                       seviper.TEMPLATE_POKEMONS["カメックス"]]
        p2_fighters = [seviper.TEMPLATE_POKEMONS["カメックス"],
                       seviper.TEMPLATE_POKEMONS["リザードン"],
                       seviper.TEMPLATE_POKEMONS["フシギバナ"]]

        test_num = 1920

        def test1():
            battle = seviper.Battle(p1_fighters, p2_fighters)
            results = [battle.push(["ギガドレイン", "なみのり"]) for _ in range(test_num)]

            p1_expected_damages = [23, 24, 25, 26, 27, 34, 35, 36, 37, 38, 39, 40, 41]
            #くろいヘドロの回復量 = 11
            p1_expected_damages = [damage - 11 for damage in p1_expected_damages]
            p2_expected_damages = [84, 86, 90, 92, 96, 98, 122, 126, 128, 132, 134, 138, 140, 144, 146]

            p1_expected_current_hps = [187 - damage for damage in p1_expected_damages]
            p2_expected_current_hps = [155 - damage for damage in p2_expected_damages]

            self.assertTrue(all([battle.p1_fighters[0].current_hp in p1_expected_current_hps \
                                 for battle in results]))
            self.assertTrue(all([battle.p2_fighters[0].current_hp in p2_expected_current_hps \
                                 for battle in results]))

            p1_min_current_hp_result = min([battle.p1_fighters[0].current_hp for battle in results])
            p1_max_current_hp_result = max([battle.p1_fighters[0].current_hp for battle in results])
            p2_min_current_hp_result = min([battle.p2_fighters[0].current_hp for battle in results])
            p2_max_current_hp_result = max([battle.p2_fighters[0].current_hp for battle in results])

            self.assertEqual(p1_min_current_hp_result, 157)
            self.assertEqual(p1_max_current_hp_result, 175)
            self.assertEqual(p2_min_current_hp_result, 9)
            self.assertEqual(p2_max_current_hp_result, 71)

        def test2():
            ...


        test1()

    def test_final_damage_probability_distribution(self):
        p1_fighters = [seviper.TEMPLATE_POKEMONS["フシギバナ"],
                       seviper.TEMPLATE_POKEMONS["リザードン"],
                       seviper.TEMPLATE_POKEMONS["カメックス"]]
        p2_fighters = [seviper.TEMPLATE_POKEMONS["カメックス"],
                       seviper.TEMPLATE_POKEMONS["リザードン"],
                       seviper.TEMPLATE_POKEMONS["フシギバナ"]]

        battle = seviper.Battle(p1_fighters, p2_fighters)
        p1_result, p2_result = battle.damage_probability_distribution()

        def helper(result, damages, p1_fighter_i, p2_fighter_i, move_name):
            damage_keys = list(result[p1_fighter_i][p2_fighter_i][move_name].keys())
            self.assertTrue(all([damage in damages for damage in damage_keys]))
            self.assertTrue(all([damage in damage_keys for damage in damages]))
            self.assertTrue(len(damages) == len(damage_keys))

        """p1のフシギバナからp2のカメックスへのダメージ確率分布"""
        damages = [0, 84, 86, 90, 92, 96, 98, 122, 126, 128, 132, 134, 138, 140, 144, 146]
        helper(p1_result, damages, 0, 0, "ギガドレイン")

        damages = [0, 51, 52, 54, 55, 57, 58, 60, 76, 78, 79, 81, 82, 84, 85, 87, 88, 90]
        helper(p1_result, damages, 0, 0, "ヘドロばくだん")

        damages = [0]
        helper(p1_result, damages, 0, 0, "やどりぎのタネ")

        damages = [0]
        helper(p1_result, damages, 0, 0, "まもる")

        """p1のフシギバナからp2のリザードンへのダメージ確率分布"""
        damages = [0, 58, 60, 61, 63, 64, 66, 67, 69, 70, 88, 90, 91, 93, 94, 96, 97, 99, 100, 102, 103, 105]
        helper(p1_result, damages, 0, 1, "ヘドロばくだん")

        damages = [0, 12, 13, 14, 18, 19, 20, 21]
        helper(p1_result, damages, 0, 1, "ギガドレイン")

        """p1のフシギバナからp2のフシギバナへのダメージ確率分布"""
        damages = [0, 37, 39, 40, 42, 43, 45, 57, 58, 60, 61, 63, 64, 66, 67]
        helper(p1_result, damages, 0, 2, "ヘドロばくだん")

        damages = [0, 7, 8, 9, 11, 12, 13]
        helper(p1_result, damages, 0, 2, "ギガドレイン")

        """p1のリザードンからp2のフシギバナへのダメージ確率分布"""
        damages = [0, 133, 135, 140, 143, 148, 151, 156, 198, 203, 205, 211, 213, 218, 221, 226, 229, 234]
        helper(p1_result, damages, 1, 2, "かえんほうしゃ")

        """p1のリザードンからp2のカメックスへのダメージ確率分布"""
        damages = [0, 55, 56, 57, 58, 60, 61, 62, 64, 65, 82, 83, 84, 86, 87, 88, 90, 91, 92, 94, 95, 96, 97]
        helper(p1_result, damages, 1, 0, "りゅうのはどう")

        """p2のカメックスからp1のカメックスへのダメージ確率分布"""
        damages = [0, 37, 38, 39, 40, 41, 42, 43, 44, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]
        helper(p2_result, damages, 0, 2, "あくのはどう")

        """p2のリザードンからp1のリザードンへのダメージ確率分布"""
        damages = [0, 86, 87, 90, 91, 94, 95, 97, 99, 101, 129, 130, 133, 134, 136, 138, 140, 142, 144, 146, 148, 149, 152]
        helper(p2_result, damages, 1, 1, "エアスラッシュ")

if __name__ == "__main__":
    unittest.main()
