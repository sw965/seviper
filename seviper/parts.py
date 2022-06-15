import copy
import random
import itertools
import numpy as np
import seviper.base_data as base_data

EMPTY = "なし"

PHYSICS = "物理"
SPECIAL = "特殊"
STATUS = "変化"

def get_sorted_move_names(self):
    indices = sorted([base_data.ALL_MOVE_NAMES.index(move_name) for move_name in self])
    return [base_data.ALL_MOVE_NAMES[index] for index in indices]

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

MIN_MOVESET_LENGTH = 1
MAX_MOVESET_LENGTH = 4

NORMAL_POISON = "どく"
BAD_POISON = "もうどく"
SLEEP = "ねむり"
BURN = "やけど"
PARALYSIS = "まひ"
FREEZE = "こおり"

ALL_STATUS_AILMENT = [
    NORMAL_POISON, BAD_POISON, SLEEP, BURN, PARALYSIS, FREEZE
]

MIN_RANK = -6
MAX_RANK = 6

def calc_hp_state(base_hp, individual_value, effort_value):
    return ((base_hp * 2) + individual_value + (effort_value // 4) ) * DEFAULT_LEVEL // 100 + DEFAULT_LEVEL + 10

def calc_state(base_state, individual_value, effort_value, nature_bonus):
    result = ( (base_state * 2) + individual_value + (effort_value // 4) ) * DEFAULT_LEVEL // 100 + 5
    return int(float(result) * nature_bonus)

MAX_FEATURE_NUM = len(base_data.RATE_POKE_NAMES)

def get_feature_height_and_width():
    h = 1
    w = 1
    while True:
        size = h * w
        if size > MAX_FEATURE_NUM:
            break

        h += 1
        if size > MAX_FEATURE_NUM:
            break

        w += 1
        if size > MAX_FEATURE_NUM:
            break
    return h, w

FEATURE_HEIGHT, FEATURE_WIDTH = get_feature_height_and_width()
ALL_2D_FEATURE_INDICES = [(h, w) for h in range(FEATURE_HEIGHT) for w in range(FEATURE_WIDTH)]

def make_2d_zeros_feature():
    return [[0 for w in range(FEATURE_WIDTH)] for h in range(FEATURE_HEIGHT)]

def make_2d_ones_feature():
    return [[1 for w in range(FEATURE_WIDTH)] for h in range(FEATURE_HEIGHT)]

class Pokemon:
    @staticmethod
    def new(poke_name, nature, ability, gender, item, move_names, point_ups, individual, effort):
        assert poke_name in base_data.ALL_POKE_NAMES, "ポケモン名が不適"
        assert nature in base_data.ALL_NATURES, "性格が不適"
        poke_data = base_data.POKEDEX[poke_name]

        assert ability in poke_data.all_abilities, "特性が不適"
        assert gender in gender_data_to_valid_genders(poke_data.gender), "性別が不適"
        assert item in base_data.ALL_ITEMS + [EMPTY], "アイテムが不適"

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

        nature_data = base_data.NATUREDEX[nature]
        pokemon = Pokemon()

        pokemon.name = poke_name
        pokemon.nature = nature
        pokemon.ability = ability
        pokemon.gender = gender
        pokemon.item = item

        pokemon.sorted_move_names = get_sorted_move_names(move_names)
        pokemon.moveset = {move_name:PowerPoint(base_data.MOVEDEX[move_name].base_pp, point_ups[i]) \
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

    @staticmethod
    def new_random(poke_name):
        poke_data = base_data.POKEDEX[poke_name]
        nature = random.choice(base_data.ALL_NATURES)
        ability = random.choice(poke_data.all_abilities)
        gender = random.choice(gender_data_to_valid_genders(poke_data.gender))

        learnset_indices = [i for i in range(len(poke_data.learnset)) if poke_data.learnset[i] in base_data.ALL_MOVE_NAMES]
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

        return Pokemon.new(poke_name, nature, ability, gender, EMPTY, move_names, point_ups, individual, effort)

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

    def is_full_hp(self):
        return self.max_hp == self.current_hp

    def is_faint(self):
        return self.current_hp <= 0

    def is_faint_damage(self, damage):
        return damage >= self.current_hp

    def current_damage(self):
        return self.max_hp - self.current_hp

    def padding_sorted_move_names(self):
        return self.sorted_move_names + [EMPTY for _ in range(MAX_MOVESET_LENGTH - len(self.sorted_move_names))]

    def poke_name_2d_feature_list(self):
        result = make_2d_zeros_feature()
        h, w = ALL_2D_FEATURE_INDICES[base_data.RATE_POKE_NAMES.index(self.name)]
        result[h][w] = 1
        return result

    def nature_2d_feature_list(self):
        result = make_2d_zeros_feature()
        h, w = ALL_2D_FEATURE_INDICES[base_data.ALL_NATURES.index(self.nature)]
        result[h][w] = 1
        return result

    def ability_2d_feature_list(self):
        result = make_2d_zeros_feature()
        h, w = ALL_2D_FEATURE_INDICES[base_data.ALL_ABILITIES.index(self.ability)]
        result[h][w] = 1
        return result

    def gender_2d_feature_list(self):
        result = make_2d_zeros_feature()
        h, w = ALL_2D_FEATURE_INDICES[ALL_GENDERS.index(self.gender)]
        result[h][w] = 1
        return result

    def item_2d_feature_list(self):
        result = make_2d_zeros_feature()
        h, w = ALL_2D_FEATURE_INDICES[base_data.ALL_ITEMS.index(self.item)]
        result[h][w] = 1
        return result

    def move_name_2d_feature_list(self):
        result = make_2d_zeros_feature()
        for move_name in self.sorted_move_names:
            h, w = ALL_2D_FEATURE_INDICES[base_data.ALL_MOVE_NAMES.index(move_name)]
            assert result[h][w] == 0
            result[h][w] = 1
        return result

    def max_power_point_2d_feature_list(self):
        result = make_2d_zeros_feature()
        for i, move_name in enumerate(self.sorted_move_names):
            power_point = self.moveset[move_name]
            h, w = ALL_2D_FEATURE_INDICES[base_data.ALL_MOVE_NAMES.index(move_name)]
            result[h][w] = float(power_point.max) / 10.0
        return result

    def current_power_point_2d_feature_list(self):
        result = make_2d_zeros_feature()
        for i, move_name in enumerate(self.sorted_move_names):
            power_point = self.moveset[move_name]
            h, w = ALL_2D_FEATURE_INDICES[base_data.ALL_MOVE_NAMES.index(move_name)]
            result[h][w] = float(power_point.current) / float(power_point.max)
        return result

    def state_2d_feature_list(self):
        result = make_2d_zeros_feature()

        h, w = ALL_2D_FEATURE_INDICES[0]
        result[h][w] = float(self.max_hp) / 100.0

        h, w = ALL_2D_FEATURE_INDICES[1]
        result[h][w] = float(self.current_hp) / float(self.max_hp)

        h, w = ALL_2D_FEATURE_INDICES[2]
        result[h][w] = float(self.atk) / 100.0

        h, w = ALL_2D_FEATURE_INDICES[3]
        result[h][w] = float(self.defe) / 100.0

        h, w = ALL_2D_FEATURE_INDICES[4]
        result[h][w] = float(self.sp_atk) / 100.0

        h, w = ALL_2D_FEATURE_INDICES[5]
        result[h][w] = float(self.sp_def) / 100.0

        h, w = ALL_2D_FEATURE_INDICES[6]
        result[h][w] = float(self.speed) /100.0
        return result

    def rank_2d_feature_list(self):
        result = make_2d_zeros_feature()

        h, w = ALL_2D_FEATURE_INDICES[0]
        result[h][w] = float(self.atk_rank)

        h, w = ALL_2D_FEATURE_INDICES[1]
        result[h][w] = float(self.def_rank)

        h, w = ALL_2D_FEATURE_INDICES[2]
        result[h][w] = float(self.sp_atk_rank)

        h, w = ALL_2D_FEATURE_INDICES[3]
        result[h][w] = float(self.sp_def_rank)

        h, w = ALL_2D_FEATURE_INDICES[4]
        result[h][w] = float(self.speed_rank)

        h, w = ALL_2D_FEATURE_INDICES[5]
        result[h][w] = float(self.accuracy_rank)

        h, w = ALL_2D_FEATURE_INDICES[6]
        result[h][w] = float(self.evasion_rank)
        return result

    def status_ailment_2d_feature_list(self):
        result = make_2d_zeros_feature()
        if self.status_ailment != "":
            h, w = ALL_2D_FEATURE_INDICES[ALL_STATUS_AILMENT.index(self.status_ailment)]
            result[h][w] = 1
        return result

    def bad_poison_elapsed_turn_2d_feature_list(self):
        result = make_2d_zeros_feature()
        h, w = ALL_2D_FEATURE_INDICES[self.bad_poison_elapsed_turn]
        result[h][w] = 1
        return result

    def choice_move_name_2d_feature_list(self):
        result = make_2d_zeros_feature()
        if self.choice_move_name != "":
            h, w = ALL_2D_FEATURE_INDICES[ALL_MOVE_NAMES.index(self.choice_move_name)]
            result[h][w] = 1
        return result

    def roots_2d_feature_list(self):
        if self.is_roots:
            return make_2d_ones_feature()
        else:
            return make_2d_zeros_feature()

    def leech_seed_2d_feature_list(self):
        if self.is_leech_seed:
            return make_2d_ones_feature()
        else:
            return make_2d_zeros_feature()

    def two_d_feature_list(self):
        result = [
            self.poke_name_2d_feature_list(),
            self.nature_2d_feature_list(),
            self.ability_2d_feature_list(),
            self.gender_2d_feature_list(),
            self.item_2d_feature_list(),
            self.move_name_2d_feature_list(),
            self.max_power_point_2d_feature_list(),
            self.current_power_point_2d_feature_list(),
            self.state_2d_feature_list(),
            self.rank_2d_feature_list(),
            self.status_ailment_2d_feature_list(),
            self.bad_poison_elapsed_turn_2d_feature_list(),
            self.choice_move_name_2d_feature_list(),
            self.roots_2d_feature_list(),
            self.leech_seed_2d_feature_list()
        ]
        return result

def new_venusaur():
    result = Pokemon.new("フシギバナ", "おだやか", "しんりょく", "♀", "くろいヘドロ",
                     ["ギガドレイン", "ヘドロばくだん", "やどりぎのタネ", "どくどく"], [3, 3, 3, 3],
                     ALL_MAX_INDIVIDUAL,
                     Effort({"hp":252, "atk":0, "defe":0, "sp_atk":0, "sp_def":252, "speed":4}))
    return result

def new_charizard():
    result = Pokemon.new("リザードン", "おくびょう", "もうか", "♂", "いのちのたま",
                     ["かえんほうしゃ", "エアスラッシュ", "オーバーヒート", "りゅうのはどう"], [3, 3, 3, 3],
                      ALL_MAX_INDIVIDUAL,
                      Effort({"hp":4, "atk":0, "defe":0, "sp_atk":252, "sp_def":0, "speed":252}))
    return result

def new_blastoise():
    result = Pokemon.new("カメックス", "ひかえめ", "げきりゅう", "♂", "オボンのみ",
                     ["なみのり", "れいとうビーム", "あくのはどう", "からをやぶる"], [3, 3, 3, 3],
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

        items_indices = [i for i in range(len(base_data.ALL_ITEMS))]
        random.shuffle(items_indices)
        items = [base_data.ALL_ITEMS[index] for index in items_indices[:Fighters.LENGTH]]

        fighters = Fighters([Pokemon.new_random(poke_name) for poke_name in poke_names])
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
