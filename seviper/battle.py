import copy
import seviper.parts as parts

class Pokemon:
    def __init__(self, name, nature, ability, gender, item, move_names, point_ups, individual, effort):
        assert name in base_data.ALL_POKE_NAMES, "ポケモン名が不適"
        assert nature in base_data.NATUREDEX, "性格が不適"
        poke_data = base_data.POKEDEX[name]
        assert ability in poke_data.AllAbilities, "特性が不適"
        assert gender in parts.valid_genders(poke_data.Gender), "性別が不適"
        assert item in base_data.ALL_ITEMS, "アイテムが不適"
        assert all([move_name in poke_data.learnset for move_name in move_names]), "覚えさせる技が不適"
        assert all([parts.is_valid_point_up(point_up) for point_up in point_ups]), "ポイントアップのリストの中に不適な値が含まれている"
        assert len(move_names) == len(point_ups), "覚えさせる技の数とポイントアップのリストの長さが一致していない"
        assert parts.MIN_MOVESET_NUM <= len(move_names) <= parts.MAX_MOVESET_NUM, "覚えさせる技の数が不適"

        assert parts.is_valid_individual_value(individual.hp), "HP個体値が不適"
        assert parts.is_valid_individual_value(individual.atk), "攻撃個体値が不適"
        assert parts.is_valid_individual_value(individual.defe), "防御個体値が不適"
        assert parts.is_valid_individual_value(individual.sp_atk), "特攻個体値が不適"
        assert parts.is_valid_individual_value(individual.sp_def), "特防個体値が不適"
        assert parts.is_valid_individual_value(individual.speed), "素早さ個体値が不適"

        assert parts.is_valid_effort_value(effort.hp), "HP努力値が不適"
        assert parts.is_valid_effort_value(effort.atk), "攻撃努力値が不適"
        assert parts.is_valid_effort_value(effort.defe), "防御努力値が不適"
        assert parts.is_valid_effort_value(effort.sp_atk), "特攻努力値が不適"
        assert parts.is_valid_effort_value(effort.sp_def), "特防努力値が不適"
        assert parts.is_valid_effort_value(effort.speed), "素早さ努力値が不適"
        assert effort.is_valid_sum(), "努力値の合計値が不正"

        self.name = name
        self.nature = nature
        self.ability = ability
        self.gender = gender
        self.item = item
        self.moveset = {move_name:PowerPoint(base_data.MOVEDEX[move_name].base_pp, point_ups[i]) \
                        for i in enumerate(move_names)}
        self.types = poke_data.types

        hp = parts.hp_state_calc(poke_data.base_hp, individual.hp, effort.hp)
        self.max_hp = hp
        self.current_hp = hp
        self.atk = parts.state_calc(poke_data.base_atk, individual.atk, effort.atk)
        self.defe = parts.state_calc(poke_data.base_def, individual.defe, effort.defe)
        self.sp_atk = parts.state_calc(poke_data.base_sp_atk, individual.sp_atk, effort.sp_atk)
        self.sp_def = parts.state_calc(poke_data.base_sp_def, individual.sp_def, effort.sp_def)
        self.speed = parts.state_calc(poke_data.base_speed, individual.speed, effort.speed)

        self.atk_rank = 0
        self.def_rank = 0
        self.sp_atk_rank = 0
        self.sp_def_rank = 0
        self.speed_rank = 0
        self.accuracy_rank = 0
        self.evasion_rank = 0

        self.status_ailment = ""
        self.bad_poison_elapsed_turn = 0
        self.choice_move_name = ""

        self.is_roots = False
        self.is_leech_seed = False

    def __eq__(self, pokemon):
        is_equal_moveset = all(
            [(move_name in pokemon.moveset) and (self.moveset[move_name] == pokemon.moveset[move_name]) \
             for move_name, power_point in self.moveset.items()]
        )
        is_equal_types = all([type_ in pokemon.types for type_ in self.types])

        d = [
            self.name == pokemon.name,
            self.nature == pokemon.nature,
            self.ability == pokemon.ability,
            self.gender == pokemon.gender,
            self.item == pokemon.item,
            is_equal_moveset,

            self.max_hp == pokemon.max_hp,
            self.current_hp == pokemon.current_hp,
            self.atk == pokemon.atk,
            self.defe == pokemon.defe,
            self.sp_atk == pokemon.sp_atk,
            self.sp_def == pokemon.sp_def,
            self.speed == pokemon.speed,

            self.individual == pokemon.individual,
            self.effort == pokemon.effort,
            is_equal_types,

            self.atk_rank == pokemon.atk_rank,
            self.def_rank == pokemon.def_rank,
            self.sp_atk_rank == pokemon.sp_atk_rank,
            self.sp_def_rank == pokemon.sp_def_rank,
            self.speed_rank == pokemon.speed_rank,

            self.status_ailment == pokemon.status_ailment,
            self.choice_move_name == pokemon.choice_move_name,
            self.is_roots == pokemon.is_roots,
            self.is_leech_seed == pokemon.is_leech_seed,
        ]

        return all(d)

    def is_full_hp(self):
        return self.max_hp == self.current_hp

    def is_faint(self):
        return self.current_hp <= 0

    def is_faint_damage(damage):
        return damage >= self.current_hp

MIN_TEAM_NUM = 3
MAX_TEAM_NUM = 6

def team_validation(team):
    assert MIN_TEAM_NUM <= len(team) <= MAX_TEAM_NUM, "チームの数が不適"
    items = [pokemon.item for pokemon in team]
    assert all([items.count(pokemon.item) == 1 for pokemon in team]), "同じアイテムを持ったポケモンがいる"

FIGHTERS_NUM = 3

def new_fighters(team, indices):
    assert all([indices.count(index) == 1 for index in indices]), "同じポケモンは選出出来ない"
    return [team[indices] for index in indices]

def is_hit(percent):
    return random.randint(0, 100) < percent

class SelfPointOfViewBattle:
    def __init__(self, self_fighters, opponent_fighters):
        self.self_fighters = self_fighters
        self.opponent_fighters = opponent_fighters

    def reverse(self):
        self = copy.deepcopy(self)
        return SelfPointOfViewBattle(self.opponent_fighters, self.self_fighters)

    def to_battle(self):
        self = copy.deepcopy(self)
        return Battle(self.self_fighters, self.opponent_fighters)

    def real_accuracy(self, move_name):
        if move_name == "どくどく" and parts.POISON in self_fighters[0].types:
            return 100
        else:
            move_data = base_data.MOVEDEX[move_name]
            return move_data.accuracy

    def toxic(self):
        if self.opponent_fighters[0].status_ailment != "":
            return self

        if (POISON in self.opponent_fighters[0].types) or (STEEL in self.opponent_fighters[0].types):
            return self

        self = copy.deepcopy(self)
        self.opponent_fighters[0].status_ailment = BAD_POISON
        return self

    def leech_seed(self):
        if parts.GRASS in self.opponent_fighters[0].types:
            return self

        self.opponent_fighters[0].is_leech_seed = True
        return self

    def is_critical(self, move_name):
        return random.randint(0, 24) == 0

    def damage(self, damage_v):
        damage_v = min([self.self_fighters[0].current_hp, damage_v])
        self = copy.deepcopy(self)
        self.self_fighters[0].current_hp -= damage_v
        return self

    def heal(self, heal_v):
        heal_v = min([self.self_fighters[0].faint_damage(), heal_v])
        self = copy.deepcopy(self)
        self.self_fighters[0].current_hp += heal_v
        return self

    def move_use(self, move_name):
        lead_poke_name = self.self_fighters[0].name
        assert not self_fighters[0].is_faint(), lead_poke_name + " は " + "技を繰り出そうとしたが、瀕死状態"

        self = copy.deepcopy(self)
        if move_name == parts.STRUGGLE:
            self.self_fighters[0].current_hp = 0
            return self

        move_data = base_data.MOVEDEX[move_name]

        assert move_name in self.self_fighters[0].moveset, \
            lead_poke_name + " は " + move_name + " を繰り出そうとしたが、覚えていない"

        assert self.self_fighters[0].moveset[move_name].current > 0, \
            lead_poke_name + " は " + move_name + " を繰り出そうとしたが、PPがない"

        self.self_fighters[0].moveset[move_name].current -= 1

        if self.opponent_fighters[0].is_faint():
            if move_data.target != "自分":
                return self

        real_accuracy = self.real_accuracy()
        if real_accuracy != -1:
            if not is_hit(real_accuracy):
                return self

        if move_data.category == parts.STATUS:
            if move_name == "どくどく":
                return self.toxic()
            elif move_name == "やどりぎのタネ":
                return self.leech_seed()
            else:
                return self

        attack_num = random.randint(move_data.min_attack_num, move_data.max_attack_num + 1)

        for i in range(attack_num):
            is_critical = self.is_critical()
            final_damage = damagetools.final_damage(move_name, is_critical)
            opovb = self.reverse()
            opovb = opovb.damage(final_damage)
            self = opovb.reverse()
            if self.self_fighters[0].is_faint() or self.opponent_fighters[0].is_faint():
                break
        return self

    def switch(self, poke_name):
        poke_names = [pokemon.name for pokemon in self.self_fighters]
        index = poke_names.index(poke_name)

        assert index != 0, poke_name + "に交代しようとしたが、既に場に出ている"
        assert index in [1, 2], poke_name + "に交代しようとしたが、存在していない"
        assert self.self_fighters[index].is_faint(), poke_name + "に交代しようとしたが、瀕死状態"

        self = copy.deepcopy(self)
        self.self_fighters[0].bad_poison_elapsed_turn = 0
        self.self_fighters[0].is_leech_seed = False

        tmp_self_fighters = self.self_fighters

        if index == 1:
            self.self_fighters[0] = tmp_self_fighters[1]
            self.self_fighters[1] = tmp_self_fighters[0]
            self.self_fighters[2] = tmp_self_fighters[2]
        else:
            self.self_fighters[0] = tmp_self_fighters[2]
            self.self_fighters[1] = tmp_self_fighters[1]
            self.self_fighters[2] = tmp_self_fighters[0]
        return self

    def action(self, command):
        if command in ALL_POKE_NAMES:
            return self.switch(command)
        elif command in ALL_MOVE_NAMES:
            return self.move_use(command)
        assert False, "アクションコマンドが不適"


class Winner:
    def __init__(self, is_p1, is_p2):
        self.is_p1 = is_p1
        self.is_p2 = is_p2

    def __eq__(self, winner):
        return (self.is_p1 == winner.is_p1) and (self.is_p2 == winner.is_p2)

    def __ne__(self, winner):
        return not self.__eq__(winner)

WINNER_P1 = Winner(True, False)
WINNER_P2 = Winner(False, True)
DRAW = Winner(False, False)


def real_speed_winner(spovb):
    p1_real_speed = real_speed(spovb)
    p2_real_speed = real_speed(spovb)

    if p1_real_speed > p2_real_speed:
        return WINNER_P1
    elif p1_real_speed < p2_real_speed:
        return WINNER_P2
    else:
        return DRAW

def priority_winner(spovb, p1_action_command, p2_action_command):
    def priority_rank(action_command):
        if action_command in ALL_MOVE_NAMES:
            return MOVEDEX[action_command].priority_rank
        elif action_command in ALL_POKE_NAMES:
            return 999
        assert False, "アクションコマンドが不適"

    p1_priority_rank = priority_rank(p1_action_command)
    p2_priority_rank = priority_rank(p2_action_command)

    if p1_priority_rank > p2_priority_rank:
        return WINNER_P1
    elif p1_priority_rank < p2_priority_rank:
        return WINNER_P2
    else:
        return DRAW

def action_speed_winner(spovb, p1_action_command, p2_action_command):
    real_speed_winner_v = real_speed_winner(spovb)
    if real_speed_winner != DRAW:
        return real_speed_winner_v

    priority_winner_v = priority_winner(spovb, p1_action_command, p2_action_command)
    if priority_winner_v != DRAW:
        return priority_winner_v

    return random.choice([WINNER_P1, WINNER_P2])

#https://wiki.xn--rckteqa2e.com/wiki/%E3%81%99%E3%81%B0%E3%82%84%E3%81%95

INIT_SPEED_BONUS = 4096

def speed_bonus(spovb):
    result = INIT_SPEED_BONUS
    if spovb.self_fighters[0].item == "こだわりスカーフ":
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def real_speed(spovb):
    speed = spovb.self_fighters[0].speed
    rank_bonus = RANK_BONUS[spovb.self_fighters[0].speed_rank]
    speed_bonus_v = speed_bonus(spovb)
    paralysis_bonus = PARALYSIS_BONUS[spovb.self_fighters[0].status_ailment == PARALYSIS]

    result = int(float(speed) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(speed_bonus_v) / 4096.0)
    return result

PARALYSIS_BONUS = {True:2048.0 / 4096.0, False:1.0}


class Battle:
    def __init__(self, p1_fighters, p2_fighters):
        self.p1_fighters = p1_fighters
        self.p2_fighters = p2_fighters

    def reverse(self):
        self = copy.deepcopy(self)
        return Battle(self.p2_fighters, self.p1_fighters)

    def to_p1_point_of_view_battle(self):
        self = copy.deepcopy(self)
        return SelfPointOfViewBattle(self.p1_fighters, self.p2_fighters)

    def to_p2_point_of_view_battle(self):
        self = copy.deepcopy(self)
        return SelfPointOfViewBattle(self.p2_fighters, self.p1_fighters)

    def p1_action(self, command):
        p1_point_of_view_battle = self.to_p1_point_of_view_battle()
        p1_point_of_view_battle = p1_point_of_view_battle.action(command)
        self = p1_point_of_view_battle.to_battle()
        return self

    def p2_action(self, command):
        p2_point_of_view_battle = self.to_p2_point_of_view_battle()
        p2_point_of_view_battle = p2_point_of_view_battle.action(command)
        self = p2_point_of_view_battle.to_battle()
        return self

    def is_p1_only_switch_after_faint_phase(self):
        return self.p1_fighters[0].is_faint() and not self.p2_fighters[0].is_faint()

    def is_p2_only_switch_after_faint_phase(self):
        return not self.p1_fighters[0].is_faint() and self.p2_fighters[0].is_faint()

    def is_p1_and_p2_phase(self):
        return self.p1_fighters[0].is_faint() == self.p2_fighters[0].is_faint()

    def turn_end(self):
        def p1_first(spovb, turn_end_f):
            p1_point_of_view_battle = spovb.to_p1_point_of_view_battle()
            p1_point_of_view_battle = turn_end_f(p1_point_of_view_battle)
            p2_point_of_view_battle = p1_point_of_view_battle.reverse()
            p2_point_of_view_battle = turn_end_f(p2_point_of_view_battle)
            p1_point_of_view_battle = p2_point_of_view_battle.reverse()
            return p1_point_of_view_battle.to_battle()

        def p2_first(spovb, turn_end_f):
            p2_point_of_view_battle = spovb.to_p2_point_of_view_battle()
            p2_point_of_view_battle = turn_end_f(p2_point_of_view_battle)
            p1_point_of_view_battle = p2_point_of_view_battle.reverse()
            p1_point_of_view_battle = turn_end_f(p1_point_of_view_battle)
            return p1_point_of_view_battle.to_battle()

        def run(self, turn_end_fs):
            real_speed_winner_v = self.real_speed_winner()
            for turn_end_f in turn_end_fs:
                if real_speed_winner_v == WINNER_P1:
                    self = p1_first(self, turn_end_f)
                elif real_speed_winner_v == WINNER_P2:
                    self = p2_first(self, turn_end_f)
                else:
                    if is_hit(50):
                        self = p1_first(self, turn_end_f)
                    else:
                        self = p2_first(self, turn_end_f)
            return self

        self = run(self, [turn_end.leftovers, turn_end.black_sludge])
        self = run(self, [turn_end.leech_seed])
        self = run(self, [turn_end.bad_poison])
        return self

    def push(self, action_commands):
        is_p1_only_switch_after_faint_phase = self.is_p1_only_switch_after_faint_phase()
        is_p2_only_switch_after_faint_phase = self.is_p2_only_switch_after_faint_phase()

        if is_p1_only_switch_after_faint_phase:
            assert len(action_commands) == 1, "p1のみアクションが可能な状態で、2つのコマンドが渡された"
        elif is_p2_only_switch_after_faint_phase:
            assert len(action_commands) == 1, "p2のみアクションが可能な状態で、2つのコマンドが渡された"
        else:
            assert len(action_commands) == 2, "p1とp2の両方がアクション可能な状態で、1つのコマンドしか渡されなかった"

        if is_p1_only_switch_after_faint_phase:
            return self.p1_action(action_commands[0])
        elif is_p2_only_switch_after_faint_phase:
            return self.p2_action(action_commands[0])
        elif self.is_p1_and_p2_phase() and self.p1_fighters[0].is_faint():
            self = self.p1_action(action_commands[0])
            self = self.p2_action(action_commands[1])
            return self

        action_speed_winner_v = self.action_speed_winner(action_co)
        if action_speed_winner_v == WINNER_P1:
            is_p1_actions = [True, False]
        else:
            is_p2_actions = [False, True]

        for is_p1_action in is_p1_actions:
            if is_p1_action:
                self = self.p1_action(action_commands[0])
            else:
                self = self.p2_action(action_commands[1])

        return self.turn_end()

    def is_game_end(self):
        is_p1_all_faint = all([pokemon.is_faint() for pokemon in self.p1_fighters])
        is_p2_all_faint = all([pokemon.is_faint() for pokemon in self.p2_fighters])
        return is_p1_all_faint or is_p2_all_faint

    def one_game(self, trainer1, trainer2):
        while True:
            if self.is_p1_and_p2_phase():
                p1_action_command = trainer1(self)
                p2_action_command = trainer2(self)
                action_commands = [p1_action_command, p2_action_command]
            elif self.is_p1_only_switch_after_faint_phase():
                action_commands = [trainer1(self)]
            else:
                action_commands = [trainer2(self)]

            self = self.run(action_commands)
            if self.is_game_end():
                break
        return self

if __name__ == "__main__":
    for i in range(parts.RATE_POKE_NAMES_LENGTH):
        row, column = PokemonFeatureValue2D.INDICES_2D[i]
        print(i, row, column)

    #pokemon_feature_value_2d.set_name("サンダー")
    #print(pokemon_feature_value_2d.name)
