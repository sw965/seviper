import copy
import itertools
import numpy as np
import seviper.parts as parts
import seviper.battle as battle

POKE_NAME_FEATURES = ["なし"] + parts.RATE_POKE_NAMES
BASE_STATE_FEATURES = [state + 1 for state in range(parts.MAX_BASE_STATE)]
MOVE_NAME_FEATURES = ["なし"] + parts.ALL_MOVE_NAMES
MOVE_POWER_FEATURES = [power + 1 for power in range(parts.MAX_MOVE_POWER)]
MOVE_ACCURACY_FEATURES = [i + 1 for i in range(100)]
ITEM_FEATURES = ["なし"] + parts.ALL_ITEMS

class BinaryImageTeamPokemonFeatureTable:
    def __or__(self, bipft):
        self = copy.deepcopy(self)
        v = [[self.v[h][w] | bipft[h][w] for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]
        self.v = v
        return self

    def print(self, key):
        d = self.v[key]
        v = [[d[h][w] for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]
        for ele in v:
            print(ele)

def new_binary_image_team_pokemon_feature_table(index_1d_to_2d, features, is_inclusion_mode):
    feature_1d_index_to_2d = make_feature_1d_index_to_2d(index_1d_to_2d, features, is_inclusion_mode)
    v = {}
    for feature in features:
        index = features.index(feature)
        tmp = [[0 for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]
        for h, w in feature_1d_index_to_2d[index]:
            tmp[h][w] = 1
        v[feature] = tmp

    bipft = BinaryImageTeamPokemonFeatureTable()
    bipft.v = v
    return bipft

def new_binary_image_team_pokemon_half_heal_table():
    v = {}
    v[True] = [[1 for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]
    v[False] = [[0 for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]

    bipft = BinaryImageTeamPokemonFeatureTable()
    bipft.v = v
    return bipft

def new_binary_image_team_pokemon_one_hit_ko_table():
    v = {}
    v[True] = [[1 for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]
    v[False] = [[0 for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]

    bipft = BinaryImageTeamPokemonFeatureTable()
    bipft.v = v
    return bipft

def binary_image_team_pokemon_2d_size():
    height = 0
    width = 0

    while True:
        height += 1
        if parts.RATE_POKE_NAMES_LENGTH <= (height * width):
            break

        width += 1
        if parts.RATE_POKE_NAMES_LENGTH <= (height * width):
            break
    return (height, width)

BINARY_IMAGE_TEAM_POKEMON_SIZE_2D = binary_image_team_pokemon_2d_size()
BINARY_IMAGE_TEAM_POKEMON_HEIGHT = BINARY_IMAGE_TEAM_POKEMON_SIZE_2D[0]
BINARY_IMAGE_TEAM_POKEMON_WIDTH = BINARY_IMAGE_TEAM_POKEMON_SIZE_2D[1]
BINARY_IMAGE_TEAM_POKEMON_DEPTH = 57

def make_feature_1d_index_to_2d(index_1d_to_2d, features, is_inclusion_mode):
    features_length = len(features)
    count = (i for i in range(len(index_1d_to_2d)))

    result = [[index_1d_to_2d[next(count)] for j in range(len(index_1d_to_2d) // features_length)] \
               for i in range(features_length)]

    if is_inclusion_mode:
        return list(itertools.accumulate(result))
    else:
        return result

class BinaryImageTeamPokemon:
    INDEX_1D_TO_2D = [(h, w) for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT) for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)]

    POKE_NAME_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, POKE_NAME_FEATURES, False)
    TYPE_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_TYPES, False)
    LEARNSET_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_MOVE_NAMES, False)
    BASE_STATE_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, BASE_STATE_FEATURES, True)

    NATURE_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_NATURES, False)
    ABILITY_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_ABILITIES, False)
    GENDER_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_GENDERS, False)
    ITEM_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, ITEM_FEATURES, False)

    MOVE_NAME_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, MOVE_NAME_FEATURES, False)
    MOVE_POWER_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, MOVE_POWER_FEATURES, True)
    MOVE_ACCURACY_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, ACCURACY_FEATURES, True)
    HALF_HEAL_TABLE = new_binary_image_team_pokemon_half_heal_table()
    ONE_HIT_KO_TABLE = new_binary_image_team_pokemon_one_hit_ko_table()
    POINT_UP_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_POINT_UPS, True),
    INDIVIDUAL_VALUE_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_INDIVIDUAL_VALUES, True)
    EFFORT_VALUE_TABLE = new_binary_image_team_pokemon_feature_table(INDEX_1D_TO_2D, parts.ALL_EFFORT_VALUES, True)

    depth_counter = (i for i in range(BINARY_IMAGE_TEAM_POKEMON_DEPTH))

    POKE_NAME_DEPTH = next(depth_counter)
    POKE_TYPES_DEPTH = next(depth_counter)
    LEARNSET_DEPTH = next(depth_counter)
    BASE_HP_DEPTH = next(depth_counter)
    BASE_ATK_DEPTH = next(depth_counter)
    BASAE_DEF_DEPTH = next(depth_counter)
    BASE_SP_ATK_DEPTH = next(depth_counter)
    BASE_SP_DEF_DEPTH = next(depth_counter)
    BASE_SPEED_DEPTH = next(depth_counter)

    NATURE_DEPTH = next(depth_counter)
    ABILITY_DEPTH = next(depth_counter)
    GENDER_DEPTH = next(depth_counter)
    ITEM_DEPTH = next(depth_counter)

    MOVE1_NAME_DEPTH = next(depth_counter)
    MOVE1_TYPE_DEPTH = next(depth_counter)
    MOVE1_POWER_DEPTH = next(depth_counter)
    MOVE1_ACCURACY_DEPTH = next(depth_counter)
    MOVE1_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE1_ONE_HIT_KO_DEPTH = next(depth_counter)

    MOVE2_NAME_DEPTH = next(depth_counter)
    MOVE2_TYPE_DEPTH = next(depth_counter)
    MOVE2_POWER_DEPTH = next(depth_counter)
    MOVE2_ACCURACY_DEPTH = next(depth_counter)
    MOVE2_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE2_ONE_HIT_KO_DEPTH = next(depth_counter)

    MOVE3_NAME_DEPTH = next(depth_counter)
    MOVE3_TYPE_DEPTH = next(depth_counter)
    MOVE3_POWER_DEPTH = next(depth_counter)
    MOVE3_ACCURACY_DEPTH = next(depth_counter)
    MOVE3_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE3_ONE_HIT_KO_DEPTH = next(depth_counter)

    MOVE4_NAME_DEPTH = next(depth_counter)
    MOVE4_TYPE_DEPTH = next(depth_counter)
    MOVE4_POWER_DEPTH = next(depth_counter)
    MOVE4_ACCURACY_DEPTH = next(depth_counter)
    MOVE4_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE4_ONE_HIT_KO_DEPTH = next(depth_counter)

    POINT_UP1_DEPTH = next(depth_counter)
    POINT_UP2_DEPTH = next(depth_counter)
    POINT_UP3_DEPTH = next(depth_counter)
    POINT_UP4_DEPTH = next(depth_counter)

    INDIVIDUAL_HP_DEPTH = next(depth_counter)
    INDIVIDUAL_ATK_DEPTH = next(depth_counter)
    INDIVIDUAL_DEF_DEPTH = next(depth_counter)
    INDIVIDUAL_SP_ATK_DEPTH = next(depth_counter)
    INDIVIDUAL_SP_DEF_DEPTH = next(depth_counter)
    INDIVIDUAL_SPEED_DEPTH = next(depth_counter)

    EFFORT_HP_DEPTH = next(depth_counter)
    EFFORT_ATK_DEPTH = next(depth_counter)
    EFFORT_DEF_DEPTH = next(depth_counter)
    EFFORT_SP_ATK_DEPTH = next(depth_counter)
    EFFORT_SP_DEF_DEPTH = next(depth_counter)
    EFFORT_SPEED_DEPTH = next(depth_counter)

    TABLES = [
        POKE_NAME_TABLE,
        TYPE_TABLE,
        LEARNSET_TABLE,
        BASE_STATE_TABLE,
        BASE_STATE_TABLE,
        BASE_STATE_TABLE,
        BASE_STATE_TABLE,
        BASE_STATE_TABLE,
        BASE_STATE_TABLE,

        NATURE_TABLE,
        ABILITY_TABLE,
        GENDER_TABLE,
        ITEM_TABLE,

        MOVE_NAME_TABLE,
        TYPE_TABLE,
        MOVE_POWER_TABLE,
        MOVE_ACCURACY_TABLE,
        HALF_HEAL_TABLE,
        ONE_HIT_KO_TABLE,

        MOVE_NAME_TABLE,
        TYPE_TABLE,
        MOVE_POWER_TABLE,
        MOVE_ACCURACY_TABLE,
        HALF_HEAL_TABLE,
        ONE_HIT_KO_TABLE,

        MOVE_NAME_TABLE,
        TYPE_TABLE,
        MOVE_POWER_TABLE,
        MOVE_ACCURACY_TABLE,
        HALF_HEAL_TABLE,
        ONE_HIT_KO_TABLE,

        MOVE_NAME_TABLE,
        TYPE_TABLE,
        MOVE_POWER_TABLE,
        MOVE_ACCURACY_TABLE,
        HALF_HEAL_TABLE,
        ONE_HIT_KO_TABLE,

        POINT_UP_TABLE,
        POINT_UP_TABLE,
        POINT_UP_TABLE,
        POINT_UP_TABLE,

        INDIVIDUAL_VALUE_TABLE,
        INDIVIDUAL_VALUE_TABLE,
        INDIVIDUAL_VALUE_TABLE,
        INDIVIDUAL_VALUE_TABLE,
        INDIVIDUAL_VALUE_TABLE,
        INDIVIDUAL_VALUE_TABLE,

        EFFORT_VALUE_TABLE,
        EFFORT_VALUE_TABLE,
        EFFORT_VALUE_TABLE,
        EFFORT_VALUE_TABLE,
        EFFORT_VALUE_TABLE,
        EFFORT_VALUE_TABLE,
    ]

    assert len(TABLES) == (EFFORT_SPEED_DEPTH + 1)

    def __init__(self):
        data_2d = [[0 for w in range(BINARY_IMAGE_TEAM_POKEMON_WIDTH)] for h in range(BINARY_IMAGE_TEAM_POKEMON_HEIGHT)]
        self.data = [copy.deepcopy(data_2d) for _ in range(BinaryImageTeamPokemon.FEATURE_CATEGORY_NUM)]

        self.poke_name = None
        self.nature = None
        self.ability = None
        self.gender = None
        self.item = None
        self.move_names = [None, None, None, None]
        self.point_ups = [None, None, None, None]
        self.individual = parts.Individual(None, None, None, None, None, None)
        self.effort = parts.Effort(None, None, None, None, None, None)

    def print_2d(self, depth):
        height = BINARY_IMAGE_TEAM_POKEMON_HEIGHT
        width = BINARY_IMAGE_TEAM_POKEMON_WIDTH
        v = [[self.data[depth][h][w] for w in range(width)] for h in range(height)]
        for ele in v:
            print(ele)

    def set_features(self, features, depth):
        table = BinaryImageTeamPokemon.TABLES[depth]
        for feature in features:
            self.data[depth] = self.data[depth] | table[feature].v

    def set_poke_name(self, poke_name):
        assert self.poke_name is None, "ポケモン名は既に入力済み"
        self.set_features([poke_name], BinaryImageTeamPokemon.POKE_NAME_DEPTH)
        poke_data = POKEDEX[poke_name]
        self.set_features(poke_data.types, BinaryImageTeamPokemon.POKE_TYPE_DEPTH)
        self.set_features(poke_data.learnset, BinaryImageTeamPokemon.LEARNSET_DEPTH)
        self.set_features([poke_data.base_hp], BinaryImageTeamPokemon.BASE_HP_DEPTH)
        self.set_features([poke_data.base_atk], BinaryImageTeamPokemon.BASE_ATK_DEPTH)
        self.set_features([poke_data.base_def], BinaryImageTeamPokemon.BASE_DEF_DEPTH)
        self.set_features([poke_data.base_sp_atk], BinaryImageTeamPokemon.BASE_SP_ATK_DEPTH)
        self.set_features([poke_data.base_sp_def], BinaryImageTeamPokemon.BASE_SP_DEF_DEPTH)
        self.set_features([poke_data.base_speed], BinaryImageTeamPokemon.BASE_SPEED_DEPTH)
        self.poke_name = poke_name

    def set_nature(self, nature):
        assert self.nature is None, "性格は既に入力済み"
        self.set_features([nature], BinaryImageTeamPokemon.NATURE_DEPTH)
        self.nature = nature

    def set_ability(self, ability):
        assert self.poke_name is not None, "特性を入力する時は、ポケモン名を入力してからでなければならない"
        assert self.ability is None, "特性は既に入力済み"
        assert ability in POKEDEX[self.name].all_abilities, "特性: " + ability + "と ポケモン名: " + poke_name + "の組み合わせは不適"
        self.set_features([ability], BinaryImageTeamPokemon.ABILITY_DEPTH)
        self.ability = ability

    def set_gender(self, gender):
        assert self.poke_name is not None, "性別を入力する時は、ポケモン名を入力してからでなければならない"
        assert self.gender is None, "性別は既に入力済み"
        assert gender in valid_genders(poke_name, gender)
        self.set_features([gender], BinaryImageTeamPokemon.GENDER_DEPTH)
        self.gender = gender

    def set_item(self, item):
        assert self.item is None, "アイテムは既に入力済み"
        self.set_feature([item], BinaryImageTeamPokemon.ITEM_DEPTH)
        self.item = item

    def set_move_name(self, move_name, depth):
        assert self.poke_name is not None, "技名を入力する時は、ポケモン名を入力してからでなければならない"
        poke_data = POKEDEX[poke_name]

        depth_i = [MOVE1_NAME_DEPTH, MOVE2_NAME_DEPTH, MOVE3_NAME_DEPTH, MOVE4_NAME_DEPTH].index(depth)
        move_type_depth = [MOVE1_TYPE_DEPTH, MOVE2_TYPE_DEPTH, MOVE3_TYPE_DEPTH, MOVE4_TYPE_DEPTH][depth_i]
        move_power_depth = [MOVE1_POWER_DEPTH, MOVE2_POWER_DEPTH, MOVE3_POWER_DEPTH, MOVE4_POWER_DEPTH][depth_i]
        accuracy_depth = [MOVE1_ACCURACY_DEPTH, MOVE2_ACCURACY_DEPTH, MOVE3_ACCURACY_DEPTH, MOVE4_ACCURACY_DEPTH][depth_i]
        half_heal_depth = [MOVE1_HALF_HEAL, MOVE2_HALF_HEAL, MOVE3_HALF_HEAL, MOVE4_HALF_HEAL][depth_i]
        one_hit_ko_depth = [MOVE1_ONE_HIT_KO, MOVE2_ONE_HIT_KO, MOVE3_ONE_HIT_KO, MOVE4_ONE_HIT_KO][depth_i]

        self.set_features([move_name], depth)
        move_data = MOVEDEX[move_name]
        self.set_features([move_data.type], move_type_depth)

        if move_data.power > 0:
            if move_data.type in poke_data.types:
                power = int(power * 1.5)
            else:
                power = move_data.power
            self.set_features([power], move_power_depth)

        accuracy = move_data.accuracy
        if accuracy == -1:
            accuracy = 100

        if accuracy != 0:
            self.set_features([accuracy], accuracy_depth)

        self.set_features([move_name in parts.HALF_HEAL_MOVE_NAMES], half_heal_depth)
        self.set_features([move_name in parts.ONE_HIT_KO_MOVE_NAMES], one_hit_ko_depth)

    def set_move1_name(self, move_name):
        assert move_name in POKEDEX[self.poke_name].learnset
        assert self.move_names[0] is None
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE1_NAME_DEPTH)
        assert self.move_names.count(None) == 4
        self.move_names[0] = move_name

    def set_move2_name(self, move_name):
        assert move_name in ["なし"] + POKEDEX[self.poke_name].learnset
        assert self.move_names[1] is None
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE2_NAME_DEPTH)
        assert self.move_names.count(None) == 3
        self.move_names[1] = move_name

    def set_move3_name(self, move_name):
        assert move_name in ["なし"] + POKEDEX[self.poke_name].learnset
        assert self.move_names[2] is None
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE3_NAME_DEPTH)
        assert self.move_names.count(None) == 2
        self.move_names[2] = move_name

    def set_move4_name(self, move_name):
        assert move_name in ["なし"] + POKEDEX[self.poke_name].learnset
        assert self.move_names[3] is None
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE4_NAME_DEPTH)
        assert self.move_names.count(None) == 1
        self.move_names[3] = move_name

    def set_point_up(self, point_up, depth):
        assert parts.is_valid_point_up(point_up)
        self.set_features([point_up], depth)

    def set_point_up1(self, point_up):
        assert self.move_names[0] is not None
        assert self.point_ups[0] is None
        self.set_point_up(point_up, BinaryImageTeamPokemon.POINT_UP1_DEPTH)
        self.point_ups[0] = point_up

    def set_point_up2(self, point_up):
        assert self.move_names[1] is not None
        assert self.point_ups[1] is None
        self.set_point_up(point_up, BinaryImageTeamPokemon.POINT_UP2_DEPTH)
        self.point_ups[1] = point_up

    def set_point_up3(self, point_up):
        assert self.move_names[2] is not None
        assert self.point_ups[2] is None
        self.set_point_up(point_up, BinaryImageTeamPokemon.POINT_UP3_DEPTH)
        self.point_ups[2] = point_up

    def set_point_up4(self, point_up):
        assert self.move_names[3] is not None
        assert self.point_ups[3] is None
        self.set_point_up(point_up, BinaryImageTeamPokemon.POINT_UP4_DEPTH)
        self.point_ups[3] = point_up

    def set_individual_v(self, individual_v, depth, state_type):
        assert individual_v in ALL_INDIVIDUAL_VALUES
        self.set_features([individual_v], depth)

    def set_individual_hp(self, individual_v):
        assert self.individual.hp is None
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_HP_DEPTH)
        self.individual.hp = individual_v

    def set_individual_atk(self, individual_v):
        assert self.individual.atk is None
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_ATK_DEPTH)
        self.individual.atk = individual_v

    def set_individual_def(self, individual_v):
        assert self.individual.defe is None
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_DEF_DEPTH)
        self.individual.defe = individual_v

    def set_individual_sp_atk(self, individual_v):
        assert self.individual.sp_atk is None
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_SP_ATK_DEPTH)
        self.individual.sp_atk = individual_v

    def set_individual_sp_def(self, individual_v):
        assert self.individual.sp_def is None
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_SP_DEF_DEPTH)
        self.individual.sp_def = individual_v

    def set_individual_speed(self, individual_v):
        assert self.individual.speed is None
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_SPEED_DEPTH)
        self.individual.speed = individual_v

    def set_effort_v(self, effort_v, depth):
        assert effort_v in parts.ALL_EFFORT_VALUES

        if self.effort.hp is None:
            hp = 0
        if self.effort.atk is None:
            atk = 0
        if self.effort.defe is None:
            defe = 0
        if self.effort.sp_atk is None:
            sp_atk = 0
        if self.effort.sp_def is None:
            sp_def = 0
        if self.effort.speed is None:
            speed = 0

        sum_v = hp + atk + defe + sp_atk + sp_def + speed
        assert (effort_v + sum_v) <= Effort.MAX_SUM, "努力値の合計値が" + Effort.MAX_SUM + "を超えた"
        self.set_features([effort_v], depth)

    def set_effort_hp(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_HP_DEPTH)
        self.effort.hp = effort_v

    def set_effort_atk(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_ATK_DEPTH)
        self.effort.atk = effort_v

    def set_effort_def(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_DEF_DEPTH)
        self.effort.defe = effort_v

    def set_effort_sp_atk(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_SP_ATK_DEPTH)
        self.effort.sp_atk = effort_v

    def set_effort_sp_def(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_SP_DEF_DEPTH)
        self.effort.sp_def = effort

    def set_effort_speed(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_SPEED_DEPTH)
        self.effort.speed = effort_v


class BinaryImageTeam:
    def __init__(self):
        self.images = [BinaryImageTeamPokemon() for _ in range(battle.MAX_TEAM_NUM)]

    def get(self):
        return sum([image.data for image in self.images], [])

    def set_poke_name(self, poke_name, index):
        if index in [0, 1, 2]:
            assert poke_name != "なし"

        poke_names = [image.poke_name for image in self.images]
        assert poke_name not in poke_names, poke_name + " は既にチームに存在する(同じ名前のポケモンを入れようとした)"

        images[index].set_poke_name(poke_name)

    def set_item(self, item, index):
        items = [image.item for image in self.images]
        if item != "なし":
            assert item not in items, item + " は別のポケモンが既に持っている"
        self.images[index].set_item(item)


BINARY_IMAGE_BATTLE_POKEMON_DEPTH = 1

class BinaryImageBattlePokemon:
    depth_counter = (i for i in range(BINARY_IMAGE_BATTLE_POKEMON_DEPTH))
    POKE_NAME_DEPTH = next(depth_counter)
    NATURE_DEPTH = next(depth_counter)
    ABILITY_DEPTH = next(depth_counter)
    GENDER_DEPTH = next(depth_counter)


    def __init__(self, pokemon):


    def set(battle_pokemon):


class BinaryImageFighters:
    def __init__(self):
        self.data = []

class BinaryImageBattle:
    def __init__(self):
        ...
