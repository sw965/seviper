import unittest
import random
import seviper

class Pokemon(unittest.TestCase):
    def test_template_venusaur(self):
        venusaur = seviper.TEMPLATE_POKEMONS["フシギバナ"]()
        self.assertEqual(venusaur.max_hp, 187)
        self.assertEqual(venusaur.atk, 91)
        self.assertEqual(venusaur.defe, 103)
        self.assertEqual(venusaur.sp_atk, 120)
        self.assertEqual(venusaur.sp_def, 167)
        self.assertEqual(venusaur.speed, 101)
        self.assertEqual(venusaur.nature, "おだやか")
        self.assertEqual(venusaur.moveset["ギガドレイン"].max, 16)

    def test_template_charizard(self):
        charizard = seviper.TEMPLATE_POKEMONS["リザードン"]()
        self.assertEqual(charizard.speed, 167)
        self.assertEqual(charizard.max_hp, 154)
        self.assertEqual(charizard.atk, 93)
        self.assertEqual(charizard.defe, 98)
        self.assertEqual(charizard.sp_atk, 161)
        self.assertEqual(charizard.sp_def, 105)
        self.assertEqual(charizard.moveset["オーバーヒート"].max, 8)

    def test_template_blastoise(self):
        blastoise = seviper.TEMPLATE_POKEMONS["カメックス"]()
        self.assertEqual(blastoise.max_hp, 155)
        self.assertEqual(blastoise.atk, 92)
        self.assertEqual(blastoise.defe, 120)
        self.assertEqual(blastoise.sp_atk, 150)
        self.assertEqual(blastoise.sp_def, 125)
        self.assertEqual(blastoise.speed, 130)
        self.assertEqual(blastoise.moveset["からをやぶる"].max, 24)

class Battle(unittest.TestCase):
    def test_damage(self):
        p1_fighters = [seviper.TEMPLATE_POKEMONS["フシギバナ"](),
                       seviper.TEMPLATE_POKEMONS["リザードン"](),
                       seviper.TEMPLATE_POKEMONS["カメックス"]()]
        p2_fighters = [seviper.TEMPLATE_POKEMONS["カメックス"](),
                       seviper.TEMPLATE_POKEMONS["リザードン"](),
                       seviper.TEMPLATE_POKEMONS["フシギバナ"]()]

        test_num = 1280

        def test1():
            battle = seviper.Battle(seviper.Fighters(p1_fighters), seviper.Fighters(p2_fighters))
            results = [battle.push({"p1":"ギガドレイン", "p2":"なみのり"}) for _ in range(test_num)]

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

        test1()

    def test_all_damage_probability_distribution(self):
        p1_fighters = [seviper.TEMPLATE_POKEMONS["フシギバナ"](),
                       seviper.TEMPLATE_POKEMONS["リザードン"](),
                       seviper.TEMPLATE_POKEMONS["カメックス"]()]
        p2_fighters = [seviper.TEMPLATE_POKEMONS["カメックス"](),
                       seviper.TEMPLATE_POKEMONS["リザードン"](),
                       seviper.TEMPLATE_POKEMONS["フシギバナ"]()]

        battle = seviper.Battle(p1_fighters, p2_fighters)
        all_dpd = battle.all_damage_probability_distribution()
        p1_attack_dpd = all_dpd["p1_attack"]
        p2_attack_dpd = all_dpd["p2_attack"]

        def helper(result, damages, p1_fighter_i, p2_fighter_i, move_name):
            damage_keys = list(result[p1_fighter_i][p2_fighter_i][move_name].keys())
            self.assertTrue(all([damage in damages for damage in damage_keys]))
            self.assertTrue(all([damage in damage_keys for damage in damages]))
            self.assertTrue(len(damages) == len(damage_keys))

        """p1のフシギバナからp2のカメックスへのダメージ確率分布"""
        damages = [0, 84, 86, 90, 92, 96, 98, 122, 126, 128, 132, 134, 138, 140, 144, 146]
        helper(p1_attack_dpd, damages, 0, 0, "ギガドレイン")

        damages = [0, 51, 52, 54, 55, 57, 58, 60, 76, 78, 79, 81, 82, 84, 85, 87, 88, 90]
        helper(p1_attack_dpd, damages, 0, 0, "ヘドロばくだん")

        damages = [None]
        helper(p1_attack_dpd, damages, 0, 0, "やどりぎのタネ")

        damages = [None]
        helper(p1_attack_dpd, damages, 0, 0, "どくどく")

        """p1のフシギバナからp2のリザードンへのダメージ確率分布"""
        damages = [0, 58, 60, 61, 63, 64, 66, 67, 69, 70, 88, 90, 91, 93, 94, 96, 97, 99, 100, 102, 103, 105]
        helper(p1_attack_dpd, damages, 0, 1, "ヘドロばくだん")

        damages = [0, 12, 13, 14, 18, 19, 20, 21]
        helper(p1_attack_dpd, damages, 0, 1, "ギガドレイン")

        """p1のフシギバナからp2のフシギバナへのダメージ確率分布"""
        damages = [0, 37, 39, 40, 42, 43, 45, 57, 58, 60, 61, 63, 64, 66, 67]
        helper(p1_attack_dpd, damages, 0, 2, "ヘドロばくだん")

        damages = [0, 7, 8, 9, 11, 12, 13]
        helper(p1_attack_dpd, damages, 0, 2, "ギガドレイン")

        """p1のリザードンからp2のフシギバナへのダメージ確率分布"""
        damages = [0, 133, 135, 140, 143, 148, 151, 156, 198, 203, 205, 211, 213, 218, 221, 226, 229, 234]
        helper(p1_attack_dpd, damages, 1, 2, "かえんほうしゃ")

        """p1のリザードンからp2のカメックスへのダメージ確率分布"""
        damages = [0, 55, 56, 57, 58, 60, 61, 62, 64, 65, 82, 83, 84, 86, 87, 88, 90, 91, 92, 94, 95, 96, 97]
        helper(p1_attack_dpd, damages, 1, 0, "りゅうのはどう")

        """p2のカメックスからp1のカメックスへのダメージ確率分布"""
        damages = [0, 37, 38, 39, 40, 41, 42, 43, 44, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]
        helper(p2_attack_dpd, damages, 0, 2, "あくのはどう")

        """p2のリザードンからp1のリザードンへのダメージ確率分布"""
        damages = [0, 86, 87, 90, 91, 94, 95, 97, 99, 101, 129, 130, 133, 134, 136, 138, 140, 142, 144, 146, 148, 149, 152]
        helper(p2_attack_dpd, damages, 1, 1, "エアスラッシュ")

class BattleWithUI(unittest.TestCase):
    def test(self):
        def random_trainer(battle):
            return random.choice(battle.p1_fighters.legal_action_cmds())

        game_num = 1280

        for i in range(game_num):
            init_battle = seviper.Battle(seviper.Fighters.new_rate_random(), seviper.Fighters.new_rate_random())

            if random.choice([True, False]):
                init_battle.p1_fighters[0].current_hp //= random.choice([2, 3])
                init_battle.p1_fighters[1].current_hp //= random.choice([2, 3])
                init_battle.p1_fighters[2].current_hp //= random.choice([2, 3])

            if random.choice([True, False]):
                init_battle.p2_fighters[0].current_hp //= random.choice([2, 3])
                init_battle.p2_fighters[1].current_hp //= random.choice([2, 3])
                init_battle.p2_fighters[2].current_hp //= random.choice([2, 3])

            init_battle_with_ui = init_battle.to_with_ui()
            seed = random.randint(0, 100000)

            random.seed(seed)
            p1_battles, p2_battles, p1_action_cmds, p2_action_cmds, winner = init_battle.one_game(random_trainer, random_trainer)

            random.seed(seed)
            p1_battles_, p2_battles_, p1_action_cmds_, p2_action_cmds_, ui_history, winner_ = init_battle_with_ui.one_game(random_trainer, random_trainer)

            for j, battle in enumerate(p1_battles):
                battle_ = p1_battles_[j]
                if battle != battle_:
                    print("battle")
                    print(battle)
                    print("battle_")
                    print(battle_)
                    for ui in ui_history:
                        print(ui, "\n")
                self.assertTrue(battle == battle_)

            for k, battle in enumerate(p2_battles):
                battle_ = p2_battles_[k]
                if battle != battle_:
                    print("battle")
                    print(battle)
                    print("battle_")
                    print(battle_)
                    for ui in ui_history:
                        print(ui, "\n")
                self.assertTrue(battle == battle_)

            self.assertEqual(p1_action_cmds, p1_action_cmds_)
            self.assertEqual(p2_action_cmds, p2_action_cmds_)

            if winner != winner_:
                print(winner.is_p1, winner.is_p2, winner_.is_p1, winner_.is_p2)
                for ui in ui_history:
                    print(ui)
                    print("")
            self.assertEqual(winner, winner_)

            print(i)

if __name__ == "__main__":
    unittest.main()
