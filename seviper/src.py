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
for poke_name in ["ダンバル", "メタモン", "トランセル", "ソーナンス", "サッチムシ",
                  "ミツハニー", "カジッチュ", "キャタピー", "コイキング", "ソーナノ"]:
   del RATE_POKE_NAMES[RATE_POKE_NAMES.index(poke_name)]
del poke_name

RATE_POKE_NAMES_LENGTH = len(RATE_POKE_NAMES)

ALL_ABILITIES = []
for poke_name in ALL_POKE_NAMES:
    for ability in POKEDEX[poke_name].all_abilities:
        if ability not in ALL_ABILITIES:
            ALL_ABILITIES.append(ability)

del poke_name

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

MIN_PRIORITY_RANK = min([move_data.priority_rank for move_data in MOVEDEX.values()])
MAX_PRIORITY_RANK = max([move_data.priority_rank for move_data in MOVEDEX.values()])

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

def gender_data_to_valid_genders(gender_data):
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
        return self.max == power_point.max and self.current == power_point.current

    def __ne__(self, power_point):
        return not self.__eq__(power_point)

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
    @staticmethod
    def new(poke_name, nature, ability, gender, item, move_names, point_ups, individual, effort):
        assert poke_name in ALL_POKE_NAMES, "ポケモン名が不適"
        assert nature in ALL_NATURES, "性格が不適"
        poke_data = POKEDEX[poke_name]

        assert ability in poke_data.all_abilities, "特性が不適"
        assert gender in gender_data_to_valid_genders(poke_data.gender), "性別が不適"
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
        pokemon = Pokemon()

        pokemon.name = poke_name
        pokemon.nature = nature
        pokemon.ability = ability
        pokemon.gender = gender
        pokemon.item = item

        pokemon.sorted_move_names = get_sorted_move_names(move_names)
        pokemon.moveset = {move_name:PowerPoint(MOVEDEX[move_name].base_pp, point_ups[i]) \
                        for i, move_name in enumerate(move_names)}

        pokemon.types = poke_data.types

        hp = calc_hp_state(poke_data.base_hp, individual.hp, effort.hp)
        pokemon.max_hp = hp
        pokemon.current_hp = hp
        pokemon.atk = calc_state(poke_data.base_atk, individual.atk, effort.atk, nature_data.atk_bonus)
        pokemon.defe = calc_state(poke_data.base_def, individual.defe, effort.defe, nature_data.def_bonus)
        pokemon.sp_atk = calc_state(poke_data.base_sp_atk, individual.sp_atk, effort.sp_atk, nature_data.sp_atk_bonus)
        pokemon.sp_def = calc_state(poke_data.base_sp_def, individual.sp_def, effort.sp_def, nature_data.sp_def_bonus)
        pokemon.speed = calc_state(poke_data.base_speed, individual.speed, effort.speed, nature_data.speed_bonus)

        pokemon.atk_rank = 0
        pokemon.def_rank = 0
        pokemon.sp_atk_rank = 0
        pokemon.sp_def_rank = 0
        pokemon.speed_rank = 0
        pokemon.accuracy_rank = 0
        pokemon.evasion_rank = 0

        pokemon.status_ailment = ""
        pokemon.bad_poison_elapsed_turn = 0
        pokemon.choice_move_name = ""

        pokemon.is_roots = False
        pokemon.is_leech_seed = False
        return pokemon

    def __eq__(self, pokemon):
        if self.name != pokemon.name:
            return False
        elif self.nature != pokemon.nature:
            return False
        elif self.ability != pokemon.ability:
            return False
        elif self.gender != pokemon.gender:
            return False
        elif self.item != pokemon.item:
            return False
        elif len(self.sorted_move_names) != len(pokemon.sorted_move_names):
            return False
        elif not all([self.sorted_move_names[i] == pokemon.sorted_move_names[i] for i in range(len(self.sorted_move_names))]):
            return False
        elif not all([self.moveset[move_name] == pokemon.moveset[move_name] for move_name in self.sorted_move_names]):
            return False
        elif len(self.types) != len(pokemon.types):
            return False
        elif not all([type_ in pokemon.types for type_ in self.types]):
            return False
        elif self.max_hp != pokemon.max_hp:
            return False
        elif self.current_hp != pokemon.current_hp:
            return False
        elif self.atk != pokemon.atk:
            return False
        elif self.defe != pokemon.defe:
            return False
        elif self.sp_atk != pokemon.sp_atk:
            return False
        elif self.sp_def != pokemon.sp_def:
            return False
        elif self.speed != pokemon.speed:
            return False
        elif self.atk_rank != pokemon.atk_rank:
            return False
        elif self.def_rank != pokemon.def_rank:
            return False
        elif self.sp_atk_rank != pokemon.sp_atk_rank:
            return False
        elif self.sp_def_rank != pokemon.sp_def_rank:
            return False
        elif self.speed_rank != pokemon.speed_rank:
            return False
        elif self.accuracy_rank != pokemon.accuracy_rank:
            return False
        elif self.evasion_rank != pokemon.evasion_rank:
            return False
        elif self.status_ailment != pokemon.status_ailment:
            return False
        elif self.bad_poison_elapsed_turn != pokemon.bad_poison_elapsed_turn:
            return False
        elif self.choice_move_name != pokemon.choice_move_name:
            return False
        elif self.is_roots != pokemon.is_roots:
            return False
        elif self.is_leech_seed != pokemon.is_leech_seed:
            return False
        else:
            return True

    @staticmethod
    def new_random(poke_name):
        poke_data = POKEDEX[poke_name]
        nature = random.choice(ALL_NATURES)
        ability = random.choice(poke_data.all_abilities)
        gender = random.choice(gender_data_to_valid_genders(poke_data.gender))

        learnset_indices = [i for i in range(len(poke_data.learnset)) if poke_data.learnset[i] in IMPLEMENTED_MOVE_NAMES]
        random.shuffle(learnset_indices)
        learnset_indices_end = min([len(learnset_indices), MAX_MOVESET_LENGTH])
        move_names = [poke_data.learnset[index] for index in learnset_indices[:learnset_indices_end]]
        point_ups = [random.randint(0, MAX_POINT_UP) for _ in range(len(move_names))]

        state_keys = ["hp", "atk", "defe", "sp_atk", "sp_def", "speed"]
        individual_dict = {key:random.randint(0, MAX_INDIVIDUAL_VALUE) for key in state_keys}
        individual = Individual(individual_dict)
        effort_dict = {key:0 for key in state_keys}
        while sum(effort_dict.values()) != MAX_SUM_EFFORT:
            key = random.choice(state_keys)
            if effort_dict[key] < MAX_EFFORT_VALUE:
                effort_dict[key] += 1
        effort = Effort(effort_dict)

        return Pokemon.new(poke_name, nature, ability, gender, "なし", move_names, point_ups, individual, effort)

    def is_full_hp(self):
        return self.max_hp == self.current_hp

    def is_faint(self):
        return self.current_hp <= 0

    def is_faint_damage(self, damage):
        return damage >= self.current_hp

    def current_damage(self):
        return self.max_hp - self.current_hp

    def padding_sorted_move_names(self):
        return self.sorted_move_names + ["なし" for _ in range(MAX_MOVESET_LENGTH - len(self.sorted_move_names))]

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

    def to_feature_list(self):
        poke_name_start = 0

        nature_atk_bonus_start = RATE_POKE_NAMES_LENGTH
        nature_def_bonus_start = nature_atk_bonus_start + 1
        nature_sp_atk_bonus_start = nature_def_bonus_start + 1
        nature_sp_def_bonus_start = nature_sp_atk_bonus_start + 1
        nature_sp_def_bonus_start = nature_sp_def_bonus_start + 1
        nature_speed_bonus_start = nature_sp_def_bonus_start + 1

        ability_start = nature_speed_bonus_start + 1
        gender_start = ability_start + 3
        item_start = gender_start + ALL_GENDERS_LENGTH
        move_name_start = item_start + ITEM_FEATURES_LENGTH
        priority_start = move_name_start + (MAX_PRIORITY_RANK - MIN_PRIORITY_RANK)

        max_power_point1_start = priority_start + ALL_MOVE_NAMES_LENGTH
        max_power_point2_start = max_power_point1_start + 1
        max_power_point3_start = max_power_point2_start + 1
        max_power_point4_start = max_power_point3_start + 1

        current_power_point1_start = max_power_point4_start + 1
        current_power_point2_start = current_power_point1_start + 1
        current_power_point3_start = current_power_point2_start + 1
        current_power_point4_start = current_power_point3_start + 1

        max_hp_start = current_power_point4_start + 1
        current_hp_start = max_hp_start + 1
        atk_start = current_hp_start + 1
        defe_start = atk_start + 1
        sp_atk_start = defe_start + 1
        sp_def_start = sp_atk_start + 1
        speed_start = sp_def_start + 1

        atk_rank_start = speed_start + 1
        def_rank_start = atk_rank_start + 1
        sp_atk_rank_start = def_rank_start + 1
        sp_def_rank_start = sp_atk_rank_start + 1
        speed_rank_start = sp_def_rank_start + 1
        accuracy_rank_start = speed_rank_start + 1
        evasion_rank_start = accuracy_rank_start + 1

        status_ailment_start = evasion_rank_start + 1
        bad_poison_elapsed_turn_start = status_ailment_start + STATUS_AILMENT_FEATURES_LENGTH

        choice_move_name_start = bad_poison_elapsed_turn_start + 1
        is_roots_start = choice_move_name_start + MAX_MOVESET_LENGTH
        is_leech_seed_start = is_roots_start + 1

        result = [0 for _ in range(is_leech_seed_start + 1)]

        def input_with_validation(start, i, v):
            index = start + i
            assert result[index] == 0
            result[index] = v

        poke_data = POKEDEX[self.name]
        nature_data = NATUREDEX[self.nature]

        input_with_validation(poke_name_start, RATE_POKE_NAMES.index(self.name), 1)
        input_with_validation(nature_atk_bonus_start, 0, nature_data.atk_bonus)
        input_with_validation(nature_def_bonus_start, 0, nature_data.def_bonus)
        input_with_validation(nature_sp_atk_bonus_start, 0, nature_data.sp_atk_bonus)
        input_with_validation(nature_sp_def_bonus_start, 0, nature_data.sp_def_bonus)
        input_with_validation(nature_speed_bonus_start, 0, nature_data.speed_bonus)
        input_with_validation(ability_start, poke_data.all_abilities.index(self.ability), 1)
        input_with_validation(gender_start, ALL_GENDERS.index(self.gender), 1)
        input_with_validation(item_start, ITEM_FEATURES.index(self.item), 1)

        max_power_point_starts = [max_power_point1_start, max_power_point2_start, max_power_point3_start, max_power_point4_start]
        current_power_point_starts = [current_power_point1_start, current_power_point2_start,
                                      current_power_point3_start, current_power_point4_start]

        for i, move_name in enumerate(self.sorted_move_names):
            max_power_point = float(self.moveset[move_name].max)
            input_with_validation(move_name_start, ALL_MOVE_NAMES.index(move_name), 1.0)
            input_with_validation(priority_start, 0, float(MOVEDEX[move_name].priority_rank))
            input_with_validation(max_power_point_starts[i], 0, self.moveset[move_name].max / 10.0)
            input_with_validation(current_power_point_starts[i], 0, float(self.moveset[move_name].current) / max_power_point)

        input_with_validation(max_hp_start, 0, float(self.max_hp) / 100.0)
        input_with_validation(current_hp_start, 0, float(self.current_hp) / float(self.max_hp))
        input_with_validation(atk_start, 0, float(self.atk) / 100.0)
        input_with_validation(defe_start, 0, float(self.defe) / 100.0)
        input_with_validation(sp_atk_start, 0, float(self.sp_atk) / 100.0)
        input_with_validation(sp_def_start, 0, float(self.sp_def) / 100.0)
        input_with_validation(speed_start, 0, float(self.speed) / 100.0)

        input_with_validation(atk_rank_start, 0, float(self.atk_rank))
        input_with_validation(def_rank_start, 0, float(self.def_rank))
        input_with_validation(sp_atk_rank_start, 0, float(self.sp_atk_rank))
        input_with_validation(sp_def_rank_start, 0, float(self.sp_def_rank))
        input_with_validation(speed_rank_start, 0, float(self.speed_rank))
        input_with_validation(accuracy_rank_start, 0, float(self.accuracy_rank))
        input_with_validation(evasion_rank_start, 0, float(self.evasion_rank))

        input_with_validation(status_ailment_start, STATUS_AILMENT_FEATURES.index(self.status_ailment), 1)
        input_with_validation(bad_poison_elapsed_turn_start, 0, float(self.bad_poison_elapsed_turn) / 16.0)

        if self.choice_move_name != "":
            input_with_validation(choice_move_name_start, self.sorted_move_names.index(choice_move_name), 1)

        if self.is_roots:
            input_with_validation(is_roots_start, 0, 1)

        if self.is_leech_seed:
            input_with_validation(is_leech_seed_start, 0, 1)
        return result

def new_venusaur():
    result = Pokemon.new("フシギバナ", "おだやか", "しんりょく", "♀", "くろいヘドロ",
                     ["ギガドレイン", "ヘドロばくだん", "やどりぎのタネ", "どくどく"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL,
                     Effort({"hp":252, "atk":0, "defe":0, "sp_atk":0, "sp_def":252, "speed":4}))
    return result

def new_charizard():
    result = Pokemon.new("リザードン", "おくびょう", "もうか", "♂", "いのちのたま",
                     ["かえんほうしゃ", "エアスラッシュ", "りゅうのはどう", "オーバーヒート"], [3, 3, 3, 3],
                      ALL_MAX_INDIVIDUAL,
                      Effort({"hp":4, "atk":0, "defe":0, "sp_atk":252, "sp_def":0, "speed":252}))
    return result

def new_blastoise():
    result = Pokemon.new("カメックス", "ひかえめ", "げきりゅう", "♂", "オボンのみ",
                     ["からをやぶる", "なみのり", "れいとうビーム", "あくのはどう"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL,
                     Effort({"hp":4, "atk":0, "defe":0, "sp_atk":252, "sp_def":0, "speed":252}))
    return result

def new_gyarados():
    result = Pokemon.new("ギャラドス", "いじっぱり", "いかく", "♂", "カゴのみ",
                     ["たきのぼり", "じしん", "こおりのキバ", "りゅうのまい"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL, Effort({"hp":128, "atk":252, "defe":0, "sp_atk":0, "sp_def":0, "speed":128}))
    return result

def new_garchomp():
    result = Pokemon.new("ガブリアス", "ようき", "さめはだ", "♀", "きあいのタスキ",
                     ["じしん", "ドラゴンクロー", "ストーンエッジ", "つるぎのまい"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL, Effort({"hp":4, "atk":252, "defe":0, "sp_atk":0, "sp_def":0, "speed":252}))
    return result

TEMPLATE_POKEMONS = {
    "フシギバナ":new_venusaur,
    "リザードン":new_charizard,
    "カメックス":new_blastoise,
    "ギャラドス":new_gyarados,
    "ガブリアス":new_garchomp
}

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

    def assert_item_validation():
        items = [pokemon.item for pokemon in team]
        assert all([items.count(pokemon.item) == 1 for pokemon in team]), "同じアイテムを持ったポケモンがいる"

class Fighters(list):
    LENGTH = 3

    def __eq__(self, fighters):
        return all([self[i] == fighters[i] for i in range(Fighters.LENGTH)])

    def __ne__(self, fighters):
        return not self.__eq__(fighters)

    @staticmethod
    def new_rate_random():
        rate_poke_names_indices = [i for i in range(RATE_POKE_NAMES_LENGTH)]
        random.shuffle(rate_poke_names_indices)
        poke_names = [RATE_POKE_NAMES[index] for index in rate_poke_names_indices[:Fighters.LENGTH]]

        items_indices = [i for i in range(len(ALL_ITEMS))]
        random.shuffle(items_indices)
        items = [ALL_ITEMS[index] for index in items_indices[:Fighters.LENGTH]]

        fighters = Fighters([Pokemon.new_random(poke_name) for poke_name in poke_names])
        for i in range(Fighters.LENGTH):
            fighters[i].item = items[i]
        return fighters

    def is_all_faint(self):
        return all([pokemon.is_faint() for pokemon in self])

    def legal_action_commands(self):
        legal_back_poke_name_action_commands = [pokemon.name for pokemon in self[1:] if not pokemon.is_faint()]

        if self[0].is_faint():
            return legal_back_poke_name_action_commands

        if self[0].choice_move_name != "":
            legal_move_name_action_commands = [self[0].choice_move_name]
        else:
            legal_move_name_action_commands = self[0].sorted_move_names

        legal_move_name_action_commands = [move_name for move_name in legal_move_name_action_commands \
                                           if self[0].moveset[move_name].current > 0]

        if len(legal_move_name_action_commands) == 0:
            legal_move_name_action_commands = [STRUGGLE]
        return legal_move_name_action_commands + legal_back_poke_name_action_commands

    def to_feature_list(self):
        return [pokemon.to_feature_list() for pokemon in self]

MIN_RANK = -6
MAX_RANK = 6

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

def get_real_rank_up_down(rank, v):
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

def get_final_power(battle, move_name):
    move_data = MOVEDEX[move_name]
    assert move_data.category != STATUS, \
        "ダメージ計算関連のメソッドは、物理技か変化技の技名でなければならない"

    if move_data.power <= 0:
        power = 50
    else:
        power = move_data.power

    result = five_over_rounding(float(power) * float(INIT_POWER_BONUS) / 4096.0)
    return max([result, 1])

def get_physics_attack_bonus(battle):
    result = INIT_PHYSICS_ATTACK_BONUS
    if battle.p1_fighters[0].item == "こだわりハチマキ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_special_attack_bonus(battle):
    result = INIT_SPECIAL_ATTACK_BONUS
    if battle.p1_fighters[0].item == "こだわりメガネ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_final_attack(battle, move_name, is_critical):
    move_data = MOVEDEX[move_name]

    if move_data.category == PHYSICS:
        attack_state = battle.p1_fighters[0].atk
        rank = battle.p1_fighters[0].atk_rank
        attack_bonus = get_physics_attack_bonus(battle)
    elif move_data.category == SPECIAL:
        attack_state = battle.p1_fighters[0].sp_atk
        rank = battle.p1_fighters[0].sp_atk_rank
        attack_bonus = get_special_attack_bonus(battle)
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

def get_physics_defense_bonus(battle):
	result = INIT_PHYSICS_DEFENSE_BONUS
	return result

def get_special_defense_bonus(battle):
    result = INIT_SPECIAL_DEFENSE_BONUS
    if battle.p1_fighters[0].item == "とつげきチョッキ":
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_final_defense(battle, move_name, is_critical):
    category = MOVEDEX[move_name].category

    if category == PHYSICS:
        defense_state = battle.p1_fighters[0].defe
        rank = battle.p1_fighters[0].def_rank
        defense_bonus = get_physics_defense_bonus(battle)
    elif category == SPECIAL:
        defense_state = battle.p1_fighters[0].sp_def
        rank = battle.p1_fighters[0].sp_def_rank
        defense_bonus = get_special_defense_bonus(battle)
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

def get_damage_bonus(battle):
    result = INIT_DAMAGE_BONUS
    if battle.p1_fighters[0].item == "いのちのたま":
        result = five_over_rounding(float(result) * 5324.0 / 4096.0)
    return result

FINAL_DAMAGE_RANDOM_BONUSES = [
    0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0
]

FINAL_DAMAGE_RANDOM_BONUSES_LENGTH = len(FINAL_DAMAGE_RANDOM_BONUSES)

def get_final_damage(battle, move_name, final_damage_random_bonus, is_critical):
    move_data = MOVEDEX[move_name]

    final_power = get_final_power(battle, move_name)
    final_attack = get_final_attack(battle, move_name, is_critical)
    final_defense = get_final_defense(battle.reverse(), move_name, is_critical)

    critical_bonus = CRITICAL_BONUS[is_critical]
    stab = get_same_type_attack_bonus(battle.p1_fighters[0], move_name)
    effectiveness_bonus = get_effectiveness_bonus(battle.p2_fighters[0], move_name)
    damage_bonus = get_damage_bonus(battle)

    result = DEFAULT_LEVEL*2//5 + 2
    result = int(float(result) * float(final_power) * float(final_attack) / float(final_defense))
    result = result // 50 + 2
    result = five_over_rounding(float(result) * critical_bonus)
    result = int(float(result) * final_damage_random_bonus)
    result = five_over_rounding(float(result) * stab)
    result = int(float(result) * effectiveness_bonus)
    result = five_over_rounding(float(result) * float(damage_bonus) / 4096.0)
    return result

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
        if move_name == "どくどく" and POISON in self.p1_fighters[0].types:
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
        if move_name in MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.real_accuracy(move_name)
            attack_num = 0
            for _ in range(3):
                if not is_hit(real_accuracy):
                    break
                attack_num += 1
        elif move_name in MIN_TWO_MAX_FIVE_ATTACK_MOVE_NAMES:
            if self.p1_fighters[0].ability == "スキルリンク":
                attack_num = 5
            else:
                attack_num = 0
                for percent in MIN_TWO_MAX_FIVE_ATTACK_PERCENTS:
                    if not is_hit(percent):
                        break
                    attack_num += 1
        else:
            move_data = MOVEDEX[move_name]
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

        move_data = MOVEDEX[move_name]
        self.p1_fighters[0].moveset[move_name].current -= 1

        if self.p2_fighters[0].is_faint():
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
            elif move_name in STATUS_MOVES:
                return STATUS_MOVES[move_name](self)
            else:
                return self

        attack_num = self.attack_num(move_name)
        if attack_num == 0:
            return self

        for i in range(attack_num):
            final_damage_random_bonus = random.choice(FINAL_DAMAGE_RANDOM_BONUSES)
            is_critical = self.is_critical(move_name)
            final_damage = get_final_damage(self, move_name, final_damage_random_bonus, is_critical)

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
        self.p1_fighters[0].types = POKEDEX[poke_names[0]].types

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
        if command in ALL_MOVE_NAMES + [STRUGGLE]:
            return self.move_use(command)
        elif command in ALL_POKE_NAMES:
            return self.switch(command)
        assert False, "アクションコマンドが不正"

    def p2_action(self, command):
        self = self.reverse()
        if command in ALL_MOVE_NAMES + [STRUGGLE]:
            self = self.move_use(command)
            return self.reverse()
        elif command in ALL_POKE_NAMES:
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

    def playout(self, p1_trainer, p2_trainer):
        assert not self.is_game_end()

        while True:
            if self.is_p1_and_p2_phase():
                p1_action_command = p1_trainer(self)
                p2_action_command = p2_trainer(self.reverse())
                action = {"p1":p1_action_command, "p2":p2_action_command}
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
        s = []
        a = []

        while True:
            if self.is_p1_and_p2_phase():
                p1_action_command = p1_trainer(self)
                p2_action_command = p2_trainer(self.reverse())
                action = {"p1":p1_action_command, "p2":p2_action_command}
            elif self.is_p1_only_switch_after_faint_phase():
                action = {"p1":p1_trainer(self)}
            else:
                action = {"p2":p2_trainer(self.reverse())}

            s.append(self)
            a.append(action)
            self = self.push(action)

            if self.is_game_end():
                break

        is_p1_all_faint = self.p1_fighters.is_all_faint()
        is_p2_all_faint = self.p2_fighters.is_all_faint()

        if is_p1_all_faint and is_p2_all_faint:
            return s, a, DRAW
        elif is_p1_all_faint:
            return s, a, WINNER_P2
        else:
            return s, a, WINNER_P1

    def damage_probability_distribution(self, move_name):
    	critical_n = self.critical_n(move_name)
    	critical_p = 1.0 / float(critical_n)
    	no_critical_p = 1.0 - critical_p
    	bool_to_critical_p = {True:critical_p, False:no_critical_p}
    	accuracy_p = self.real_accuracy(move_name) / 100.0
    	final_damage_random_bonus_p = 1.0 / float(FINAL_DAMAGE_RANDOM_BONUSES_LENGTH)

    	result = {0:1.0 - accuracy_p}

    	for is_critical in [False, True]:
    		for final_damage_random_bonus in FINAL_DAMAGE_RANDOM_BONUSES:
    			final_damage = get_final_damage(self, move_name, final_damage_random_bonus, is_critical)
    			p = accuracy_p * final_damage_random_bonus_p * bool_to_critical_p[is_critical]

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
                        if MOVEDEX[move_name].category == STATUS:
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

    def to_feature_list(self):
        dpd = self.all_damage_probability_distribution()

        def get(attack_fighters, defense_fighters, key):
            result = []
            for attack_i, attack_pokemon in enumerate(attack_fighters):
                for defense_i, defense_pokemon in enumerate(defense_fighters):
                    for move_name in attack_pokemon.padding_sorted_move_names():
                        data = dpd[key][attack_i][defense_i][move_name]
                        if move_name == "なし":
                            max_hp_expected_damage_percent = -1.0
                            current_hp_expected_damage_percent = -1.0
                            status_move_feature_v = -1.0
                        if None in data:
                            max_hp_expected_damage_percent = 0.0
                            current_hp_expected_damage_percent = 0.0
                            status_move_feature_v = 1.0
                        else:
                            expected_damage = sum(damage * percent for damage, percent in dpd[key][attack_i][defense_i][move_name].items())
                            if defense_pokemon.max_hp < expected_damage:
                                max_hp_expected_damage_percent = 1.0
                            else:
                                max_hp_expected_damage_percent = expected_damage / float(defense_pokemon.max_hp)

                            if defense_pokemon.current_hp < expected_damage:
                                current_hp_expected_damage_percent = 1.0
                            elif defense_pokemon.current_hp <= 0:
                                current_hp_expected_damage_percent = 1.0
                            else:
                                current_hp_expected_damage_percent = expected_damage / float(defense_pokemon.current_hp)

                            status_move_feature_v = 0.0

                        result.append(max_hp_expected_damage_percent)
                        result.append(current_hp_expected_damage_percent)
                        result.append(status_move_feature_v)
            return result

        p1_dpd_feature_list = get(self.p1_fighters, self.p2_fighters, "p1_attack")
        p2_dpd_feature_list = get(self.p2_fighters, self.p1_fighters, "p2_attack")

        p1_feature_list = self.p1_fighters.to_feature_list()
        p2_feature_list = self.p2_fighters.to_feature_list()

        fighters_indices = [[0, 1, 2], [1, 0, 2], [2, 0, 1]]
        battles = [Battle([self.p1_fighters[index] for index in p1_indices],
                          [self.p2_fighters[index] for index in p2_indices]) \
                           for p1_indices in fighters_indices for p2_indices in fighters_indices]

        real_speed_winners = [Winner.new_real_speed(battle) for battle in battles]
        p1_real_speed_winner_feature_list = sum([real_speed_winner.to_binary_list() for real_speed_winner in real_speed_winners], [])
        p2_real_speed_winner_feature_list = sum([real_speed_winner.reverse().to_binary_list() for real_speed_winner in real_speed_winners], [])

        rsw_i = len(real_speed_winners) // Fighters.LENGTH
        dpb_i = len(p1_dpd_feature_list) // Fighters.LENGTH

        p1_feature_list[0] += (p1_dpd_feature_list[0:dpb_i] + p1_real_speed_winner_feature_list[0:rsw_i])
        p1_feature_list[1] += (p1_dpd_feature_list[dpb_i:dpb_i*2] + p1_real_speed_winner_feature_list[rsw_i:rsw_i*2])
        p1_feature_list[2] += (p1_dpd_feature_list[dpb_i*2:dpb_i*3] + p1_real_speed_winner_feature_list[rsw_i*2:rsw_i*3])

        p2_feature_list[0] += (p2_dpd_feature_list[0:dpb_i] + p2_real_speed_winner_feature_list[0:rsw_i])
        p2_feature_list[1] += (p2_dpd_feature_list[dpb_i:dpb_i*2] + p2_real_speed_winner_feature_list[rsw_i:rsw_i*2])
        p2_feature_list[2] += (p2_dpd_feature_list[dpb_i*2:dpb_i*3] + p2_real_speed_winner_feature_list[rsw_i*2:rsw_i*3])
        return p1_feature_list + p2_feature_list

    def to_feature_array_3d(self):
        feature_list = self.to_feature_list()
        padding_size = 18
        feature_list[0] += [0 for _ in range(padding_size)]
        feature_list[1] += [0 for _ in range(padding_size)]
        feature_list[2] += [0 for _ in range(padding_size)]
        feature_list[3] += [0 for _ in range(padding_size)]
        feature_list[4] += [0 for _ in range(padding_size)]
        feature_list[5] += [0 for _ in range(padding_size)]
        return np.array(feature_list).reshape(38, 38, Fighters.LENGTH * 2)

    def to_with_ui(self):
        return BattleWithUI(self)

    def new_checkmate_battle():
        def new_one_on_one():
            battle = Battle(Fighters.new_rate_random(), Fighters.new_rate_random())
            s, a, winner = battle.one_game(Trainer.random(), Trainer.random())


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

        if POISON in battle.p1_fighters[0].types:
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
        if battle.p1_fighters[0].status_ailment != BAD_POISON:
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

    def to_binary_list(self):
        if self == WINNER_P1:
            return [1, 0, 0]
        elif self == WINNER_P2:
            return [0, 1, 0]
        else:
            return [0, 0, 1]

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
    def new_action_priority(battle, p1_action_command, p2_action_command):
        def priority_rank(action_command):
            if action_command in ALL_MOVE_NAMES:
                return MOVEDEX[action_command].priority_rank
            elif action_command == STRUGGLE:
                return 0
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
    def new_final_priority(battle, p1_action_command, p2_action_command):
        priority_winner = Winner.new_action_priority(battle, p1_action_command, p2_action_command)
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
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def get_real_speed(battle):
    speed = battle.p1_fighters[0].speed
    rank_bonus = RANK_BONUS[battle.p1_fighters[0].speed_rank]
    speed_bonus = get_speed_bonus(battle)
    paralysis_bonus = PARALYSIS_BONUS[battle.p1_fighters[0].status_ailment == PARALYSIS]

    result = int(float(speed) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(speed_bonus) / 4096.0)
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

        if (POISON in battle.p2_fighters[0].types) or (STEEL in battle.p2_fighters[0].types):
            return battle

        battle = copy.deepcopy(battle)
        battle.p2_fighters[0].status_ailment = BAD_POISON
        return battle

    @staticmethod
    def leech_seed(battle):
        battle = copy.deepcopy(battle)
        if GRASS in battle.p2_fighters[0].types:
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
    def random(battle):
        return random.choice(battle.p1_fighters[0].legal_action_commands())

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
        assert MIN_RANK <= fluctuation_v <= MAX_RANK

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
            ui.real_p1_level = DEFAULT_LEVEL
            ui.real_p1_gender = real_p1_pokemon.gender
            ui.real_p1_max_hp = real_p1_pokemon.max_hp
            ui.real_p1_current_hp = real_p1_pokemon.current_hp

        if not self.hide_real_p2_ui:
            ui.real_p2_poke_name = real_p2_pokemon.name
            ui.real_p2_level = DEFAULT_LEVEL
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

        move_data = MOVEDEX[move_name]
        self = copy.deepcopy(self)
        self.battle.p1_fighters[0].moveset[move_name].current -= 1

        if self.battle.p2_fighters[0].is_faint():
            if move_data.target != "自分":
                for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                    ui_history.append(ui)

                for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(self, is_real_p1):
                    ui_history.append(ui)
                return self

        if move_name not in MAX_THREE_ATTACK_MOVE_NAMES:
            real_accuracy = self.battle.real_accuracy(move_name)
            if real_accuracy != -1:
                if not is_hit(real_accuracy):
                    for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                        ui_history.append(ui)

                    for ui in MISS_SHOT_BATTLE_MESSAGE.apply_bwu(self, is_real_p1):
                        ui_history.append(ui)
                    return self

        if move_data.category == STATUS:
            for ui in move_use_battle_message.apply_bwu(self, is_real_p1):
                ui_history.append(ui)

            if move_name in HALF_HEAL_MOVE_NAMES:
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
            final_damage_random_bonus = random.choice(FINAL_DAMAGE_RANDOM_BONUSES)
            is_critical = self.battle.is_critical(move_name)

            final_damage = get_final_damage(self.battle, move_name, final_damage_random_bonus, is_critical)

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

        effectiveness_bonus = get_effectiveness_bonus(self.battle.p2_fighters[0], move_name)

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
        if command in ALL_MOVE_NAMES + [STRUGGLE]:
            self = self.move_use(command, True, ui_history)
            return self
        elif command in ALL_POKE_NAMES:
            return self.switch(command, True, ui_history)
        assert False, "アクションコマンドが不正"

    def p2_action(self, command, ui_history):
        self.battle = self.battle.reverse()
        if command in ALL_MOVE_NAMES + [STRUGGLE]:
            self = self.move_use(command, False, ui_history)
            self.battle = self.battle.reverse()
            return self
        elif command in ALL_POKE_NAMES:
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
        s = []
        a = []
        ui_history = []
        while True:
            if self.battle.is_p1_and_p2_phase():
                p1_action_command = p1_trainer(self.battle)
                p2_action_command = p2_trainer(self.battle.reverse())
                action = {"p1":p1_action_command, "p2":p2_action_command}
            elif self.battle.is_p1_only_switch_after_faint_phase():
                action = {"p1":p1_trainer(self.battle)}
            else:
                action = {"p2":p2_trainer(self.battle.reverse())}

            s.append(self.battle)
            a.append(action)
            self = self.push(action, ui_history)

            if self.battle.is_game_end():
                break

        is_p1_all_faint = self.battle.p1_fighters.is_all_faint()
        is_p2_all_faint = self.battle.p2_fighters.is_all_faint()

        if is_p1_all_faint and is_p2_all_faint:
            return s, a, ui_history, DRAW
        elif is_p1_all_faint:
            return s, a, ui_history, WINNER_P2
        else:
            return s, a, ui_history, WINNER_P1

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

        if POISON in bwu.battle.p1_fighters[0].types:
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
        if bwu.battle.p1_fighters[0].status_ailment != BAD_POISON:
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

        if (POISON in bwu.battle.p2_fighters[0].types) or (STEEL in bwu.battle.p2_fighters[0].types):
            for ui in BattleMessage.new_no_effective(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, not is_real_p1):
                ui_history.append(ui)
            return bwu

        bwu = copy.deepcopy(bwu)
        bwu.battle.p2_fighters[0].status_ailment = BAD_POISON
        for ui in BattleMessage.new_bad_poisoned(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, is_real_p1):
            ui_history.append(ui)
        return bwu

    @staticmethod
    def leech_seed(bwu, is_real_p1, ui_history):
        if GRASS in bwu.battle.p2_fighters[0].types:
            for ui in BattleMessage.new_no_effective(bwu.battle.p2_fighters[0].name, not is_real_p1).apply_bwu(bwu, is_real_p1):
                ui_history.append(ui)
            return bwu

        if bwu.battle.p2_fighters[0].is_leech_seed:
            for ui in FAILURE_BATTLE_MESSAGE.apply_bwu(bwu, not is_real_p1):
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

IMPLEMENTED_MOVE_NAMES = [move_name for move_name in ALL_MOVE_NAMES \
                          if MOVEDEX[move_name].category != STATUS or move_name in HALF_HEAL_MOVE_NAMES or move_name in STATUS_MOVES]
