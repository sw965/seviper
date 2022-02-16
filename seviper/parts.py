import os
import boa
import seviper.path as path

ALL_POKE_NAMES = boa.readlines_txt(path.ALL_POKE_NAMES, True)
assert len(set(ALL_POKE_NAMES)) == len(ALL_POKE_NAMES)

STRUGGLE = "わるあがき"

ALL_MOVE_NAMES = [file_name[:-4] for folder_name in os.listdir(path.POKETETU_MOVEDEX) \
                  for file_name in os.listdir(path.POKETETU_MOVEDEX + folder_name)]
assert len(set(ALL_MOVE_NAMES)) == len(ALL_MOVE_NAMES)

HALF_HEAL_MOVE_NAMES = boa.readlines_txt(path.HALF_HEAL_MOVE_NAMES, True)
assert len(set(HALF_HEAL_MOVE_NAMES)) == len(HALF_HEAL_MOVE_NAMES)
assert set(HALF_HEAL_MOVE_NAMES).issubset(ALL_MOVE_NAMES)

ONE_HIT_KO_MOVE_NAMES = boa.readlines_txt(path.ONE_HIT_KO_MOVE_NAMES, True)
assert len(set(ONE_HIT_KO_MOVE_NAMES)) == len(ONE_HIT_KO_MOVE_NAMES)
assert set(ONE_HIT_KO_MOVE_NAMES).issubset(ALL_MOVE_NAMES)

def valid_genders(gender_data):
    if gender_data == "♂♀両方":
        return [MALE, FEMALE]
    elif gender_data == "♂のみ":
        return [MALE]
    elif gender_data == "♀のみ":
        return [FEMALE]
    else:
        return [UNKNOWN]

MALE = "♂"
FEMALE = "♀"
UNKNOWN = "不明"

ALL_GENDERS = [MALE, FEMALE, UNKNOWN]


class PokeData:
    def __init__(self, json_data):
        self.normal_abilities = json_data["NormalAbilities"]
        self.hidden_ability = json_data["HiddenAbility"]
        self.all_abilities = json_data["AllAbilities"]
        self.gender = json_data["Gender"]
        self.types = json_data["Types"]

        self.base_hp = json_data["BaseHP"]
        self.base_atk = json_data["BaseAtk"]
        self.base_def = json_data["BaseDef"]
        self.base_sp_atk = json_data["BaseSpAtk"]
        self.base_sp_def = json_data["BaseSpDef"]
        self.base_speed = json_data["BaseSpeed"]

        self.height = json_data["Height"]
        self.weight = json_data["Weight"]
        self.egg_groups = json_data["EggGroups"]
        self.category = json_data["Category"]
        self.learnset = json_data["Learnset"]

def is_rate_battle_ok(poke_data):
    return poke_data.category != "伝説のポケモン" and poke_data.category != "幻のポケモン"


POKEDEX = {poke_name:PokeData(boa.load_json(path.POKEDEX + poke_name + ".json")) for poke_name in ALL_POKE_NAMES}

RATE_POKE_NAMES = [poke_name for poke_name in ALL_POKE_NAMES if is_rate_battle_ok(POKEDEX[poke_name])]
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
    def __init__(self, json_data):
        self.type = json_data["Type"]
        self.category = json_data["Category"]
        self.power = json_data["Power"]
        self.accuracy = json_data["Accuracy"]
        self.base_pp = json_data["BasePP"]
        self.target = json_data["Target"]

        self.contact = json_data["Contact"]
        self.protect = json_data["Protect"]
        self.magic_coat = json_data["MagicCoat"]
        self.snatch = json_data["Snatch"]
        self.mirror_move = json_data["MirrorMove"]
        self.substitute = json_data["Substitute"]

        self.gigantamax_move = json_data["GigantamaxMove"]
        self.gigantamax_power = json_data["GigantamaxPower"]
        self.priority_rank = json_data["PriorityRank"]
        self.critical_rank = json_data["CriticalRank"]

        self.min_attack_num = json_data["MinAttackNum"]
        self.max_attack_num = json_data["MaxAttackNum"]


MOVEDEX = {move_name:MoveData(boa.load_json(path.MOVEDEX + move_name + ".json")) for move_name in ALL_MOVE_NAMES}

PHYSICS = "物理"
SPECIAL = "特殊"
STATUS = "変化"

MAX_MOVE_POWER = max([MOVEDEX[move_name].power for move_name in ALL_MOVE_NAMES])
MIN_ATTACK_NUM = min([MOVEDEX[move_name].min_attack_num for move_name in ALL_MOVE_NAMES])
MAX_ATTACK_NUM = max([MOVEDEX[move_name].max_attack_num for move_name in ALL_MOVE_NAMES])

class NatureData:
    def __init__(self, json_data):
        self.id = json_data["ID"]
        self.atk_bonus = json_data["AtkBonus"]
        self.def_bonus = json_data["DefBonus"]
        self.sp_atk_bonus = json_data["SpAtkBonus"]
        self.sp_def_bonus = json_data["SpDefBonus"]
        self.speed_bonus = json_data["SpeedBonus"]

NATUREDEX = {key:NatureData(value) for key, value in boa.load_json(path.NATUREDEX).items()}

def id_to_nature(id_):
    results = [key for key, value in NATUREDEX.items() if value.id == id_]
    assert len(results) == 1
    return results[0]

ALL_NATURES = [id_to_nature(i) for i in range(len(NATUREDEX))]
ALL_NATURES_LENGTH = len(ALL_NATURES)

TYPEDEX = boa.load_json(path.TYPEDEX)

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

ALL_TYPES = [
    NORMAL,
    FIRE,
    WATER,
    GRASS,
    ELECTRIC,
    ICE,
    FIGHTING,
    POISON,
    GROUND,
    FLYING,
    PSYCHIC,
    BUG,
    ROCK,
    GHOST,
    DRAGON,
    DARK,
    STEEL,
    FAIRY
]

assert len(ALL_TYPES) == 18
assert len(set(ALL_TYPES)) == len(ALL_TYPES)
assert set(TYPEDEX.keys()) == set(ALL_TYPES)

DEFAULT_LEVEL = 50

ALL_ITEMS = boa.readlines_txt(path.ALL_ITEMS, True)

ALL_INDIVIDUAL_VALUES = [i for i in range(32)]
MIN_INDIVIDUAL_VALUE = min(ALL_INDIVIDUAL_VALUES)
MAX_INDIVIDUAL_VALUE = max(ALL_INDIVIDUAL_VALUES)

def is_valid_individual_value(individual_value):
    return MIN_INDIVIDUAL_VALUE <= individual_value <= MAX_INDIVIDUAL_VALUE

class Individual:
    def __init__(self, hp, atk, defe, sp_atk, sp_def, speed):
        self.hp = hp
        self.atk = atk
        self.defe = defe
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed

    def __eq__(self, individual):
        d = [self.hp == effort.hp,
             self.atk == effort.atk,
             self.defe == effort.defe,
             self.sp_atk == effort.sp_atk,
             self.sp_def == effort.sp_def,
             self.speed == effort.speed]
        return all(d)


ALL_EFFORT_VALUES = [i for i in range(253)]
MIN_EFFORT_VALUE = min(ALL_EFFORT_VALUES)
MAX_EFFORT_VALUE = max(ALL_EFFORT_VALUES)
EFFECTIVE_EFFORT_VALUES = [ev for ev in ALL_EFFORT_VALUES if ev%4 == 0]

def is_valid_effort_value(effort_value):
    return MIN_EFFORT_VALUE <= effort_value <= MAX_EFFORT_VALUE


class Effort:
    MAX_SUM = 510

    def __init__(self, hp, atk, defe, sp_atk, sp_def, speed):
        self.hp = hp
        self.atk = atk
        self.defe = defe
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed

    def __eq__(self, effort):
        d = [self.hp == effort.hp,
             self.atk == effort.atk,
             self.defe == effort.defe,
             self.sp_atk == effort.sp_atk,
             self.sp_def == effort.sp_def,
             self.speed == effort.speed]
        return all(d)

    def sum(self):
        return self.hp + self.atk + self.defe + self.sp_atk + self.sp_def + self.speed

    def is_valid_sum(self):
        return 0 <= self.sum() <= Effort.MAX_SUM


ALL_POINT_UPS = [0, 1, 2, 3]
MIN_POINT_UP = min(ALL_POINT_UPS)
MAX_POINT_UP = max(ALL_POINT_UPS)

def is_valid_point_up(point_up):
    return MIN_POINT_UP <= point_up <= MAX_POINT_UP


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

MIN_MOVESET_NUM = 1
MAX_MOVESET_NUM = 4

def hp_state_calc(base_hp, individual_value, effort_value):
    return ((base_hp * 2) + individual_value + (effort_value // 4) ) * DEFAULT_LEVEL // 100 + DEFAULT_LEVEL + 10

def state_calc(base_state, individual_value, effort_value, nature_bonus):
    result = ( (base_state * 2) + individual_value + (effort_value // 4) ) * DEFAULT_LEVEL // 100 + 5
    return int(float(result) * nature_bonus)

MAX_HP = hp_state_calc(MAX_BASE_HP, 31, 252)
MAX_STATE = state_calc(MAX_BASE_STATE, 31, 31, 1.1)

NORMAL_POISON = "どく"
BAD_POISON = "もうどく"
SLEEP = "ねむり"
BURN = "やけど"
PARALYSIS = "まひ"
FREEZE = "こおり"

ALL_STATUS_AILMENT = [
    NORMAL_POISON, BAD_POISON, SLEEP, BURN, PARALYSIS, FREEZE
]

#https://wiki.xn--rckteqa2e.com/wiki/%E9%80%A3%E7%B6%9A%E6%94%BB%E6%92%83%E6%8A%80
TWO_ATTACK_PERCENT = [100, 100]
THREE_ATTACK_PERCENT = [100, 100, 100]
MIN_TWO_MAX_FIVE_ATTACK_PERCENT = [100, 100, 35, 35, 15, 15]

ATTACK_NUM_PERCENT = {
    "すいりゅうれんだ":THREE_ATTACK_PERCENT,
    "ダブルウイング":TWO_ATTACK_PERCENT,
    "ホネブーメラン":TWO_ATTACK_PERCENT,
    "ギアソーサー":TWO_ATTACK_PERCENT,
    "みだれづき":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "トリプルアクセル":None,
    "ドラゴンアロー":TWO_ATTACK_PERCENT,
    "つっぱり":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "ボーンラッシュ":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "みずしゅりけん":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "にどげり":TWO_ATTACK_PERCENT,
    "ダブルチョップ":TWO_ATTACK_PERCENT,
    "スイープビンタ":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "ミサイルばり":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "ダブルアタック":TWO_ATTACK_PERCENT,
    "トリプルキック":None,
    "タネマシンガン":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "ダブルパンツァー":TWO_ATTACK_PERCENT,
    "つららばり":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "みだれひっかき":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "ロックブラスト":MIN_TWO_MAX_FIVE_ATTACK_PERCENT,
    "スケイルショット":MIN_TWO_MAX_FIVE_ATTACK_PERCENT
}
