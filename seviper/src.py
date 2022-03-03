import copy
import random
import itertools
import numpy as np
import seviper.base_data as base_data

ALL_POKE_NAMES = base_data.ALL_POKE_NAMES
ALL_MOVE_NAMES = base_data.ALL_MOVE_NAMES
ALL_MOVE_NAMES_LENGTH = len(ALL_MOVE_NAMES)
HALF_HEAL_MOVE_NAMES = base_data.HALF_HEAL_MOVE_NAMES
ONE_HIT_KO_MOVE_NAMES = base_data.ONE_HIT_KO_MOVE_NAMES
TWO_ATTACK_MOVE_NAMES = base_data.TWO_ATTACK_MOVE_NAMES
MIN_TWO_MAX_FIVE_ATTACK_MOVE_NAMES = base_data.MIN_TWO_MAX_FIVE_ATTACK_MOVE_NAMES
MAX_THREE_ATTACK_MOVE_NAMES = base_data.MAX_THREE_ATTACK_MOVE_NAMES
ALL_NATURES = base_data.ALL_NATURES
ALL_ITEMS = base_data.ALL_ITEMS
ALL_TYPES = base_data.ALL_TYPES

class PokeData:
    def __init__(self, dict_data):
        self.normal_abilities = dict_data["NormalAbilities"]
        self.hidden_ability = dict_data["HiddenAbility"]
        self.all_abilities = dict_data["AllAbilities"]
        self.gender = dict_data["Gender"]
        self.types = dict_data["Types"]

        self.base_hp = dict_data["BaseHP"]
        self.base_atk = dict_data["BaseAtk"]
        self.base_def = dict_data["BaseDef"]
        self.base_sp_atk = dict_data["BaseSpAtk"]
        self.base_sp_def = dict_data["BaseSpDef"]
        self.base_speed = dict_data["BaseSpeed"]

        self.height = dict_data["Height"]
        self.weight = dict_data["Weight"]
        self.egg_groups = dict_data["EggGroups"]
        self.category = dict_data["Category"]
        self.learnset = dict_data["Learnset"]

    def is_rate_battle_ok(self):
        return self.category != "伝説のポケモン" and self.category != "幻のポケモン"

POKEDEX = {k:PokeData(v) for k, v in base_data.POKEDEX.items()}
RATE_POKE_NAMES = [poke_name for poke_name in ALL_POKE_NAMES if POKEDEX[poke_name].is_rate_battle_ok()]
RATE_POKE_NAMES_LENGTH = len(RATE_POKE_NAMES)

ALL_ABILITIES = []
for poke_name in ALL_POKE_NAMES:
    for ability in POKEDEX[poke_name].all_abilities:
        if ability not in ALL_ABILITIES:
            ALL_ABILITIES.append(ability)

MAX_BASE_HP = 0
for poke_data in POKEDEX.values():
    MAX_BASE_HP = max([poke_data.base_hp, MAX_BASE_HP])

MAX_BASE_STATE = 0
for poke_data in POKEDEX.values():
    MAX_BASE_STATE = max([poke_data.base_atk, poke_data.base_def, poke_data.base_sp_atk,
                          poke_data.base_sp_def, poke_data.base_speed, MAX_BASE_STATE])

class MoveData:
    def __init__(self, dict_data):
        self.type = dict_data["Type"]
        self.category = dict_data["Category"]
        self.power = dict_data["Power"]
        self.accuracy = dict_data["Accuracy"]
        self.base_pp = dict_data["BasePP"]
        self.target = dict_data["Target"]

        self.contact = dict_data["Contact"]
        self.protect = dict_data["Protect"]
        self.magic_coat = dict_data["MagicCoat"]
        self.snatch = dict_data["Snatch"]
        self.mirror_move = dict_data["MirrorMove"]
        self.substitute = dict_data["Substitute"]

        self.gigantamax_move = dict_data["GigantamaxMove"]
        self.gigantamax_power = dict_data["GigantamaxPower"]
        self.priority_rank = dict_data["PriorityRank"]
        self.critical_rank = dict_data["CriticalRank"]

        self.min_attack_num = dict_data["MinAttackNum"]
        self.max_attack_num = dict_data["MaxAttackNum"]

MOVEDEX = {k:MoveData(v) for k, v in base_data.MOVEDEX.items()}

MAX_MOVE_POWER = max([MOVEDEX[move_name].power for move_name in ALL_MOVE_NAMES])
MIN_ATTACK_NUM = min([MOVEDEX[move_name].min_attack_num for move_name in ALL_MOVE_NAMES])
MAX_ATTACK_NUM = max([MOVEDEX[move_name].max_attack_num for move_name in ALL_MOVE_NAMES])

PHYSICS = "物理"
SPECIAL = "特殊"
STATUS = "変化"

STRUGGLE = "わるあがき"

def get_sorted_move_names(move_names):
    indices = sorted([ALL_MOVE_NAMES.index(move_name) for move_name in move_names])
    return [ALL_MOVE_NAMES[index] for index in indices]

#https://wiki.xn--rckteqa2e.com/wiki/%E9%80%A3%E7%B6%9A%E6%94%BB%E6%92%83%E6%8A%80
MIN_TWO_MAX_FIVE_ATTACK_PERCENTS = [100, 100, 35, 35, 15, 15]

class NatureData:
    def __init__(self, dict_data):
        self.atk_bonus = dict_data["AtkBonus"]
        self.def_bonus = dict_data["DefBonus"]
        self.sp_atk_bonus = dict_data["SpAtkBonus"]
        self.sp_def_bonus = dict_data["SpDefBonus"]
        self.speed_bonus = dict_data["SpeedBonus"]

NATUREDEX = {k:NatureData(v) for k, v in base_data.NATUREDEX.items()}
TYPEDEX = base_data.TYPEDEX

NORMAL = "ノーマル"
FIRE = "ほのお"
WATER = "みず"
GRASS = "くさ"
ELECTRIC = "でんき"
ICE = "こおり"
FIGHTING = "かくとう"
POISON = "どく"
GROUND = "じめん"
FLYING = "ひこう"
PSYCHIC = "エスパー"
BUG = "むし"
ROCK = "いわ"
GHOST = "ゴースト"
DRAGON = "ドラゴン"
DARK = "あく"
STEEL = "はがね"
FAIRY = "フェアリー"

MALE = "♂"
FEMALE = "♀"
UNKNOWN = "不明"

ALL_GENDERS = [MALE, FEMALE, UNKNOWN]
ALL_GENDERS_LENGTH = len(ALL_GENDERS)

def get_valid_genders(gender_data):
    if gender_data == "♂♀両方":
        return [MALE, FEMALE]
    elif gender_data == "♂のみ":
        return [MALE]
    elif gender_data == "♀のみ":
        return [FEMALE]
    else:
        return [UNKNOWN]

DEFAULT_LEVEL = 50

ALL_INDIVIDUAL_VALUES = [i for i in range(32)]
MIN_INDIVIDUAL_VALUE = min(ALL_INDIVIDUAL_VALUES)
MAX_INDIVIDUAL_VALUE = max(ALL_INDIVIDUAL_VALUES)

class Individual:
    def __init__(self, dict_data):
        self.hp = dict_data["hp"]
        self.atk = dict_data["atk"]
        self.defe = dict_data["defe"]
        self.sp_atk = dict_data["sp_atk"]
        self.sp_def = dict_data["sp_def"]
        self.speed = dict_data["speed"]

ALL_MIN_INDIVIDUAL = Individual({"hp":0, "atk":0, "defe":0, "sp_atk":0, "sp_def":0, "speed":0})
ALL_MAX_INDIVIDUAL = Individual({"hp":31, "atk":31, "defe":31, "sp_atk":31, "sp_def":31, "speed":31})

ALL_EFFORT_VALUES = [i for i in range(253)]
MIN_EFFORT_VALUE = min(ALL_EFFORT_VALUES)
MAX_EFFORT_VALUE = max(ALL_EFFORT_VALUES)
EFFECTIVE_EFFORT_VALUES = [ev for ev in ALL_EFFORT_VALUES if ev%4 == 0]
MAX_SUM_EFFORT = 510

class Effort:
    def __init__(self, dict_data):
        self.hp = dict_data["hp"]
        self.atk = dict_data["atk"]
        self.defe = dict_data["defe"]
        self.sp_atk = dict_data["sp_atk"]
        self.sp_def = dict_data["sp_def"]
        self.speed = dict_data["speed"]

    def sum(self):
        return self.hp + self.atk + self.defe + self.sp_atk + self.sp_def + self.speed

    def is_valid_sum(self):
        return 0 <= self.sum() <= MAX_SUM_EFFORT

ALL_POINT_UPS = [0, 1, 2, 3]
MIN_POINT_UP = min(ALL_POINT_UPS)
MAX_POINT_UP = max(ALL_POINT_UPS)

class PowerPoint:
    def __init__(self, base_pp, point_up):
        max_v = PowerPoint.calc(base_pp, point_up)
        self.max = max_v
        self.current = max_v

    def __eq__(self, power_point):
        return self.max_v == power_point.max_v and self.current == power_point.current

    @staticmethod
    def calc(base_pp, point_up):
        result = (5.0 + float(point_up)) / 5.0
        return int(base_pp * result)

MAX_BASE_PP = max([move_data.base_pp for move_data in MOVEDEX.values()])
MAX_POWER_POINT = PowerPoint.calc(MAX_BASE_PP, MAX_POINT_UP)

MIN_MOVESET_LENGTH = 1
MAX_MOVESET_LENGTH = 4

def calc_hp_state(base_hp, individual_value, effort_value):
    return ((base_hp * 2) + individual_value + (effort_value // 4) ) * DEFAULT_LEVEL // 100 + DEFAULT_LEVEL + 10

def calc_state(base_state, individual_value, effort_value, nature_bonus):
    result = ( (base_state * 2) + individual_value + (effort_value // 4) ) * DEFAULT_LEVEL // 100 + 5
    return int(float(result) * nature_bonus)

MAX_HP = calc_hp_state(MAX_BASE_HP, 31, 252)
MAX_STATE = calc_state(MAX_BASE_STATE, 31, 31, 1.1)

NORMAL_POISON = "どく"
BAD_POISON = "もうどく"
SLEEP = "ねむり"
BURN = "やけど"
PARALYSIS = "まひ"
FREEZE = "こおり"

ALL_STATUS_AILMENT = [
    NORMAL_POISON, BAD_POISON, SLEEP, BURN, PARALYSIS, FREEZE
]

BUILD_POKE_NAME_FEATURES = RATE_POKE_NAMES + ["なし"]
ITEM_FEATURES = ALL_ITEMS + ["なし"]
ITEM_FEATURES_LENGTH = len(ITEM_FEATURES)
BUILD_MOVE_NAME_FEATURES = ALL_MOVE_NAMES + ["なし"]
STATUS_AILMENT_FEATURES = [""] + ALL_STATUS_AILMENT
STATUS_AILMENT_FEATURES_LENGTH = len(STATUS_AILMENT_FEATURES)

class Pokemon:
    def __init__(self, poke_name, nature, ability, gender, item, move_names, point_ups, individual, effort):
        assert poke_name in ALL_POKE_NAMES, "ポケモン名が不適"
        assert nature in ALL_NATURES, "性格が不適"
        poke_data = POKEDEX[poke_name]

        assert ability in poke_data.all_abilities, "特性が不適"
        assert gender in get_valid_genders(poke_data.gender), "性別が不適"
        assert item in ITEM_FEATURES, "アイテムが不適"

        assert MIN_MOVESET_LENGTH <= len(move_names) <= MAX_MOVESET_LENGTH, "覚えさせる技の数が不適"
        assert len(move_names) == len(point_ups), "覚えさせる技の数とポイントアップリストの数が一致していない"

        for move_name in move_names:
            assert move_name in poke_data.learnset, poke_name + " は " + move_name + " を 覚えない"

        for i, point_up in enumerate(point_ups):
            assert MIN_POINT_UP <= point_up <= MAX_POINT_UP, move_names[i] + " の ポイントアップ が 不適"

        assert MIN_INDIVIDUAL_VALUE <= individual.hp <= MAX_INDIVIDUAL_VALUE, "HP個体値が不適"
        assert MIN_INDIVIDUAL_VALUE <= individual.atk <= MAX_INDIVIDUAL_VALUE, "攻撃個体値が不適"
        assert MIN_INDIVIDUAL_VALUE <= individual.defe <= MAX_INDIVIDUAL_VALUE, "防御個体値が不適"
        assert MIN_INDIVIDUAL_VALUE <= individual.sp_atk <= MAX_INDIVIDUAL_VALUE, "特攻個体値が不適"
        assert MIN_INDIVIDUAL_VALUE <= individual.sp_def <= MAX_INDIVIDUAL_VALUE, "特防個体値が不適"
        assert MIN_INDIVIDUAL_VALUE <= individual.speed <= MAX_INDIVIDUAL_VALUE, "素早さ個体値が不適"

        assert MIN_EFFORT_VALUE <= effort.hp <= MAX_EFFORT_VALUE, "HP努力値が不適"
        assert MIN_EFFORT_VALUE <= effort.atk <= MAX_EFFORT_VALUE, "攻撃努力値が不適"
        assert MIN_EFFORT_VALUE <= effort.defe <= MAX_EFFORT_VALUE, "防御努力値が不適"
        assert MIN_EFFORT_VALUE <= effort.sp_atk <= MAX_EFFORT_VALUE, "特攻努力値が不適"
        assert MIN_EFFORT_VALUE <= effort.sp_def <= MAX_EFFORT_VALUE, "特防努力値が不適"
        assert MIN_EFFORT_VALUE <= effort.speed <= MAX_EFFORT_VALUE, "素早さ努力値が不適"
        assert effort.is_valid_sum(), "努力値の合計値が不適"

        nature_data = NATUREDEX[nature]

        self.name = poke_name
        self.nature = nature
        self.ability = ability
        self.gender = gender
        self.item = item

        self.sorted_move_names = get_sorted_move_names(move_names)
        self.moveset = {move_name:PowerPoint(MOVEDEX[move_name].base_pp, point_ups[i]) \
                        for i, move_name in enumerate(move_names)}

        self.types = poke_data.types

        hp = calc_hp_state(poke_data.base_hp, individual.hp, effort.hp)
        self.max_hp = hp
        self.current_hp = hp
        self.atk = calc_state(poke_data.base_atk, individual.atk, effort.atk, nature_data.atk_bonus)
        self.defe = calc_state(poke_data.base_def, individual.defe, effort.defe, nature_data.def_bonus)
        self.sp_atk = calc_state(poke_data.base_sp_atk, individual.sp_atk, effort.sp_atk, nature_data.sp_atk_bonus)
        self.sp_def = calc_state(poke_data.base_sp_def, individual.sp_def, effort.sp_def, nature_data.sp_def_bonus)
        self.speed = calc_state(poke_data.base_speed, individual.speed, effort.speed, nature_data.speed_bonus)

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

    def is_full_hp(self):
        return self.max_hp == self.current_hp

    def is_faint(self):
        return self.current_hp <= 0

    def is_faint_damage(self, damage):
        return damage >= self.current_hp

    def current_damage(self):
        return self.max_hp - self.current_hp

    def nature_feature_list(self):
        nature_data = NATUREDEX[self.nature]
        nature_feature = [nature_data.atk_bonus, nature_data.def_bonus,
                          nature_data.sp_atk_bonus, nature_data.sp_def_bonus, nature_data.speed_bonus]
        return nature_feature

    def ability_feature_list(self):
        poke_data = POKEDEX[self.name]
        ability_feature = [0, 0, 0]
        ability_feature[poke_data.all_abilities.index(self.ability)] = 1
        return ability_feature

    def gender_feature_list(self):
        gender_feature = [0 for _ in range(len(ALL_GENDERS))]
        gender_feature[ALL_GENDERS.index(self.gender)] = 1
        return gender_feature

    def to_feature_array(self):
        poke_name_start = 0
        poke_name_end = RATE_POKE_NAMES_LENGTH

        nature_atk_bonus_start = poke_name_end
        nature_atk_bonus_end = nature_atk_bonus_start + 1

        nature_def_bonus_start = nature_atk_bonus_end
        nature_def_bonus_end = nature_def_bonus_start + 1

        nature_sp_atk_bonus_start = nature_def_bonus_end
        nature_sp_atk_bonus_end = nature_sp_atk_bonus_start + 1

        nature_sp_def_bonus_start = nature_sp_atk_bonus_end
        nature_sp_def_bonus_end = nature_sp_def_bonus_start + 1

        nature_speed_bonus_start = nature_sp_def_bonus_end
        nature_speed_bonus_end = nature_speed_bonus_start + 1

        ability_start = nature_speed_bonus_end
        ability_end = ability_start + 3

        gender_start = ability_end
        gender_end = gender_start + ALL_GENDERS_LENGTH

        item_start = gender_end
        item_end = item_start + ITEM_FEATURES_LENGTH

        move_name_start = item_end
        move_name_end = move_name_start + ALL_MOVE_NAMES_LENGTH

        max_power_point1_start = move_name_end
        max_power_point1_end = max_power_point1_start + 1

        max_power_point2_start = max_power_point1_end
        max_power_point2_end = max_power_point2_start + 1

        max_power_point3_start = max_power_point2_end
        max_power_point3_end = max_power_point3_start + 1

        max_power_point4_start = max_power_point3_end
        max_power_point4_end = max_power_point4_start + 1

        current_power_point1_start = max_power_point4_end
        current_power_point1_end = current_power_point1_start + 1

        current_power_point2_start = current_power_point1_end
        current_power_point2_end = current_power_point2_start + 1

        current_power_point3_start = current_power_point2_end
        current_power_point3_end = current_power_point3_start + 1

        current_power_point4_start = current_power_point3_end
        current_power_point4_end = current_power_point4_start + 1

        max_hp_start = current_power_point4_end
        max_hp_end = max_hp_start + 1

        current_hp_start = max_hp_end
        current_hp_end = current_hp_start + 1

        atk_start = current_hp_end
        atk_end = atk_start + 1

        defe_start = atk_end
        defe_end = defe_start + 1

        sp_atk_start = defe_end
        sp_atk_end = sp_atk_start + 1

        sp_def_start = sp_atk_end
        sp_def_end = sp_def_start + 1

        speed_start = sp_def_end
        speed_end = speed_start + 1

        atk_rank_start = speed_end
        atk_rank_end = atk_rank_start + 1

        def_rank_start = atk_rank_end
        def_rank_end = def_rank_start + 1

        sp_atk_rank_start = def_rank_end
        sp_atk_rank_end = sp_atk_rank_start + 1

        sp_def_rank_start = sp_atk_rank_end
        sp_def_rank_end = sp_def_rank_start + 1

        speed_rank_start = sp_def_rank_end
        speed_rank_end = speed_rank_start + 1

        accuracy_rank_start = speed_rank_end
        accuracy_rank_end = accuracy_rank_start + 1

        evasion_rank_start = accuracy_rank_end
        evasion_rank_end = evasion_rank_start + 1

        status_ailment_start = evasion_rank_end
        status_ailment_end = status_ailment_start + STATUS_AILMENT_FEATURES_LENGTH

        bad_poison_elapsed_turn_start = status_ailment_end
        bad_poison_elapsed_turn_end = bad_poison_elapsed_turn_start + 1

        choice_move_name_start = bad_poison_elapsed_turn_end
        choice_move_name_end = choice_move_name_start + MAX_MOVESET_LENGTH

        is_roots_start = choice_move_name_end
        is_roots_end = is_roots_start + 1

        is_leech_seed_start = is_roots_end
        is_leech_seed_end = is_leech_seed_start + 1

        result = [0 for _ in range(is_leech_seed_end)]

        def input_with_validation(start, end, i, v):
            assert result[start:end][i] == 0
            result[start:end][i] = v

        poke_data = POKEDEX[self.name]
        nature_data = NATUREDEX[self.nature]

        input_with_validation(poke_name_start, poke_name_end, RATE_POKE_NAMES.index(self.name), 1)
        input_with_validation(nature_atk_bonus_start, nature_atk_bonus_end, 0, nature_data.atk_bonus)
        input_with_validation(nature_def_bonus_start, nature_def_bonus_end, 0, nature_data.def_bonus)
        input_with_validation(nature_sp_atk_bonus_start, nature_sp_atk_bonus_end, 0, nature_data.sp_atk_bonus)
        input_with_validation(nature_sp_def_bonus_start, nature_sp_def_bonus_end, 0, nature_data.sp_def_bonus)
        input_with_validation(nature_speed_bonus_start, nature_speed_bonus_end, 0, nature_data.speed_bonus)
        input_with_validation(ability_start, ability_end, poke_data.all_abilities.index(self.ability), 1)
        input_with_validation(gender_start, gender_end, ALL_GENDERS.index(self.gender), 1)
        input_with_validation(item_start, item_end, ITEM_FEATURES.index(self.item), 1)

        max_power_point_starts = [max_power_point1_start, max_power_point2_start, max_power_point3_start, max_power_point4_start]
        max_power_point_ends = [max_power_point1_end, max_power_point2_end, max_power_point3_end, max_power_point4_end]
        current_power_point_starts = [current_power_point1_start, current_power_point2_start,
                                      current_power_point3_start, current_power_point4_start]
        current_power_point_ends = [current_power_point1_end, current_power_point2_end,
                                    current_power_point3_end, current_power_point4_end]

        for i, move_name in enumerate(self.sorted_move_names):
            max_power_point = float(self.moveset[move_name].max)
            input_with_validation(move_name_start, move_name_end, ALL_MOVE_NAMES.index(move_name), 1)
            input_with_validation(max_power_point_starts[i], max_power_point_ends[i], 0,
                                  self.moveset[move_name].max / 10.0)
            input_with_validation(current_power_point_starts[i], current_power_point_ends[i], 0,
                                  float(self.moveset[move_name].current) / max_power_point)

        input_with_validation(max_hp_start, max_hp_end, 0, float(self.max_hp) / 100.0)
        input_with_validation(current_hp_start, current_hp_end, 0, float(self.current_hp) / float(self.max_hp))
        input_with_validation(atk_start, atk_end, 0, float(self.atk) / 100.0)
        input_with_validation(defe_start, defe_end, 0, float(self.defe) / 100.0)
        input_with_validation(sp_atk_start, sp_atk_end, 0, float(self.sp_atk) / 100.0)
        input_with_validation(sp_def_start, sp_def_end, 0, float(self.sp_def) / 100.0)
        input_with_validation(speed_start, speed_end, 0, float(self.speed) / 100.0)

        input_with_validation(atk_rank_start, atk_rank_end, 0, float(self.atk_rank))
        input_with_validation(def_rank_start, def_rank_end, 0, float(self.def_rank))
        input_with_validation(sp_atk_rank_start, sp_atk_rank_end, 0, float(self.sp_atk_rank))
        input_with_validation(sp_def_rank_start, sp_def_rank_end, 0, float(self.sp_def_rank))
        input_with_validation(speed_rank_start, speed_rank_end, 0, float(self.speed_rank))
        input_with_validation(accuracy_rank_start, accuracy_rank_end, 0, float(self.accuracy_rank))
        input_with_validation(evasion_rank_start, evasion_rank_end, 0, float(self.evasion_rank))

        input_with_validation(status_ailment_start, status_ailment_end,
                              STATUS_AILMENT_FEATURES.index(self.status_ailment), 1)
        input_with_validation(bad_poison_elapsed_turn_start, bad_poison_elapsed_turn_end, 0,
                              float(self.bad_poison_elapsed_turn) / 16.0)

        if self.choice_move_name != "":
            input_with_validation(choice_move_name_start, choice_move_name_end,
                                  self.sorted_move_names.index(choice_move_name), 1)

        if self.is_roots:
            input_with_validation(is_roots_start, is_roots_end, 0, 1)

        if self.is_leech_seed:
            input_with_validation(is_leech_seed_start, is_leech_seed_end, 0, 1)

        return np.array(result)

class Team(list):
    MIN_LENGTH = 3
    MAX_LENGTH = 6

    def __init__(self, pokemons):
        assert Team.MIN_LENGTH <= len(team) <= Team.MAX_LENGTH, "チームの数が不適"
        super().__init__(pokemons)

    def assert_item_validation():
        items = [pokemon.item for pokemon in team]
        assert all([items.count(pokemon.item) == 1 for pokemon in team]), "同じアイテムを持ったポケモンがいる"

class Fighters(list):
    LENGTH = 3

    @staticmethod
    def select(team, indices):
        assert all([indices.count(index) == 1 for index in indices]), "同じポケモンは選出出来ない"
        return Fighters([team[indices] for index in indices])

    def is_all_faint(self):
        return all([pokemon.is_faint() for pokemon in self])

    def to_feature_array(self):
        first = self[0].to_feature_array()
        second = self[1].to_feature_array()
        third = self[2].to_feature_array()
        return first, second, third

#https://wiki.xn--rckteqa2e.com/wiki/%E3%83%A9%E3%83%B3%E3%82%AF%E8%A3%9C%E6%AD%A3
RANK_BONUS = {
    -6:2.0 / 8.0,
    -5:2.0 / 7.0,
    -4:2.0 / 6.0,
    -3:2.0 / 5.0,
    -2:2.0 / 4.0,
    -1:2.0 / 3.0,
    0:2.0 / 2.0,
    1:3.0 / 2.0,
    2:4.0 / 2.0,
    3:5.0 / 2.0,
    4:6.0 / 2.0,
    5:7.0 / 2.0,
    6:8.0 / 2.0,
}

def get_real_rank_fluctuation(rank, v):
    if v > 0:
        return min([MAX_RANK - rank, v])
    elif v < 0:
        return max([MIN_RANK - rank, v])
    assert False

def is_hit(percent):
    return random.randint(0, 99) < percent

CRITICAL_BONUS = {True:6144.0 / 4096.0, False:1.0}

#https://latest.pokewiki.net/%E3%83%80%E3%83%A1%E3%83%BC%E3%82%B8%E8%A8%88%E7%AE%97%E5%BC%8F
#小数点以下がが0.5以上ならば、繰り上げ
def five_or_more_rounding(x):
	after_the_decimal_point = float(x) - float(int(x))
	if after_the_decimal_point >= 0.5:
		return int(x + 1)
	else:
		return int(x)

#小数点以下が0.5より大きいならば、繰り上げ
def five_over_rounding(x):
	after_the_decimal_point = float(x) - float(int(x))
	if after_the_decimal_point > 0.5:
		return int(x + 1)
	else:
		return int(x)

INIT_POWER_BONUS = 4096
INIT_PHYSICS_ATTACK_BONUS = 4096
INIT_SPECIAL_ATTACK_BONUS = 4096

def get_final_power(spovb, move_name):
    move_data = MOVEDEX[move_name]
    assert move_data.category != STATUS, \
        "ダメージ計算関連のメソッドは、物理技か変化技の技名でなければならない"

    result = five_over_rounding(float(move_data.power) * float(INIT_POWER_BONUS) / 4096.0)
    return max([result, 1])

def get_physics_attack_bonus(spovb):
    result = INIT_PHYSICS_ATTACK_BONUS
    if spovb.self_fighters[0].item == "こだわりハチマキ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_special_attack_bonus(spovb):
    result = INIT_SPECIAL_ATTACK_BONUS
    if spovb.self_fighters[0].item == "こだわりメガネ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_final_attack(spovb, move_name, is_critical):
    move_data = MOVEDEX[move_name]

    if move_data.category == PHYSICS:
        attack_state = spovb.self_fighters[0].atk
        rank = spovb.self_fighters[0].atk_rank
        attack_bonus = get_physics_attack_bonus(spovb)
    elif move_data.category == SPECIAL:
        attack_state = spovb.self_fighters[0].sp_atk
        rank = spovb.self_fighters[0].sp_atk_rank
        attack_bonus = get_special_attack_bonus(spovb)
    else:
        assert False, "ダメージ計算関連の関数で、変化技の技名が入力された"

    if (rank < 0) and is_critical:
        rank = 0

    rank_bonus = RANK_BONUS[rank]

    result = int(float(attack_state) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(attack_bonus) / 4096.0)
    return max([result, 1])

INIT_PHYSICS_DEFENSE_BONUS = 4096
INIT_SPECIAL_DEFENSE_BONUS = 4096
INIT_DEFENSE_BONUS = 4096

def get_physics_defense_bonus(spovb):
	result = INIT_PHYSICS_DEFENSE_BONUS
	return result

def get_special_defense_bonus(spovb):
    result = INIT_SPECIAL_DEFENSE_BONUS
    if spovb.self_fighters[0].item == "とつげきチョッキ":
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_final_defense(spovb, move_name, is_critical):
    category = MOVEDEX[move_name].category

    if category == PHYSICS:
        defense_state = spovb.self_fighters[0].defe
        rank = spovb.self_fighters[0].def_rank
        defense_bonus = get_physics_defense_bonus(spovb)
    elif category == SPECIAL:
        defense_state = spovb.self_fighters[0].sp_def
        rank = spovb.self_fighters[0].sp_def_rank
        defense_bonus = get_special_defense_bonus(spovb)
    else:
        assert False, "ダメージ計算関連の関数で、変化技の技名が入力された"

    if (rank > 0) and is_critical:
        rank = 0

    rank_bonus = RANK_BONUS[rank]

    result = int(float(defense_state) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(defense_bonus) / 4096.0)
    return max([result, 1])

def get_same_type_attack_bonus(pokemon, move_name):
    move_type = MOVEDEX[move_name].type
    if move_type in pokemon.types:
        return 6144.0 / 4096.0
    else:
        return 1.0

def get_effectiveness_bonus(pokemon, move_name):
    result = 1.0
    move_type = MOVEDEX[move_name].type
    for poke_type in pokemon.types:
        result *= TYPEDEX[move_type][poke_type]
    return result

INIT_DAMAGE_BONUS = 4096

def get_damage_bonus(spovb):
    result = INIT_DAMAGE_BONUS
    if spovb.self_fighters[0].item == "いのちのたま":
        result = five_over_rounding(float(result) * 5324.0 / 4096.0)
    return result

FINAL_DAMAGE_RANDOM_BONUSES = [
    0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0
]

FINAL_DAMAGE_RANDOM_BONUSES_LENGTH = len(FINAL_DAMAGE_RANDOM_BONUSES)

def get_final_damage(spovb, move_name, final_damage_random_bonus, is_critical):
    move_data = MOVEDEX[move_name]
    opovb = spovb.reverse()

    final_power = get_final_power(spovb, move_name)
    final_attack = get_final_attack(spovb, move_name, is_critical)
    final_defense = get_final_defense(opovb, move_name, is_critical)

    critical_bonus = CRITICAL_BONUS[is_critical]
    stab = get_same_type_attack_bonus(spovb.self_fighters[0], move_name)
    effectiveness_bonus = get_effectiveness_bonus(spovb.opponent_fighters[0], move_name)
    damage_bonus = get_damage_bonus(spovb)

    result = DEFAULT_LEVEL*2//5 + 2
    result = int(float(result) * float(final_power) * float(final_attack) / float(final_defense))
    result = result // 50 + 2
    result = five_over_rounding(float(result) * critical_bonus)
    result = int(float(result) * final_damage_random_bonus)
    result = five_over_rounding(float(result) * stab)
    result = int(float(result) * effectiveness_bonus)
    result = five_over_rounding(float(result) * float(damage_bonus) / 4096.0)
    return result

def get_damage_probability_distribution(spovb, move_name):
	critical_n = spovb.critical_n(move_name)
	critical_p = 1.0 / float(critical_n)
	no_critical_p = 1.0 - critical_p
	bool_to_critical_p = {True:critical_p, False:no_critical_p}
	accuracy_p = spovb.real_accuracy(move_name) / 100.0
	final_damage_random_bonus_p = 1.0 / float(FINAL_DAMAGE_RANDOM_BONUSES_LENGTH)

	result = {0:1.0 - accuracy_p}

	for is_critical in [False, True]:
		for final_damage_random_bonus in FINAL_DAMAGE_RANDOM_BONUSES:
			final_damage = get_final_damage(spovb, move_name, final_damage_random_bonus, is_critical)
			p = accuracy_p * final_damage_random_bonus_p * bool_to_critical_p[is_critical]

			if final_damage not in result:
				result[final_damage] = p
			else:
				#確率の加法定理
			    result[final_damage] += p
	return result

class SelfPointOfViewBattle:
    def __init__(self, self_fighters, opponent_fighters):
        self.self_fighters = self_fighters
        self.opponent_fighters = opponent_fighters

    def reverse(self):
        return SelfPointOfViewBattle(self.opponent_fighters, self.self_fighters)

    def to_battle(self):
        return Battle(self.self_fighters, self.opponent_fighters)

    def real_accuracy(self, move_name):
        if move_name == "どくどく" and POISON in self_fighters[0].types:
            return 100
        else:
            move_data = MOVEDEX[move_name]
            return move_data.accuracy

    def critical_n(self, move_name):
        rank = MOVEDEX[move_name].critical_rank
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
        damage_v = min([self.self_fighters[0].current_hp, damage_v])
        self = copy.deepcopy(self)
        self.self_fighters[0].current_hp -= damage_v
        return self

    def heal(self, heal_v):
        heal_v = min([self.self_fighters[0].current_damage(), heal_v])
        self = copy.deepcopy(self)
        self.self_fighters[0].current_hp += heal_v
        return self

    #https://wiki.xn--rckteqa2e.com/wiki/%E9%80%A3%E7%B6%9A%E6%94%BB%E6%92%83%E6%8A%80
    def attack_num(self, move_name):
        if move_name in MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.real_accuracy(move_name)
            attack_num = 0
            for _ in range(3):
                if not is_hit(real_accuracy):
                    break
                attack_num += 1
        elif move_name in MIN_TWO_MAX_FIVE_ATTACK_MOVE_NAMES:
            if self.self_fighters[0].ability == "スキルリンク":
                attack_num = 5
            else:
                attack_num = 0
                for percent in MIN_TWO_MAX_FIVE_ATTACK_PERCENTS[move_name]:
                    if not is_hit(percent):
                        break
                    attack_num += 1
        else:
            move_data = MOVEDEX[move_name]
            attack_num = random.randint(move_data.min_attack_num, move_data.max_attack_num)

        return attack_num

    def move_use(self, move_name):
        if self.self_fighters[0].is_faint():
            return self

        self = copy.deepcopy(self)
        if move_name == STRUGGLE:
            self.self_fighters[0].current_hp = 0
            return self

        lead_poke_name = self.self_fighters[0].name
        move_data = MOVEDEX[move_name]

        assert move_name in self.self_fighters[0].moveset, \
            lead_poke_name + " は " + move_name + " を繰り出そうとしたが、覚えていない"

        assert self.self_fighters[0].moveset[move_name].current > 0, \
            lead_poke_name + " は " + move_name + " を繰り出そうとしたが、PPがない"

        self.self_fighters[0].moveset[move_name].current -= 1

        if self.opponent_fighters[0].is_faint():
            if move_data.target != "自分":
                return self

        if move_name not in MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.real_accuracy(move_name)
            if real_accuracy != -1:
                if not is_hit(real_accuracy):
                    return self

        if move_data.category == STATUS:
            if move_name in HALF_HEAL_MOVE_NAMES:
                return StatusMove.half_heal(self)
            else:
                return STATUS_MOVES[move_name](self)

        attack_num = self.attack_num(move_name)
        if attack_num == 0:
            return self

        for i in range(attack_num):
            final_damage_random_bonus = random.choice(FINAL_DAMAGE_RANDOM_BONUSES)
            is_critical = self.is_critical(move_name)
            final_damage = get_final_damage(self, move_name, final_damage_random_bonus, is_critical)

            opovb = self.reverse()
            opovb = opovb.damage(final_damage)
            self = opovb.reverse()

            if self.self_fighters[0].is_faint() or self.opponent_fighters[0].is_faint():
                break

        if self.self_fighters[0].item == "いのちのたま":
            life_orb_damage = int(float(self.self_fighters[0].max_hp) * 1.0 / 10.0)
            life_orb_damage = max([life_orb_damage, 1])
            self = self.damage(life_orb_damage)
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

class Battle:
    def __init__(self, p1_fighters, p2_fighters):
        self.p1_fighters = p1_fighters
        self.p2_fighters = p2_fighters

    def reverse(self):
        return Battle(self.p2_fighters, self.p1_fighters)

    def to_p1_point_of_view_battle(self):
        return SelfPointOfViewBattle(self.p1_fighters, self.p2_fighters)

    def to_p2_point_of_view_battle(self):
        return SelfPointOfViewBattle(self.p2_fighters, self.p1_fighters)

    def p1_action(self, command):
        p1_point_of_view_battle = self.to_p1_point_of_view_battle()
        p1_point_of_view_battle = p1_point_of_view_battle.action(command)
        self = p1_point_of_view_battle.to_battle()
        return self

    def p2_action(self, command):
        p2_point_of_view_battle = self.to_p2_point_of_view_battle()
        p2_point_of_view_battle = p2_point_of_view_battle.action(command)
        p1_point_of_view_battle = p2_point_of_view_battle.reverse()
        self = p1_point_of_view_battle.to_battle()
        return self

    def is_p1_only_switch_after_faint_phase(self):
        return self.p1_fighters[0].is_faint() and not self.p2_fighters[0].is_faint()

    def is_p2_only_switch_after_faint_phase(self):
        return not self.p1_fighters[0].is_faint() and self.p2_fighters[0].is_faint()

    def is_p1_and_p2_phase(self):
        return self.p1_fighters[0].is_faint() == self.p2_fighters[0].is_faint()

    #https://latest.pokewiki.net/%E3%83%90%E3%83%88%E3%83%AB%E4%B8%AD%E3%81%AE%E5%87%A6%E7%90%86%E3%81%AE%E9%A0%86%E7%95%AA
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
            real_speed_winner = Winner.new_real_speed(self)
            for turn_end_f in turn_end_fs:
                if real_speed_winner == WINNER_P1:
                    self = p1_first(self, turn_end_f)
                elif real_speed_winner == WINNER_P2:
                    self = p2_first(self, turn_end_f)
                else:
                    f = random.choice([p1_first, p2_first])
                    self = f(self, turn_end_f)
            return self

        self = run(self, [TurnEnd.leftovers, TurnEnd.black_sludge])
        self = run(self, [TurnEnd.leech_seed])
        self = run(self, [TurnEnd.bad_poison])
        return self

    def push(self, action_commands):
        is_p1_only_switch_after_faint_phase = self.is_p1_only_switch_after_faint_phase()
        is_p2_only_switch_after_faint_phase = self.is_p2_only_switch_after_faint_phase()

        if is_p1_only_switch_after_faint_phase:
            assert len(action_commands) > 1, "p1のみアクションが可能な状態で、2つ以上のコマンドが渡された"
        elif is_p2_only_switch_after_faint_phase:
            assert len(action_commands) > 1, "p2のみアクションが可能な状態で、2つ以上のコマンドが渡された"
        else:
            assert len(action_commands) == 2, "p1とp2の両方がアクション可能な状態で、長さが2じゃないコマンドリストが渡された"

        if is_p1_only_switch_after_faint_phase:
            return self.p1_action(action_commands[0])
        elif is_p2_only_switch_after_faint_phase:
            return self.p2_action(action_commands[0])
        elif self.is_p1_and_p2_phase() and self.p1_fighters[0].is_faint():
            self = self.p1_action(action_commands[0])
            self = self.p2_action(action_commands[1])
            return self

        action_speed_winner = Winner.new_action_speed(self, action_commands[0], action_commands[1])

        if action_speed_winner == WINNER_P1:
            is_p1_actions = [True, False]
        else:
            is_p1_actions = [False, True]

        for is_p1_action in is_p1_actions:
            if is_p1_action:
                self = self.p1_action(action_commands[0])
            else:
                self = self.p2_action(action_commands[1])
        return self.turn_end()

    def is_game_end(self):
        is_p1_all_faint = self.p1_fighters.is_all_faint()
        is_p2_all_faint = self.p2_fighters.is_all_faint()
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

    def damage_probability_distribution(self):
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
                    for move_name in get_sorted_move_names(fighters1[0].moveset.keys()):
                        if MOVEDEX[move_name].category == STATUS:
                            damage_probability_distribution = {0:1.0}
                        else:
                            spovb = SelfPointOfViewBattle(fighters1, fighters2)
                            damage_probability_distribution = get_damage_probability_distribution(spovb, move_name)
                        tmp[move_name] = damage_probability_distribution
                    result[i].append(tmp)
            return result

        p1_result = get_result(p1_fighterses, p2_fighterses)
        p2_result = get_result(p2_fighterses, p1_fighterses)
        return p1_result, p2_result

    def to_feature_array(self):
        p10, p11, p12 = self.p1_fighters.to_feature_array()
        p20, p21, p22 = self.p2_fighters.to_feature_array()
        dpd = self.damage_probability_distribution()

        for player_i in range(len(damage_probability_distribution):
            for fighters_i in range(FIGHTERS_LENGTH):
                if player_i == 0:
                    fighters = self.p1_fighters
                else:
                    fighters = self.p2_fighters

                for move_name in fighters[fighters_i].sorted_move_names:
                    for damage, percent in dpd[player_i][fighters_i][move_name]:
                        damage = min([damage, MAX_HP])
                        result[damage] = percent
        return result

#https://latest.pokewiki.net/%E3%83%90%E3%83%88%E3%83%AB%E4%B8%AD%E3%81%AE%E5%87%A6%E7%90%86%E3%81%AE%E9%A0%86%E7%95%AA
class TurnEnd:
    @staticmethod
    def leftovers(spovb):
        if spovb.self_fighters[0].item != "たべのこし":
            return spovb

        if spovb.self_fighters[0].is_faint():
            return spovb

        if spovb.self_fighters[0].is_full_hp():
            return spovb

        heal = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 16.0)
        spovb = spovb.heal(heal)
        return spovb

    @staticmethod
    def black_sludge(spovb):
        if spovb.self_fighters[0].item != "くろいヘドロ":
            return spovb

        if spovb.self_fighters[0].is_faint():
            return spovb

        if POISON in spovb.self_fighters[0].types:
            heal = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 16.0)
            spovb = spovb.heal(heal)
        else:
            damage = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 8.0)
            spovb = spovb.damage(damage)
        return spovb

    @staticmethod
    def leech_seed(spovb):
        if spovb.self_fighters[0].is_faint():
            return spovb

        if spovb.opponent_fighters[0].is_faint():
            return spovb

        if not spovb.opponent_fighters[0].is_leech_seed:
            return spovb

        damage = int(float(spovb.opponent_fighters[0].max_hp) * 1.0 / 8.0)
        heal = damage

        opovb = spovb.reverse()
        opovb = opovb.damage(damage)
        spovb = opovb.reverse()
        spovb = spovb.heal(heal)
        return spovb

    @staticmethod
    def bad_poison(spovb):
        if spovb.self_fighters[0].status_ailment != BAD_POISON:
            return spovb

        if spovb.self_fighters[0].bad_poison_elapsed_turn < 16:
            spovb.self_fighters[0].bad_poison_elapsed_turn += 1

        damage = int(float(spovb.self_fighters[0].max_hp) * float(spovb.self_fighters[0].bad_poison_elapsed_turn) / 16.0)
        if damage < 1:
            damage = 1
        return spovb.damage(damage)

class Winner:
    def __init__(self, is_p1, is_p2):
        self.is_p1 = is_p1
        self.is_p2 = is_p2

    def __eq__(self, winner):
        return (self.is_p1 == winner.is_p1) and (self.is_p2 == winner.is_p2)

    def __ne__(self, winner):
        return not self.__eq__(winner)

    @staticmethod
    def new_real_speed(battle):
        p1_point_of_view_battle = battle.to_p1_point_of_view_battle()
        p2_point_of_view_battle = battle.to_p2_point_of_view_battle()

        p1_real_speed = get_real_speed(p1_point_of_view_battle)
        p2_real_speed = get_real_speed(p2_point_of_view_battle)

        if p1_real_speed > p2_real_speed:
            return WINNER_P1
        elif p1_real_speed < p2_real_speed:
            return WINNER_P2
        else:
            return DRAW

    @staticmethod
    def new_action_priority(battle, p1_action_command, p2_action_command):
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

    @staticmethod
    def new_action_speed(battle, p1_action_command, p2_action_command):
        real_speed_winner = Winner.new_real_speed(battle)
        if real_speed_winner != DRAW:
            return real_speed_winner

        priority_winner = Winner.new_priority(battle, p1_action_command, p2_action_command)
        if priority_winner != DRAW:
            return priority_winner

        return random.choice([WINNER_P1, WINNER_P2])

WINNER_P1 = Winner(True, False)
WINNER_P2 = Winner(False, True)
DRAW = Winner(False, False)

#https://wiki.xn--rckteqa2e.com/wiki/%E3%81%99%E3%81%B0%E3%82%84%E3%81%95
INIT_SPEED_BONUS = 4096
PARALYSIS_BONUS = {True:2048.0 / 4096.0, False:1.0}

def get_speed_bonus(spovb):
    result = INIT_SPEED_BONUS
    if spovb.self_fighters[0].item == "こだわりスカーフ":
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_real_speed(spovb):
    speed = spovb.self_fighters[0].speed
    rank_bonus = RANK_BONUS[spovb.self_fighters[0].speed_rank]
    speed_bonus = get_speed_bonus(spovb)
    paralysis_bonus = PARALYSIS_BONUS[spovb.self_fighters[0].status_ailment == PARALYSIS]

    result = int(float(speed) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(speed_bonus) / 4096.0)
    return result

def new_venusaur():
    result = Pokemon("フシギバナ", "おだやか", "しんりょく", "♀", "くろいヘドロ",
                     ["ギガドレイン", "ヘドロばくだん", "やどりぎのタネ", "まもる"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL,
                     Effort({"hp":252, "atk":0, "defe":0, "sp_atk":0, "sp_def":252, "speed":4}))
    return result

def new_charizard():
    result = Pokemon("リザードン", "おくびょう", "もうか", "♂", "いのちのたま",
                     ["かえんほうしゃ", "エアスラッシュ", "りゅうのはどう", "オーバーヒート"], [3, 3, 3, 3],
                      ALL_MAX_INDIVIDUAL,
                      Effort({"hp":4, "atk":0, "defe":0, "sp_atk":252, "sp_def":0, "speed":252}))
    return result

def new_blastoise():
    result = Pokemon("カメックス", "ひかえめ", "げきりゅう", "♂", "オボンのみ",
                     ["からをやぶる", "なみのり", "れいとうビーム", "あくのはどう"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL,
                     Effort({"hp":4, "atk":0, "defe":0, "sp_atk":252, "sp_def":0, "speed":252}))
    return result

TEMPLATE_POKEMONS = {
    "フシギバナ":new_venusaur(),
    "リザードン":new_charizard(),
    "カメックス":new_blastoise()
}

class StatusMove:
    @staticmethod
    def half_heal(spovb):
        spovb = copy.deepcopy(spovb)
        heal = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 2.0)
        return spovb.heal(heal)

    @staticmethod
    def swords_dance(spovb):
        spovb = copy.deepcopy(spovb)
        spovb.self_fighters[0].atk_rank += get_real_rank_fluctuation(spovb.self_fighters[0].atk_rank, 2)
        return spovb

    @staticmethod
    def shell_smash(spovb):
        spovb = copy.deepcopy(spovb)
        spovb.self_fighters[0].atk_rank += get_real_rank_fluctuation(spovb.self_fighters[0].atk_rank, 2)
        spovb.self_fighters[0].sp_atk_rank += get_real_rank_fluctuation(spovb.self_fighters[0].sp_atk_rank, 2)
        spovb.self_fighters[0].speed_rank += get_real_rank_fluctuation(spovb.self_fighters[0].speed_rank, 2)
        spovb.self_fighters[0].def_rank += get_real_rank_fluctuation(spovb.self_fighters[0].def_rank, -1)
        spovb.self_fighters[0].sp_def_rank += get_real_rank_fluctuation(spovb.self_fighters[0].sp_def_rank, -1)
        return spovb

    @staticmethod
    def dragon_dance(spovb):
        spovb = copy.deepcopy(spovb)
        spovb.self_fighters[0].atk_rank += get_real_rank_fluctuation(spovb.self_fighters[0].atk_rank, 1)
        spovb.self_fighters[0].speed_rank += get_real_rank_fluctuation(spovb.self_fighters[0].speed_rank, 1)
        return spovb

    @staticmethod
    def toxic(spovb):
        spovb = copy.deepcopy(spovb)
        if spovb.opponent_fighters[0].status_ailment != "":
            return spovb

        if (POISON in self.opponent_fighters[0].types) or (STEEL in self.opponent_fighters[0].types):
            return self

        spovb = copy.deepcopy(spovb)
        spovb.opponent_fighters[0].status_ailment = BAD_POISON
        return spovb

    @staticmethod
    def leech_seed(spovb):
        spovb = copy.deepcopy(spovb)
        if GRASS in spovb.opponent_fighters[0].types:
            return spovb

        spovb.opponent_fighters[0].is_leech_seed = True
        return spovb

STATUS_MOVES = {
    "つるぎのまい":StatusMove.swords_dance,
    "からをやぶる":StatusMove.shell_smash,
    "りゅうのまい":StatusMove.dragon_dance,
    "どくどく":StatusMove.toxic,
    "やどりぎのタネ":StatusMove.leech_seed,
}
