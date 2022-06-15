import random
import copy
import seviper.base_data as base_data
import seviper.parts as parts
import seviper.damage_tools as dt

STRUGGLE = "わるあがき"
#https://wiki.xn--rckteqa2e.com/wiki/%E9%80%A3%E7%B6%9A%E6%94%BB%E6%92%83%E6%8A%80
MIN_TWO_MAX_FIVE_ATTACK_PERCENTS = [100, 100, 35, 35, 15, 15]

def is_hit(percent):
    return random.randint(0, 99) < percent

def get_real_rank_up_down(rank, v):
    if v > 0:
        return min([parts.MAX_RANK - rank, v])
    elif v < 0:
        return max([parts.MIN_RANK - rank, v])
    assert False

class Team(list):
    MIN_LENGTH = 3
    MAX_LENGTH = 6

    def __init__(self, pokemons):
        super().__init__(pokemons)
        assert Team.MIN_LENGTH <= len(self) <= Team.MAX_LENGTH, "チームの数が不適"

    @staticmethod
    def select_fighters(self, indices):
        assert all([indices.count(index) == 1 for index in indices]), "同じポケモンは選出出来ない"
        return Fighters([self[indices] for index in indices])

class Fighters(list):
    LENGTH = 3

    def __eq__(self, fighters):
        return all([self[i] == fighters[i] for i in range(Fighters.LENGTH)])

    def __ne__(self, fighters):
        return not self.__eq__(fighters)

    @staticmethod
    def new_rate_random():
        rate_poke_names_indices = [i for i in range(base_data.RATE_POKE_NAMES_LENGTH)]
        random.shuffle(rate_poke_names_indices)
        poke_names = [base_data.RATE_POKE_NAMES[index] for index in rate_poke_names_indices[:Fighters.LENGTH]]

        items_indices = [i for i in range(len(base_data.ALL_ITEMS))]
        random.shuffle(items_indices)
        items = [base_data.ALL_ITEMS[index] for index in items_indices[:Fighters.LENGTH]]

        fighters = Fighters([parts.Pokemon.new_random(poke_name) for poke_name in poke_names])
        for i in range(Fighters.LENGTH):
            fighters[i].item = items[i]
        return fighters

    def is_all_faint(self):
        return all([pokemon.is_faint() for pokemon in self])

    def legal_action_cmds(self):
        legal_back_poke_name_action_cmds = [pokemon.name for pokemon in self[1:] if not pokemon.is_faint()]

        if self[0].is_faint():
            return legal_back_poke_name_action_cmds

        if self[0].choice_move_name != "":
            legal_move_name_action_cmds = [self[0].choice_move_name]
        else:
            legal_move_name_action_cmds = self[0].sorted_move_names

        legal_move_name_action_cmds = [move_name for move_name in legal_move_name_action_cmds \
                                           if self[0].moveset[move_name].current > 0]

        if len(legal_move_name_action_cmds) == 0:
            legal_move_name_action_cmds = [STRUGGLE]
        return legal_move_name_action_cmds + legal_back_poke_name_action_cmds

    def two_d_feature_list(self):
        return sum([pokemon.two_d_feature_list() for pokemon in self], [])

class Battle:
    def __init__(self, p1_fighters, p2_fighters):
        self.p1_fighters = p1_fighters
        self.p2_fighters = p2_fighters
        self.turn_num = 1

    def __eq__(self, battle):
        if self.p1_fighters != battle.p1_fighters:
            return False
        elif self.p2_fighters != battle.p2_fighters:
            return False
        else:
            return True

    def __ne__(self, battle):
        return not self.__eq__(battle)

    def __str__(self):
        result = ""
        result += self.p1_fighters[0].name
        result += " " + str(self.p1_fighters[0].current_hp)
        result += "/" + str(self.p1_fighters[0].max_hp)
        result += " @" + self.p1_fighters[0].item + "\n"

        result += self.p2_fighters[0].name
        result += " " + str(self.p2_fighters[0].current_hp)
        result += "/" + str(self.p2_fighters[0].max_hp)
        result += " @" + self.p2_fighters[0].item
        return result

    def reverse(self):
        turn_num = self.turn_num
        battle = Battle(self.p2_fighters, self.p1_fighters)
        battle.turn_num = turn_num
        return battle

    def real_accuracy(self, move_name):
        if move_name == "どくどく" and parts.POISON in self.p1_fighters[0].types:
            return 100
        else:
            move_data = base_data.MOVEDEX[move_name]
            return move_data.accuracy

    def critical_n(self, move_name):
        rank = base_data.MOVEDEX[move_name].critical_rank
        if rank == 0:
            return 24
        elif rank == 1:
            return 8
        elif rank == 2:
            return 2
        else:
            return 1

    def is_critical(self, move_name):
        n = self.critical_n(move_name)
        return random.randint(0, n - 1) == 0

    def damage(self, damage_v):
        assert damage_v > 0
        damage_v = min([self.p1_fighters[0].current_hp, damage_v])
        self = copy.deepcopy(self)
        self.p1_fighters[0].current_hp -= damage_v
        return self

    def heal(self, heal_v):
        assert heal_v > 0
        heal_v = min([self.p1_fighters[0].current_damage(), heal_v])
        self = copy.deepcopy(self)
        self.p1_fighters[0].current_hp += heal_v
        return self

    #https://wiki.xn--rckteqa2e.com/wiki/%E9%80%A3%E7%B6%9A%E6%94%BB%E6%92%83%E6%8A%80
    def attack_num(self, move_name):
        if move_name in base_data.MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.real_accuracy(move_name)
            attack_num = 0
            for _ in range(3):
                if not is_hit(real_accuracy):
                    break
                attack_num += 1
        elif move_name in base_data.MIN_TWO_MAX_FIVE_ATTACK_MOVE_NAMES:
            if self.p1_fighters[0].ability == "スキルリンク":
                attack_num = 5
            else:
                attack_num = 0
                for percent in MIN_TWO_MAX_FIVE_ATTACK_PERCENTS:
                    if not is_hit(percent):
                        break
                    attack_num += 1
        else:
            move_data = base_data.MOVEDEX[move_name]
            attack_num = random.randint(move_data.min_attack_num, move_data.max_attack_num)

        return attack_num

    def move_use(self, move_name):
        if self.p1_fighters[0].is_faint():
            return self

        self = copy.deepcopy(self)

        if move_name == STRUGGLE:
            self.p1_fighters[0].current_hp = 0
            return self

        lead_poke_name = self.p1_fighters[0].name

        assert move_name in self.p1_fighters[0].moveset, \
            lead_poke_name + " は " + move_name + " を繰り出そうとしたが、覚えていない"

        assert self.p1_fighters[0].moveset[move_name].current > 0, \
            lead_poke_name + " は " + move_name + " を繰り出そうとしたが、PPがない"

        move_data = base_data.MOVEDEX[move_name]
        self.p1_fighters[0].moveset[move_name].current -= 1

        if self.p2_fighters[0].is_faint():
            if move_data.target != "自分":
                return self

        if move_name not in base_data.MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.real_accuracy(move_name)
            if real_accuracy != -1:
                if not is_hit(real_accuracy):
                    return self

        if move_data.category == parts.STATUS:
            if move_name in base_data.HALF_HEAL_MOVE_NAMES:
                return StatusMove.half_heal(self)
            elif move_name in STATUS_MOVES:
                return STATUS_MOVES[move_name](self)
            else:
                return self

        attack_num = self.attack_num(move_name)
        if attack_num == 0:
            return self

        for i in range(attack_num):
            random_damage_bonus = random.choice(dt.RANDOM_DAMAGE_BONUSES)
            is_critical = self.is_critical(move_name)
            final_damage = dt.get_final_damage(self, move_name, random_damage_bonus, is_critical)

            if final_damage == 0:
                return self

            self = self.reverse()
            self = self.damage(final_damage)
            self = self.reverse()

            if self.p1_fighters[0].is_faint() or self.p2_fighters[0].is_faint():
                break

        if self.p1_fighters[0].item == "いのちのたま":
            life_orb_damage = int(float(self.p1_fighters[0].max_hp) * 1.0 / 10.0)
            life_orb_damage = max([life_orb_damage, 1])
            self = self.damage(life_orb_damage)
        return self

    def switch(self, poke_name):
        poke_names = [pokemon.name for pokemon in self.p1_fighters]
        index = poke_names.index(poke_name)

        assert index != 0, poke_name + "に交代しようとしたが、既に場に出ている"
        assert index in [1, 2], poke_name + "に交代しようとしたが、存在していない"
        assert not self.p1_fighters[index].is_faint(), poke_name + "に交代しようとしたが、瀕死状態"

        self = copy.deepcopy(self)
        self.p1_fighters[0].bad_poison_elapsed_turn = 0
        self.p1_fighters[0].is_leech_seed = False
        self.p1_fighters[0].atk_rank = 0
        self.p1_fighters[0].def_rank = 0
        self.p1_fighters[0].sp_atk_rank = 0
        self.p1_fighters[0].sp_def_rank = 0
        self.p1_fighters[0].speed_rank = 0
        self.p1_fighters[0].accuracy_rank = 0
        self.p1_fighters[0].evasion_rank = 0
        self.p1_fighters[0].types = base_data.POKEDEX[poke_names[0]].types

        tmp_p1_fighters = copy.deepcopy(self.p1_fighters)

        if index == 1:
            self.p1_fighters[0] = tmp_p1_fighters[1]
            self.p1_fighters[1] = tmp_p1_fighters[0]
            self.p1_fighters[2] = tmp_p1_fighters[2]
        else:
            self.p1_fighters[0] = tmp_p1_fighters[2]
            self.p1_fighters[1] = tmp_p1_fighters[1]
            self.p1_fighters[2] = tmp_p1_fighters[0]
        return self

    def p1_action(self, command):
        if command in base_data.ALL_MOVE_NAMES + [STRUGGLE]:
            return self.move_use(command)
        elif command in base_data.ALL_POKE_NAMES:
            return self.switch(command)
        assert False, "アクションコマンドが不正"

    def p2_action(self, command):
        self = self.reverse()
        if command in base_data.ALL_MOVE_NAMES + [STRUGGLE]:
            self = self.move_use(command)
            return self.reverse()
        elif command in base_data.ALL_POKE_NAMES:
            self = self.switch(command)
            return self.reverse()
        assert False, "アクションコマンドが不正"

    def is_p1_only_switch_after_faint_phase(self):
        return self.p1_fighters[0].is_faint() and not self.p2_fighters[0].is_faint()

    def is_p2_only_switch_after_faint_phase(self):
        return not self.p1_fighters[0].is_faint() and self.p2_fighters[0].is_faint()

    def is_p1_and_p2_switch_after_faint_phase(self):
        return self.p1_fighters[0].is_faint() and self.p2_fighters[0].is_faint()

    def is_p1_and_p2_phase(self):
        #両者の先頭のポケモンが瀕死状態もしくは両者の先頭のポケモンがが瀕死ではない状態ならば
        return self.p1_fighters[0].is_faint() == self.p2_fighters[0].is_faint()

    def p1_legal_action_cmds(self):
        if not self.p1_fighters[0].is_faint() and self.p2_fighters[0].is_faint():
            return []
        return self.p1_fighters.legal_action_cmds()

    def p2_legal_action_cmds(self):
        if self.p1_fighters[0].is_faint() and not self.p2_fighters[0].is_faint():
            return []
        return self.p2_fighters.legal_action_cmds()

    #https://latest.pokewiki.net/%E3%83%90%E3%83%88%E3%83%AB%E4%B8%AD%E3%81%AE%E5%87%A6%E7%90%86%E3%81%AE%E9%A0%86%E7%95%AA
    def turn_end(self):
        def p1_first(battle, turn_end_f):
            battle = turn_end_f(battle)
            battle = battle.reverse()
            battle = turn_end_f(battle)
            battle = battle.reverse()
            return battle

        def p2_first(battle, turn_end_f):
            battle = battle.reverse()
            battle = turn_end_f(battle)
            battle = battle.reverse()
            battle = turn_end_f(battle)
            return battle

        def run(battle, turn_end_fs):
            real_speed_winner = Winner.new_real_speed(self)
            for turn_end_f in turn_end_fs:
                if real_speed_winner == WINNER_P1:
                    battle = p1_first(battle, turn_end_f)
                elif real_speed_winner == WINNER_P2:
                    battle = p2_first(battle, turn_end_f)
                else:
                    f = random.choice([p1_first, p2_first])
                    battle = f(battle, turn_end_f)
            return battle

        self = run(self, [TurnEnd.leftovers, TurnEnd.black_sludge])
        self = run(self, [TurnEnd.leech_seed])
        self = run(self, [TurnEnd.bad_poison])
        return self

    def push(self, action):
        is_p1_only_switch_after_faint_phase = self.is_p1_only_switch_after_faint_phase()
        is_p2_only_switch_after_faint_phase = self.is_p2_only_switch_after_faint_phase()

        if is_p1_only_switch_after_faint_phase:
            assert len(action) == 1 and ("p1" in action), "プレイヤー1のみが行動可能な状態で、不適なコマンドが渡された"
        elif is_p2_only_switch_after_faint_phase:
            assert len(action) == 1 and ("p2" in action), "プレイヤー2のみが行動可能な状態で、不適なコマンドが渡された"
        else:
            assert len(action) == 2 and ("p1" in action) and ("p2" in action), \
                "両プレイヤーが行動可能な状態で、不適なコマンドが渡された"

        if is_p1_only_switch_after_faint_phase:
            return self.p1_action(action["p1"])
        elif is_p2_only_switch_after_faint_phase:
            return self.p2_action(action["p2"])
        elif self.is_p1_and_p2_switch_after_faint_phase():
            self = self.p1_action(action["p1"])
            self = self.p2_action(action["p2"])
            return self

        final_priority = Winner.new_final_priority(self, action["p1"], action["p2"])

        for is_p1_action in {True:[True, False], False:[False, True]}[final_priority == WINNER_P1]:
            if is_p1_action:
                self = self.p1_action(action["p1"])
            else:
                self = self.p2_action(action["p2"])

        if self.is_game_end():
            return self

        self = self.turn_end()
        self.turn_num += 1
        return self

    def is_game_end(self):
        return self.p1_fighters.is_all_faint() or self.p2_fighters.is_all_faint()

    def winner(self):
        is_p1_all_faint = self.p1_fighters.is_all_faint()
        is_p2_all_faint = self.p2_fighters.is_all_faint()
        if is_p1_all_faint and is_p2_all_faint:
            return DRAW
        elif is_p1_all_faint:
            return WINNER_P2
        else:
            return WINNER_P1

    def playout(self, p1_trainer, p2_trainer):
        assert not self.is_game_end()

        while True:
            if self.is_p1_and_p2_phase():
                p1_action_cmd = p1_trainer(self)
                p2_action_cmd = p2_trainer(self.reverse())
                action = {"p1":p1_action_cmd, "p2":p2_action_cmd}
            elif self.is_p1_only_switch_after_faint_phase():
                action = {"p1":p1_trainer(self)}
            else:
                action = {"p2":p2_trainer(self.reverse())}

            self = self.push(action)

            if self.is_game_end():
                break

        is_p1_all_faint = self.p1_fighters.is_all_faint()
        is_p2_all_faint = self.p2_fighters.is_all_faint()

        if is_p1_all_faint and is_p2_all_faint:
            return DRAW
        elif is_p1_all_faint:
            return WINNER_P2
        else:
            return WINNER_P1

    def one_game(self, p1_trainer, p2_trainer):
        assert not self.is_game_end()
        p1_battles = []
        p1_action_cmds = []

        p2_battles = []
        p2_action_cmds = []

        while True:
            reverse_self = self.reverse()
            if self.is_p1_and_p2_phase():
                p1_action_cmd = p1_trainer(self)
                p2_action_cmd = p2_trainer(reverse_self)
                action = {"p1":p1_action_cmd, "p2":p2_action_cmd}

                p1_battles.append(self)
                p1_action_cmds.append(p1_action_cmd)
                p2_battles.append(reverse_self)
                p2_action_cmds.append(p2_action_cmd)
            elif self.is_p1_only_switch_after_faint_phase():
                p1_action_cmd = p1_trainer(self)
                action = {"p1":p1_action_cmd}

                p1_battles.append(self)
                p1_action_cmds.append(p1_action_cmd)
            else:
                p2_action_cmd = p2_trainer(reverse_self)
                action = {"p2":p2_action_cmd}

                p2_battles.append(reverse_self)
                p2_action_cmds.append(p2_action_cmd)

            self = self.push(action)

            if self.is_game_end():
                break

        winner = self.winner()
        return p1_battles, p2_battles, p1_action_cmds, p2_action_cmds, winner

    def damage_probability_distribution(self, move_name):
    	critical_n = self.critical_n(move_name)
    	critical_p = 1.0 / float(critical_n)
    	no_critical_p = 1.0 - critical_p
    	bool_to_critical_p = {True:critical_p, False:no_critical_p}
    	accuracy_p = self.real_accuracy(move_name) / 100.0
    	random_damage_bonus_p = 1.0 / float(dt.RANDOM_DAMAGE_BONUSES_LENGTH)

    	result = {0:1.0 - accuracy_p}

    	for is_critical in [False, True]:
    		for random_damage_bonus in dt.RANDOM_DAMAGE_BONUSES:
    			final_damage = dt.get_final_damage(self, move_name, random_damage_bonus, is_critical)
    			p = accuracy_p * random_damage_bonus_p * bool_to_critical_p[is_critical]

    			if final_damage not in result:
    				result[final_damage] = p
    			else:
    				#確率の加法定理
    			    result[final_damage] += p
    	return result

    def all_damage_probability_distribution(self):
        fighter_indices = [[0, 1, 2], [1, 0, 2], [2, 0, 1]]
        p1_fighterses = [[self.p1_fighters[index] for index in indices] \
                          for indices in fighter_indices]
        p2_fighterses = [[self.p2_fighters[index] for index in indices] \
                          for indices in fighter_indices]

        def get_result(fighterses1, fighterses2):
            result = []
            for i, fighters1 in enumerate(fighterses1):
                result.append([])
                for fighters2 in fighterses2:
                    tmp = {}
                    for move_name in fighters1[0].sorted_move_names:
                        if base_data.MOVEDEX[move_name].category == parts.STATUS:
                            damage_probability_distribution = {None:None}
                        else:
                            battle = Battle(fighters1, fighters2)
                            damage_probability_distribution = battle.damage_probability_distribution(move_name)
                        tmp[move_name] = damage_probability_distribution
                    result[i].append(tmp)
            return result

        p1_result = get_result(p1_fighterses, p2_fighterses)
        p2_result = get_result(p2_fighterses, p1_fighterses)
        return {"p1_attack":p1_result, "p2_attack":p2_result}

    def to_with_ui(self):
        return BattleWithUI(self)

    def two_d_feature_list(self):
        p1_fighters_2d_feature_list = self.p1_fighters.two_d_feature_list()
        p2_fighters_2d_feature_list = self.p2_fighters.two_d_feature_list()
        return p1_fighters_2d_feature_list + p2_fighters_2d_feature_list

#https://latest.pokewiki.net/%E3%83%90%E3%83%88%E3%83%AB%E4%B8%AD%E3%81%AE%E5%87%A6%E7%90%86%E3%81%AE%E9%A0%86%E7%95%AA
class TurnEnd:
    @staticmethod
    def leftovers(battle):
        if battle.p1_fighters[0].item != "たべのこし":
            return battle

        if battle.p1_fighters[0].is_faint():
            return battle

        if battle.p1_fighters[0].is_full_hp():
            return battle

        heal = int(float(battle.p1_fighters[0].max_hp) * 1.0 / 16.0)
        heal = max([heal, 1])
        battle = battle.heal(heal)
        return battle

    @staticmethod
    def black_sludge(battle):
        if battle.p1_fighters[0].item != "くろいヘドロ":
            return battle

        if battle.p1_fighters[0].is_faint():
            return battle

        if parts.POISON in battle.p1_fighters[0].types:
            heal = int(float(battle.p1_fighters[0].max_hp) * 1.0 / 16.0)
            battle = battle.heal(heal)
        else:
            damage = int(float(battle.p1_fighters[0].max_hp) * 1.0 / 8.0)
            battle = battle.damage(damage)
        return battle

    @staticmethod
    def leech_seed(battle):
        if battle.p1_fighters[0].is_faint():
            return battle

        if battle.p2_fighters[0].is_faint():
            return battle

        if not battle.p2_fighters[0].is_leech_seed:
            return battle

        damage = int(float(battle.p2_fighters[0].max_hp) * 1.0 / 8.0)
        damage = max([damage, 1])
        heal = damage

        battle = battle.reverse()
        battle = battle.damage(damage)
        battle = battle.reverse()
        battle = battle.heal(heal)
        return battle

    @staticmethod
    def bad_poison(battle):
        if battle.p1_fighters[0].status_ailment != parts.BAD_POISON:
            return battle

        battle = copy.deepcopy(battle)

        if battle.p1_fighters[0].bad_poison_elapsed_turn < 16:
            battle.p1_fighters[0].bad_poison_elapsed_turn += 1

        damage = int(float(battle.p1_fighters[0].max_hp) * float(battle.p1_fighters[0].bad_poison_elapsed_turn) / 16.0)
        damage = max([damage, 1])
        return battle.damage(damage)

class Winner:
    def __init__(self, is_p1, is_p2):
        self.is_p1 = is_p1
        self.is_p2 = is_p2

    def __eq__(self, winner):
        return (self.is_p1 == winner.is_p1) and (self.is_p2 == winner.is_p2)

    def __ne__(self, winner):
        return not self.__eq__(winner)

    def reverse(self):
        if self == WINNER_P1:
            return WINNER_P2
        elif self == WINNER_P2:
            return WINNER_P1
        else:
            return DRAW

    @staticmethod
    def new_real_speed(battle):
        p1_real_speed = get_real_speed(battle)
        p2_real_speed = get_real_speed(battle.reverse())

        if p1_real_speed > p2_real_speed:
            return WINNER_P1
        elif p1_real_speed < p2_real_speed:
            return WINNER_P2
        else:
            return DRAW

    @staticmethod
    def new_action_priority(battle, p1_action_cmd, p2_action_cmd):
        def priority_rank(action_cmd):
            if action_cmd in base_data.ALL_MOVE_NAMES:
                return base_data.MOVEDEX[action_cmd].priority_rank
            elif action_cmd == STRUGGLE:
                return 0
            elif action_cmd in base_data.ALL_POKE_NAMES:
                return 999
            assert False, "アクションコマンドが不適"

        p1_priority_rank = priority_rank(p1_action_cmd)
        p2_priority_rank = priority_rank(p2_action_cmd)

        if p1_priority_rank > p2_priority_rank:
            return WINNER_P1
        elif p1_priority_rank < p2_priority_rank:
            return WINNER_P2
        else:
            return DRAW

    @staticmethod
    def new_final_priority(battle, p1_action_cmd, p2_action_cmd):
        priority_winner = Winner.new_action_priority(battle, p1_action_cmd, p2_action_cmd)
        if priority_winner != DRAW:
            return priority_winner

        real_speed_winner = Winner.new_real_speed(battle)
        if real_speed_winner != DRAW:
            return real_speed_winner

        return random.choice([WINNER_P1, WINNER_P2])

WINNER_P1 = Winner(True, False)
WINNER_P2 = Winner(False, True)
DRAW = Winner(False, False)

#https://wiki.xn--rckteqa2e.com/wiki/%E3%81%99%E3%81%B0%E3%82%84%E3%81%95
INIT_SPEED_BONUS = 4096
PARALYSIS_BONUS = {True:2048.0 / 4096.0, False:1.0}

def get_speed_bonus(battle):
    result = INIT_SPEED_BONUS
    if battle.p1_fighters[0].item == "こだわりスカーフ":
        result = dt.five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_real_speed(battle):
    speed = battle.p1_fighters[0].speed
    rank_bonus = dt.RANK_BONUS[battle.p1_fighters[0].speed_rank]
    speed_bonus = get_speed_bonus(battle)
    paralysis_bonus = PARALYSIS_BONUS[battle.p1_fighters[0].status_ailment == parts.PARALYSIS]

    result = int(float(speed) * float(rank_bonus))
    result = dt.five_over_rounding(float(result) * float(speed_bonus) / 4096.0)
    return result

class StatusMove:
    @staticmethod
    def half_heal(battle):
        battle = copy.deepcopy(battle)
        heal = int(float(battle.p1_fighters[0].max_hp) * 1.0 / 2.0)
        return battle.heal(heal)

    @staticmethod
    def swords_dance(battle):
        battle = copy.deepcopy(battle)
        battle.p1_fighters[0].atk_rank += get_real_rank_up_down(battle.p1_fighters[0].atk_rank, 2)
        return battle

    @staticmethod
    def shell_smash(battle):
        battle = copy.deepcopy(battle)
        battle.p1_fighters[0].atk_rank += get_real_rank_up_down(battle.p1_fighters[0].atk_rank, 2)
        battle.p1_fighters[0].sp_atk_rank += get_real_rank_up_down(battle.p1_fighters[0].sp_atk_rank, 2)
        battle.p1_fighters[0].speed_rank += get_real_rank_up_down(battle.p1_fighters[0].speed_rank, 2)
        battle.p1_fighters[0].def_rank += get_real_rank_up_down(battle.p1_fighters[0].def_rank, -1)
        battle.p1_fighters[0].sp_def_rank += get_real_rank_up_down(battle.p1_fighters[0].sp_def_rank, -1)
        return battle

    @staticmethod
    def dragon_dance(battle):
        battle = copy.deepcopy(battle)
        battle.p1_fighters[0].atk_rank += get_real_rank_up_down(battle.p1_fighters[0].atk_rank, 1)
        battle.p1_fighters[0].speed_rank += get_real_rank_up_down(battle.p1_fighters[0].speed_rank, 1)
        return battle

    @staticmethod
    def toxic(battle):
        battle = copy.deepcopy(battle)
        if battle.p2_fighters[0].status_ailment != "":
            return battle

        if (parts.POISON in battle.p2_fighters[0].types) or (parts.STEEL in battle.p2_fighters[0].types):
            return battle

        battle = copy.deepcopy(battle)
        battle.p2_fighters[0].status_ailment = parts.BAD_POISON
        return battle

    @staticmethod
    def leech_seed(battle):
        battle = copy.deepcopy(battle)
        if parts.GRASS in battle.p2_fighters[0].types:
            return battle

        battle.p2_fighters[0].is_leech_seed = True
        return battle

STATUS_MOVES = {
    "つるぎのまい":StatusMove.swords_dance,
    "からをやぶる":StatusMove.shell_smash,
    "りゅうのまい":StatusMove.dragon_dance,
    "どくどく":StatusMove.toxic,
    "やどりぎのタネ":StatusMove.leech_seed,
}

class Trainer:
    @staticmethod
    def random_instruction(battle):
        return random.choice(battle.p1_fighters.legal_action_cmds())

class BattleUI:
    def __init__(self, battle_message):
        self.real_p1_poke_name = None
        self.real_p1_level = None
        self.real_p1_gender = None
        self.real_p1_max_hp = None
        self.real_p1_current_hp = None

        self.real_p2_poke_name = None
        self.real_p2_level = None
        self.real_p2_gender = None
        self.real_p2_max_hp = None
        self.real_p2_current_hp = None

        self.battle_message = battle_message

    def __str__(self):
        if self.real_p1_poke_name is None:
            real_p1_poke_name = "None"
        else:
            real_p1_poke_name = self.real_p1_poke_name

        if self.real_p1_level is None:
            str_real_p1_level = "None"
        else:
            str_real_p1_level = str(self.real_p1_level)

        if self.real_p1_gender is None:
            real_p1_gender = "None"
        else:
            real_p1_gender = self.real_p1_gender

        if self.real_p1_current_hp is None:
            str_real_p1_current_hp = "None"
        else:
            str_real_p1_current_hp = str(self.real_p1_current_hp)

        if self.real_p1_max_hp is None:
            str_real_p1_max_hp = "None"
        else:
            str_real_p1_max_hp = str(self.real_p1_max_hp)

        if self.real_p2_poke_name is None:
            real_p2_poke_name = "None"
        else:
            real_p2_poke_name = self.real_p2_poke_name

        if self.real_p2_level is None:
            str_real_p2_level = "None"
        else:
            str_real_p2_level = str(self.real_p2_level)

        if self.real_p2_gender is None:
            real_p2_gender = "None"
        else:
            real_p2_gender = self.real_p2_gender

        if self.real_p2_current_hp is None:
            str_real_p2_current_hp = "None"
        else:
            str_real_p2_current_hp = str(self.real_p2_current_hp)

        if self.real_p2_max_hp is None:
            str_real_p2_max_hp = "None"
        else:
            str_real_p2_max_hp = str(self.real_p2_max_hp)

        result = real_p1_poke_name + " " + str_real_p1_level + " " + real_p1_gender + " " + str_real_p1_current_hp + "/" + str_real_p1_max_hp \
               + "\n" \
               + real_p2_poke_name + " " + str_real_p2_level + " " + real_p2_gender + " " + str_real_p2_current_hp + "/" + str_real_p2_max_hp \
               + "\n" \
               + self.battle_message + "\n"
        return result

OF_SELF = {True:"", False:"相手の "}

class BattleMessage(str):
    def __new__(cls, v):
        self = super().__new__(cls, v)
        return self

    def __init__(self, v):
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == len(self):
            self._i = 0
            raise StopIteration()
        result = self[:self._i + 1]
        self._i += 1
        return result

    @staticmethod
    def new_move_use(poke_name, move_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + " の " + move_name + "!")

    @staticmethod
    def new_no_effective(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + " には 効果がないようだ...")

    @staticmethod
    def new_come_back(poke_name):
        return BattleMessage("戻れ！" + poke_name + "！")

    @staticmethod
    def new_withdrew(poke_name):
        return BattleMessage("相手は " + poke_name + " を 引っ込めた！")

    @staticmethod
    def new_go(poke_name):
        return BattleMessage("行け！" + poke_name + "！")

    @staticmethod
    def new_sent_out(poke_name):
        return BattleMessage("相手は " + poke_name + "を 繰り出した！")

    @staticmethod
    def new_faint(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + " は 倒れた！")

    @staticmethod
    def new_rank_up_down(poke_name, state, fluctuation_v, is_real_p1):
        assert fluctuation_v != 0
        assert parts.MIN_RANK <= fluctuation_v <= parts.MAX_RANK

        h = OF_SELF[is_real_p1] + poke_name + " の " + state

        if fluctuation_v == 1:
            return BattleMessage(h + " が 上がった！")
        elif fluctuation_v == 2:
            return BattleMessage(h + " が ぐ～ん と上がった！")
        elif fluctuation_v > 2:
            return BattleMessage(h + " が ぐぐ～ん と上がった！")
        elif fluctuation_v == -1:
            return BattleMessage(h + "が 下がった！")
        elif fluctuation_v == -2:
            return BattleMessage(h + "が がくんと下がった！")
        else:
            return BattleMessage(h + "が がく～んと下がった！")

    @staticmethod
    def new_after_half_heal(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + " の 体力が 回復した！")

    @staticmethod
    def new_leftovers(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + " は たべのこし で 少し回復した！")

    @staticmethod
    def new_black_sludge(poke_name, is_heal, is_real_p1):
        h = OF_SELF[is_real_p1] + poke_name + " は くろいヘドロ で "

        if is_heal:
            return BattleMessage(h + "少し回復した！")
        else:
            return BattleMessage(h + "ダメージを受けた！")

    @staticmethod
    def new_life_orb_damage(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + " は 命が削られた！")

    @staticmethod
    def new_leech_seed_planting(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + "に やどりぎを植えつけた！")

    @staticmethod
    def new_leech_seed_drain(poke_name, is_real_p1):
        return BattleMessage("やどりぎが " + OF_SELF[is_real_p1] + poke_name + "の 体力を奪う！")

    @staticmethod
    def new_bad_poisoned(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name +  "は 猛毒を あびた！")

    @staticmethod
    def new_bad_poison_damage(poke_name, is_real_p1):
        return BattleMessage(OF_SELF[is_real_p1] + poke_name + "は 毒 で ダメージを受けた")

    def apply_bwu(self, bwu, is_real_p1):
        return [bwu.to_ui(battle_msg, is_real_p1) for battle_msg in self]

GOOD_EFFECTIVE_BATTLE_MESSAGE = BattleMessage("効果 は 抜群だ！")
BAD_EFFECTIVE_BATTLE_MESSAGE = BattleMessage("効果 は いまひとつのようだ...")
MISS_SHOT_BATTLE_MESSAGE = BattleMessage("しかし 外れた！")
FAILURE_BATTLE_MESSAGE = BattleMessage("しかし うまく 決まらなかった！")
CRITICAL_BATTLE_MESSAGE = BattleMessage("急所 に 当たった！")

class BattleWithUI:
    def __init__(self, battle):
        self.battle = battle
        self.hide_real_p1_ui = False
        self.hide_real_p2_ui = False

    def to_ui(self, battle_message, is_real_p1):
        ui = BattleUI(battle_message)

        if is_real_p1:
            real_p1_pokemon = self.battle.p1_fighters[0]
        else:
            real_p1_pokemon = self.battle.p2_fighters[0]

        if is_real_p1:
            real_p2_pokemon = self.battle.p2_fighters[0]
        else:
            real_p2_pokemon = self.battle.p1_fighters[0]

        if not self.hide_real_p1_ui:
            ui.real_p1_poke_name = real_p1_pokemon.name
            ui.real_p1_level = parts.DEFAULT_LEVEL
            ui.real_p1_gender = real_p1_pokemon.gender
            ui.real_p1_max_hp = real_p1_pokemon.max_hp
            ui.real_p1_current_hp = real_p1_pokemon.current_hp

        if not self.hide_real_p2_ui:
            ui.real_p2_poke_name = real_p2_pokemon.name
            ui.real_p2_level = parts.DEFAULT_LEVEL
            ui.real_p2_gender = real_p2_pokemon.gender
            ui.real_p2_max_hp = real_p2_pokemon.max_hp
            ui.real_p2_current_hp = real_p2_pokemon.current_hp

        ui.battle_message = battle_message
        return ui

    def damage(self, damage_v, is_real_p1, ui_history):
        assert damage_v > 0
        damage_v = min([self.battle.p1_fighters[0].current_hp, damage_v])
        battle_message = ui_history[-1].battle_message
        selfs = [copy.deepcopy(self) for _ in range(damage_v)]
        for i in range(damage_v):
            selfs[i].battle.p1_fighters[0].current_hp -= (i + 1)
            ui_history.append(selfs[i].to_ui(battle_message, is_real_p1))

        if len(selfs) == 0:
            return self
        else:
            return selfs[-1]

    def heal(self, heal_v, is_real_p1, ui_history):
        assert heal_v > 0
        heal_v = min([self.battle.p1_fighters[0].current_damage(), heal_v])
        battle_message = ui_history[-1].battle_message
        selfs = [copy.deepcopy(self) for _ in range(heal_v)]
        for i in range(heal_v):
            selfs[i].battle.p1_fighters[0].current_hp += (i + 1)
            ui_history.append(selfs[i].to_ui(battle_message, is_real_p1))

        if len(selfs) == 0:
            return self
        else:
            return selfs[-1]

    def move_use(self, move_name, is_real_p1, ui_history):
        if self.battle.p1_fighters[0].is_faint():
            return self

        p1_poke_name = self.battle.p1_fighters[0].name
        p2_poke_name = self.battle.p2_fighters[0].name
        move_use_battle_message = BattleMessage.new_move_use(p1_poke_name, move_name, is_real_p1)

        if move_name == STRUGGLE:
            for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                ui_history.append(ui)
            self = self.damage(self.battle.p1_fighters[0].current_hp, is_real_p1, ui_history)
            return self

        assert move_name in self.battle.p1_fighters[0].moveset, \
            p1_poke_name + " は " + move_name + " を繰り出そうとしたが、覚えていない"

        assert self.battle.p1_fighters[0].moveset[move_name].current > 0, \
            p1_poke_name + " は " + move_name + " を繰り出そうとしたが、PPがない"

        move_data = base_data.MOVEDEX[move_name]
        self = copy.deepcopy(self)
        self.battle.p1_fighters[0].moveset[move_name].current -= 1

        if self.battle.p2_fighters[0].is_faint():
            if move_data.target != "自分":
                for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                    ui_history.append(ui)

                for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(self, is_real_p1):
                    ui_history.append(ui)
                return self

        if move_name not in base_data.MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.battle.real_accuracy(move_name)
            if real_accuracy != -1:
                if not is_hit(real_accuracy):
                    for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                        ui_history.append(ui)

                    for ui in MISS_SHOT_BATTLE_MESSAGE.apply_bwu(self, is_real_p1):
                        ui_history.append(ui)
                    return self

        if move_data.category == parts.STATUS:
            for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                ui_history.append(ui)

            if move_name in base_data.HALF_HEAL_MOVE_NAMES:
                return StatusMoveWithUI.half_heal(self, is_real_p1, ui_history)
            elif move_name in STATUS_MOVES_WITH_UI:
                return STATUS_MOVES_WITH_UI[move_name](self, is_real_p1, ui_history)
            else:
                for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(self, is_real_p1):
                    ui_history.append(ui)
                return self

        attack_num = self.battle.attack_num(move_name)
        if attack_num == 0:
            return self

        for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
            ui_history.append(ui)

        for i in range(attack_num):
            random_damage_bonus = random.choice(dt.RANDOM_DAMAGE_BONUSES)
            is_critical = self.battle.is_critical(move_name)

            final_damage = dt.get_final_damage(self.battle, move_name, random_damage_bonus, is_critical)

            if final_damage == 0:
                break

            self.battle = self.battle.reverse()
            self = self.damage(final_damage, not is_real_p1, ui_history)
            self.battle = self.battle.reverse()

            if is_critical:
                for ui in CRITICAL_BATTLE_MESSAGE.apply_bwu(self, is_real_p1):
                    ui_history.append(ui)

            if self.battle.p1_fighters[0].is_faint() or self.battle.p2_fighters[0].is_faint():
                break

        effectiveness_bonus = dt.get_effectiveness_bonus(self.battle.p2_fighters[0], move_name)

        if effectiveness_bonus == 0.0:
            effective_battle_message = BattleMessage.new_no_effective(self.battle.p2_fighters[0].name, not is_real_p1)
        if effectiveness_bonus > 1.0:
            effective_battle_message = GOOD_EFFECTIVE_BATTLE_MESSAGE
        elif effectiveness_bonus < 1.0:
            effective_battle_message = BAD_EFFECTIVE_BATTLE_MESSAGE
        else:
            effective_battle_message = BattleMessage("")

        for ui in effective_battle_message.apply_bwu(self, is_real_p1):
            ui_history.append(ui)

        if effectiveness_bonus == 0.0:
            return self

        if self.battle.p1_fighters[0].item == "いのちのたま":
            life_orb_damage = int(float(self.battle.p1_fighters[0].max_hp) * 1.0 / 10.0)
            life_orb_damage = max([life_orb_damage, 1])
            self = self.damage(life_orb_damage, is_real_p1, ui_history)
            for ui in BattleMessage.new_life_orb_damage(p1_poke_name, is_real_p1).apply_bwu(self, is_real_p1):
                ui_history.append(ui)
        return self

    def switch(self, poke_name, is_real_p1, ui_history):
        poke_names = [pokemon.name for pokemon in self.battle.p1_fighters]
        index = poke_names.index(poke_name)

        assert index != 0, poke_name + "に交代しようとしたが、既に場に出ている"
        assert index in [1, 2], poke_name + "に交代しようとしたが、存在していない"
        assert not self.battle.p1_fighters[index].is_faint(), poke_name + "に交代しようとしたが、瀕死状態"

        self = copy.deepcopy(self)
        self.battle.p1_fighters[0].bad_poison_elapsed_turn = 0
        self.battle.p1_fighters[0].is_leech_seed = False
        self.battle.p1_fighters[0].atk_rank = 0
        self.battle.p1_fighters[0].def_rank = 0
        self.battle.p1_fighters[0].sp_atk_rank = 0
        self.battle.p1_fighters[0].sp_def_rank = 0
        self.battle.p1_fighters[0].speed_rank = 0
        self.battle.p1_fighters[0].accuracy_rank = 0
        self.battle.p1_fighters[0].evasion_rank = 0

        if not self.battle.p1_fighters[0].is_faint():
            if is_real_p1:
                for ui in BattleMessage.new_come_back(self.battle.p1_fighters[0].name).apply_bwu(self, True):
                    ui_history.append(ui)
                self.hide_real_p1_ui = True
            else:
                for ui in BattleMessage.new_withdrew(self.battle.p1_fighters[0].name).apply_bwu(self, False):
                    ui_history.append(ui)
                self.hide_real_p2_ui = True

            ui_history.append(self.to_ui(ui_history[-1].battle_message, is_real_p1))

        if is_real_p1:
            go_message = BattleMessage.new_go(poke_name)
        else:
            go_message = BattleMessage.new_sent_out(poke_name)

        for ui in [self.to_ui(battle_msg, is_real_p1) for battle_msg in go_message]:
            ui_history.append(ui)

        tmp_p1_fighters = copy.deepcopy(self.battle.p1_fighters)

        if index == 1:
            self.battle.p1_fighters[0] = tmp_p1_fighters[1]
            self.battle.p1_fighters[1] = tmp_p1_fighters[0]
            self.battle.p1_fighters[2] = tmp_p1_fighters[2]
        else:
            self.battle.p1_fighters[0] = tmp_p1_fighters[2]
            self.battle.p1_fighters[1] = tmp_p1_fighters[1]
            self.battle.p1_fighters[2] = tmp_p1_fighters[0]

        if is_real_p1:
            self.hide_real_p1_ui = False
        else:
            self.hide_real_p2_ui = False

        ui_history.append(self.to_ui(ui_history[-1].battle_message, is_real_p1))
        return self

    def p1_action(self, command, ui_history):
        if command in base_data.ALL_MOVE_NAMES + [STRUGGLE]:
            self = self.move_use(command, True, ui_history)
            return self
        elif command in base_data.ALL_POKE_NAMES:
            return self.switch(command, True, ui_history)
        assert False, "アクションコマンドが不正"

    def p2_action(self, command, ui_history):
        self.battle = self.battle.reverse()
        if command in base_data.ALL_MOVE_NAMES + [STRUGGLE]:
            self = self.move_use(command, False, ui_history)
            self.battle = self.battle.reverse()
            return self
        elif command in base_data.ALL_POKE_NAMES:
            self = self.switch(command, False, ui_history)
            self.battle = self.battle.reverse()
            return self
        assert False, "アクションコマンドが不正"

    def turn_end(self, ui_history):
        def p1_first(bwu, turn_end_f):
            bwu = turn_end_f(bwu, True, ui_history)
            bwu.battle = bwu.battle.reverse()
            bwu = turn_end_f(bwu, False, ui_history)
            bwu.battle = bwu.battle.reverse()
            return bwu

        def p2_first(bwu, turn_end_f):
            bwu = copy.deepcopy(bwu)
            bwu.battle = bwu.battle.reverse()
            bwu = turn_end_f(bwu, False, ui_history)
            bwu.battle = bwu.battle.reverse()
            bwu = turn_end_f(bwu, True, ui_history)
            return bwu

        def run(bwu, turn_end_fs):
            real_speed_winner = Winner.new_real_speed(bwu.battle)

            for turn_end_f in turn_end_fs:
                if real_speed_winner == WINNER_P1:
                    bwu = p1_first(bwu, turn_end_f)
                elif real_speed_winner == WINNER_P2:
                    bwu = p2_first(bwu, turn_end_f)
                else:
                    f = random.choice([p1_first, p2_first])
                    bwu = f(bwu, turn_end_f)
            return bwu

        self = run(self, [TurnEndWithUI.leftovers, TurnEndWithUI.black_sludge])
        self = run(self, [TurnEndWithUI.leech_seed])
        self = run(self, [TurnEndWithUI.bad_poison])
        return self

    def push(self, action, ui_history):
        is_p1_only_switch_after_faint_phase = self.battle.is_p1_only_switch_after_faint_phase()
        is_p2_only_switch_after_faint_phase = self.battle.is_p2_only_switch_after_faint_phase()

        if is_p1_only_switch_after_faint_phase:
            assert len(action) == 1 and ("p1" in action), "プレイヤー1のみが行動可能な状態で、不適なコマンドが渡された"
        elif is_p2_only_switch_after_faint_phase:
            assert len(action) == 1 and ("p2" in action), "プレイヤー2のみが行動可能な状態で、不適なコマンドが渡された"
        else:
            assert len(action) == 2 and ("p1" in action) and ("p2" in action), \
                "両プレイヤーが行動可能な状態で、不適なコマンドが渡された"

        if is_p1_only_switch_after_faint_phase:
            return self.p1_action(action["p1"], ui_history)
        elif is_p2_only_switch_after_faint_phase:
            return self.p2_action(action["p2"], ui_history)
        elif self.battle.is_p1_and_p2_switch_after_faint_phase():
            self = self.p1_action(action["p1"], ui_history)
            self = self.p2_action(action["p2"], ui_history)
            return self

        final_priority = Winner.new_final_priority(self.battle, action["p1"], action["p2"])
        is_p1_faint = False
        is_p2_faint = False

        def p1_faint(self):
            assert not self.hide_real_p1_ui
            nonlocal is_p1_faint
            for ui in BattleMessage.new_faint(self.battle.p1_fighters[0].name, True).apply_bwu(self, True):
                ui_history.append(ui)
            is_p1_faint = True
            self.hide_real_p1_ui = True
            ui_history.append(self.to_ui(ui_history[-1].battle_message, True))

        def p2_faint(self):
            assert not self.hide_real_p2_ui
            nonlocal is_p2_faint
            self.battle = self.battle.reverse()
            for ui in BattleMessage.new_faint(self.battle.p1_fighters[0].name, False).apply_bwu(self, False):
                ui_history.append(ui)
            is_p2_faint = True
            self.hide_real_p2_ui = True
            ui_history.append(self.to_ui(ui_history[-1].battle_message, False))
            self.battle = self.battle.reverse()

        for is_p1_action in {True:[True, False], False:[False, True]}[final_priority == WINNER_P1]:
            if is_p1_action:
                self = self.p1_action(action["p1"], ui_history)
            else:
                self = self.p2_action(action["p2"], ui_history)

            if self.battle.p1_fighters[0].is_faint() and not is_p1_faint:
                p1_faint(self)

            if self.battle.p2_fighters[0].is_faint() and not is_p2_faint:
                p2_faint(self)

        if self.battle.is_game_end():
            return self

        self = self.turn_end(ui_history)

        if self.battle.p1_fighters[0].is_faint() and not is_p1_faint:
            p1_faint(self)

        if self.battle.p2_fighters[0].is_faint() and not is_p2_faint:
            p2_faint(self)

        return self

    def one_game(self, p1_trainer, p2_trainer):
        assert not self.battle.is_game_end()
        p1_battles = []
        p1_action_cmds = []
        p2_battles = []
        p2_action_cmds = []
        ui_history = []

        while True:
            reverse_battle = self.battle.reverse()
            if self.battle.is_p1_and_p2_phase():
                p1_action_cmd = p1_trainer(self.battle)
                p2_action_cmd = p2_trainer(reverse_battle)
                action = {"p1":p1_action_cmd, "p2":p2_action_cmd}

                p1_battles.append(self.battle)
                p2_battles.append(reverse_battle)
                p1_action_cmds.append(p1_action_cmd)
                p2_action_cmds.append(p2_action_cmd)
            elif self.battle.is_p1_only_switch_after_faint_phase():
                p1_action_cmd = p1_trainer(self.battle)
                action = {"p1":p1_action_cmd}

                p1_battles.append(self.battle)
                p1_action_cmds.append(p1_action_cmd)
            else:
                p2_action_cmd = p2_trainer(reverse_battle)
                action = {"p2":p2_action_cmd}

                p2_battles.append(reverse_battle)
                p2_action_cmds.append(p2_action_cmd)

            self = self.push(action, ui_history)

            if self.battle.is_game_end():
                break

        winner = self.battle.winner()
        return p1_battles, p2_battles, p1_action_cmds, p2_action_cmds, ui_history, winner

#https://latest.pokewiki.net/%E3%83%90%E3%83%88%E3%83%AB%E4%B8%AD%E3%81%AE%E5%87%A6%E7%90%86%E3%81%AE%E9%A0%86%E7%95%AA
class TurnEndWithUI:
    @staticmethod
    def leftovers(bwu, is_real_p1, ui_history):
        if bwu.battle.p1_fighters[0].item != "たべのこし":
            return bwu

        if bwu.battle.p1_fighters[0].is_faint():
            return bwu

        if bwu.battle.p1_fighters[0].is_full_hp():
            return bwu

        heal = int(float(bwu.battle.p1_fighters[0].max_hp) * 1.0 / 16.0)
        heal = max([heal, 1])
        bwu = bwu.heal(heal, is_real_p1, ui_history)
        for ui in BattleMessage.new_leftovers(bwu.battle.p1_fighters[0].name, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def black_sludge(bwu, is_real_p1, ui_history):
        if bwu.battle.p1_fighters[0].item != "くろいヘドロ":
            return bwu

        if bwu.battle.p1_fighters[0].is_faint():
            return bwu

        if parts.POISON in bwu.battle.p1_fighters[0].types:
            if bwu.battle.p1_fighters[0].is_full_hp():
                return bwu
            heal = int(float(bwu.battle.p1_fighters[0].max_hp) * 1.0 / 16.0)
            heal = max([heal, 1])
            bwu = bwu.heal(heal, is_real_p1, ui_history)
            is_heal = True
        else:
            damage = int(float(bwu.battle.p1_fighters[0].max_hp) * 1.0 / 8.0)
            damage = max([damage, 1])
            bwu = bwu.damage(damage, is_real_p1, ui_history)
            is_heal = False

        for ui in BattleMessage.new_black_sludge(bwu.battle.p1_fighters[0].name, is_heal, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def leech_seed(bwu, is_real_p1, ui_history):
        if bwu.battle.p1_fighters[0].is_faint():
            return bwu

        if bwu.battle.p2_fighters[0].is_faint():
            return bwu

        if not bwu.battle.p2_fighters[0].is_leech_seed:
            return bwu

        damage = int(float(bwu.battle.p2_fighters[0].max_hp) * 1.0 / 8.0)
        damage = max([damage, 1])
        heal = damage

        bwu.battle = bwu.battle.reverse()
        bwu = bwu.damage(damage, not is_real_p1, ui_history)
        bwu.battle = bwu.battle.reverse()

        bwu = bwu.heal(heal, is_real_p1, ui_history)
        for ui in BattleMessage.new_leech_seed_drain(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def bad_poison(bwu, is_real_p1, ui_history):
        if bwu.battle.p1_fighters[0].status_ailment != parts.BAD_POISON:
            return bwu

        bwu = copy.deepcopy(bwu)

        if bwu.battle.p1_fighters[0].bad_poison_elapsed_turn < 16:
            bwu.battle.p1_fighters[0].bad_poison_elapsed_turn += 1

        damage = int(float(bwu.battle.p1_fighters[0].max_hp) * float(bwu.battle.p1_fighters[0].bad_poison_elapsed_turn) / 16.0)
        damage = max([damage, 1])
        bwu = bwu.damage(damage, is_real_p1, ui_history)
        for ui in BattleMessage.new_bad_poison_damage(bwu.battle.p1_fighters[0].name, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

class StatusMoveWithUI:
    @staticmethod
    def half_heal(bwu, is_real_p1, ui_history):
        if bwu.battle.p1_fighters[0].is_full_hp():
            for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(bwu, is_real_p1):
                ui_history.append(ui)
            return bwu

        heal = int(float(bwu.battle.p1_fighters[0].max_hp) * 1.0 / 2.0)
        bwu = bwu.heal(heal, is_real_p1, ui_history)
        for ui in BattleMessage.new_after_half_heal(bwu.battle.p1_fighters[0].name, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def swords_dance(bwu, is_real_p1, ui_history):
        bwu = copy.deepcopy(bwu)
        atk_rank_up = 2
        bwu.battle.p1_fighters[0].atk_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].atk_rank, atk_rank_up)
        for ui in BattleMessage.new_rank_up_down(bwu.battle.p1_fighters[0].name, "攻撃", atk_rank_up, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def shell_smash(bwu, is_real_p1, ui_history):
        bwu = copy.deepcopy(bwu)

        atk_rank_up = 2
        sp_atk_rank_up = 2
        speed_rank_up = 2
        def_rank_down = -1
        sp_def_rank_down = -1

        bwu.battle.p1_fighters[0].atk_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].atk_rank, atk_rank_up)
        bwu.battle.p1_fighters[0].sp_atk_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].sp_atk_rank, sp_atk_rank_up)
        bwu.battle.p1_fighters[0].speed_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].speed_rank, speed_rank_up)
        bwu.battle.p1_fighters[0].def_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].def_rank, def_rank_down)
        bwu.battle.p1_fighters[0].sp_def_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].sp_def_rank, sp_def_rank_down)

        poke_name = bwu.battle.p1_fighters[0].name
        for ui in BattleMessage.new_rank_up_down(poke_name, "攻撃", atk_rank_up, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)

        for ui in BattleMessage.new_rank_up_down(poke_name, "特攻", sp_atk_rank_up, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)

        for ui in BattleMessage.new_rank_up_down(poke_name, "素早さ", speed_rank_up, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)

        for ui in BattleMessage.new_rank_up_down(poke_name, "防御", def_rank_down, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)

        for ui in BattleMessage.new_rank_up_down(poke_name, "特防", sp_def_rank_down, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def dragon_dance(bwu, is_real_p1, ui_history):
        bwu = copy.deepcopy(bwu)
        atk_rank_up = 1
        speed_rank_up = 1

        bwu.battle.p1_fighters[0].atk_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].atk_rank, atk_rank_up)
        bwu.battle.p1_fighters[0].speed_rank += get_real_rank_up_down(bwu.battle.p1_fighters[0].speed_rank, speed_rank_up)

        poke_name = bwu.battle.p1_fighters[0].name

        for ui in BattleMessage.new_rank_up_down(poke_name, "攻撃", atk_rank_up, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)

        for ui in BattleMessage.new_rank_up_down(poke_name, "素早さ", speed_rank_up, is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)

        return bwu

    @staticmethod
    def toxic(bwu, is_real_p1, ui_history):
        if bwu.battle.p2_fighters[0].status_ailment != "":
            for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(bwu, not is_real_p1):
                ui_history.append(ui)
            return bwu

        if (parts.POISON in bwu.battle.p2_fighters[0].types) or (parts.STEEL in bwu.battle.p2_fighters[0].types):
            for ui in BattleMessage.new_no_effective(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, not is_real_p1):
                ui_history.append(ui)
            return bwu

        bwu = copy.deepcopy(bwu)
        bwu.battle.p2_fighters[0].status_ailment = parts.BAD_POISON
        for ui in BattleMessage.new_bad_poisoned(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def leech_seed(bwu, is_real_p1, ui_history):
        if parts.GRASS in bwu.battle.p2_fighters[0].types:
            for ui in BattleMessage.new_no_effective(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, is_real_p1):
                ui_history.append(ui)
            return bwu

        if bwu.battle.p2_fighters[0].is_leech_seed:
            for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(bwu, is_real_p1):
                ui_history.append(ui)
            return bwu

        bwu = copy.deepcopy(bwu)
        bwu.battle.p2_fighters[0].is_leech_seed = True
        for ui in BattleMessage.new_leech_seed_planting(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

STATUS_MOVES_WITH_UI = {
    "つるぎのまい":StatusMoveWithUI.swords_dance,
    "からをやぶる":StatusMoveWithUI.shell_smash,
    "りゅうのまい":StatusMoveWithUI.dragon_dance,
    "どくどく":StatusMoveWithUI.toxic,
    "やどりぎのタネ":StatusMoveWithUI.leech_seed,
}

assert set(STATUS_MOVES.keys()) == set(STATUS_MOVES_WITH_UI.keys())

IMPLEMENTED_MOVE_NAMES = [move_name for move_name in base_data.ALL_MOVE_NAMES \
                          if base_data.MOVEDEX[move_name].category != parts.STATUS or move_name in base_data.HALF_HEAL_MOVE_NAMES or move_name in STATUS_MOVES]
