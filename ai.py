import copy
import itertools
import numpy as np
import parts

ALL_BASE_STATES = [state + 1 for state in range(parts.MAX_BASE_STATE)]
ALL_MOVE_NAMES = ["なし"] + parts.ALL_MOVE_NAMES
ALL_MOVE_POWERS = [power + 1 for power in range(parts.MAX_MOVE_POWER)]
ALL_ACCURACY = [i + 1 for i in range(100)]

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

def make_feature_1d_index_to_2d(indices_1d_to_2d, features, is_inclusion_mode):
    features_length = len(features)
    count = (i for i in range(len(indices_1d_to_2d)))

    result = [[indices_1d_to_2d[next(count)] for j in range(len(indices_1d_to_2d) // features_length)] \
               for i in range(features_length)]

    if is_inclusion_mode:
        return list(itertools.accumulate(result))
    else:
        return result

class BinaryImageTeamPokemon:
    SIZE_2D = binary_image_team_pokemon_2d_size()
    HEIGHT = SIZE_2D[0]
    WIDTH = SIZE_2D[1]

    INDEX_1D_TO_2D = (lambda height, width:[(h, w) for h in range(height) for w in range(width)])(HEIGHT, WIDTH)

    POKE_NAME_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.RATE_POKE_NAMES, False)
    TYPE_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.RATE_POKE_NAMES, False)
    LEARNSET_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_MOVE_NAMES, False),
    BASE_STATE_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, ALL_BASE_STATES, True),

    NATURE_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_NATURES, False),
    ABILITY_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_ABILITIES, False),
    GENDER_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_GENDERS, False),
    ITEM_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_ITEMS, False)

    MOVE_NAME_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, ALL_MOVE_NAMES, False)
    MOVE_POWER_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, ALL_MOVE_POWERS, True)
    MOVE_ACCURACY_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, ALL_ACCURACY, True)
    POINT_UP_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_POINT_UPS, True),
    INDIVIDUAL_VALUE_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_INDIVIDUAL_VALUES, True)
    EFFORT_VALUE_1D_INDEX_TO_2D = make_feature_1d_index_to_2d(INDEX_1D_TO_2D, parts.ALL_EFFORT_VALUES, True)

    FEATURE_INDEX_1D_TO_2D_LIST = [
        POKE_NAME_1D_INDEX_TO_2D,
        TYPE_1D_INDEX_TO_2D,
        LEARNSET_1D_INDEX_TO_2D,
        BASE_STATE_1D_INDEX_TO_2D,
        BASE_STATE_1D_INDEX_TO_2D,
        BASE_STATE_1D_INDEX_TO_2D,
        BASE_STATE_1D_INDEX_TO_2D,
        BASE_STATE_1D_INDEX_TO_2D,
        BASE_STATE_1D_INDEX_TO_2D,

        NATURE_1D_INDEX_TO_2D,
        ABILITY_1D_INDEX_TO_2D,
        GENDER_1D_INDEX_TO_2D,
        ITEM_1D_INDEX_TO_2D,

        MOVE_NAME_1D_INDEX_TO_2D,
        TYPE_1D_INDEX_TO_2D,
        MOVE_POWER_1D_INDEX_TO_2D,
        MOVE_ACCURACY_1D_INDEX_TO_2D,
        None,
        None,

        MOVE_NAME_1D_INDEX_TO_2D,
        TYPE_1D_INDEX_TO_2D,
        MOVE_POWER_1D_INDEX_TO_2D,
        MOVE_ACCURACY_1D_INDEX_TO_2D,
        None,
        None,

        MOVE_NAME_1D_INDEX_TO_2D,
        TYPE_1D_INDEX_TO_2D,
        MOVE_POWER_1D_INDEX_TO_2D,
        MOVE_ACCURACY_1D_INDEX_TO_2D,
        None,
        None,

        MOVE_NAME_1D_INDEX_TO_2D,
        TYPE_1D_INDEX_TO_2D,
        MOVE_POWER_1D_INDEX_TO_2D,
        MOVE_ACCURACY_1D_INDEX_TO_2D,
        None,
        None,

        POINT_UP_1D_INDEX_TO_2D,
        POINT_UP_1D_INDEX_TO_2D,
        POINT_UP_1D_INDEX_TO_2D,
        POINT_UP_1D_INDEX_TO_2D,

        INDIVIDUAL_VALUE_1D_INDEX_TO_2D,
        INDIVIDUAL_VALUE_1D_INDEX_TO_2D,
        INDIVIDUAL_VALUE_1D_INDEX_TO_2D,
        INDIVIDUAL_VALUE_1D_INDEX_TO_2D,
        INDIVIDUAL_VALUE_1D_INDEX_TO_2D,
        INDIVIDUAL_VALUE_1D_INDEX_TO_2D,

        EFFORT_VALUE_1D_INDEX_TO_2D,
        EFFORT_VALUE_1D_INDEX_TO_2D,
        EFFORT_VALUE_1D_INDEX_TO_2D,
        EFFORT_VALUE_1D_INDEX_TO_2D,
        EFFORT_VALUE_1D_INDEX_TO_2D,
        EFFORT_VALUE_1D_INDEX_TO_2D
    ]

    DEPTH = len(FEATURE_INDEX_1D_TO_2D_LIST)
    DEPTH_COUNTER = (i for i in range(DEPTH))

    POKE_NAME_DEPTH = next(DEPTH_COUNTER)
    POKE_TYPES_DEPTH = next(DEPTH_COUNTER)
    LEARNSET_DEPTH = next(DEPTH_COUNTER)
    BASE_HP_DEPTH = next(DEPTH_COUNTER)
    BASE_ATK_DEPTH = next(DEPTH_COUNTER)
    BASAE_DEF_DEPTH = next(DEPTH_COUNTER)
    BASE_SP_ATK_DEPTH = next(DEPTH_COUNTER)
    BASE_SP_DEF_DEPTH = next(DEPTH_COUNTER)
    BASE_SPEED_DEPTH = next(DEPTH_COUNTER)

    NATURE_DEPTH = next(DEPTH_COUNTER)
    ABILITY_DEPTH = next(DEPTH_COUNTER)
    GENDER_DEPTH = next(DEPTH_COUNTER)
    ITEM_DEPTH = next(DEPTH_COUNTER)

    MOVE1_NAME_DEPTH = next(DEPTH_COUNTER)
    MOVE1_TYPE_DEPTH = next(DEPTH_COUNTER)
    MOVE1_POWER_DEPTH = next(DEPTH_COUNTER)
    MOVE1_ACCURACY_DEPTH = next(DEPTH_COUNTER)
    MOVE1_HALF_HEAL_DEPTH = next(DEPTH_COUNTER)
    MOVE1_ONE_HIT_KO_DEPTH = next(DEPTH_COUNTER)

    MOVE2_NAME_DEPTH = next(DEPTH_COUNTER)
    MOVE2_TYPE_DEPTH = next(DEPTH_COUNTER)
    MOVE2_POWER_DEPTH = next(DEPTH_COUNTER)
    MOVE2_ACCURACY_DEPTH = next(DEPTH_COUNTER)
    MOVE2_HALF_HEAL_DEPTH = next(DEPTH_COUNTER)
    MOVE2_ONE_HIT_KO_DEPTH = next(DEPTH_COUNTER)

    MOVE3_NAME_DEPTH = next(DEPTH_COUNTER)
    MOVE3_TYPE_DEPTH = next(DEPTH_COUNTER)
    MOVE3_POWER_DEPTH = next(DEPTH_COUNTER)
    MOVE3_ACCURACY_DEPTH = next(DEPTH_COUNTER)
    MOVE3_HALF_HEAL_DEPTH = next(DEPTH_COUNTER)
    MOVE3_ONE_HIT_KO_DEPTH = next(DEPTH_COUNTER)

    MOVE4_NAME_DEPTH = next(DEPTH_COUNTER)
    MOVE4_TYPE_DEPTH = next(DEPTH_COUNTER)
    MOVE4_POWER_DEPTH = next(DEPTH_COUNTER)
    MOVE4_ACCURACY_DEPTH = next(DEPTH_COUNTER)
    MOVE4_HALF_HEAL_DEPTH = next(DEPTH_COUNTER)
    MOVE4_ONE_HIT_KO_DEPTH = next(DEPTH_COUNTER)

    POINT_UP1_DEPTH = next(DEPTH_COUNTER)
    POINT_UP2_DEPTH = next(DEPTH_COUNTER)
    POINT_UP3_DEPTH = next(DEPTH_COUNTER)
    POINT_UP4_DEPTH = next(DEPTH_COUNTER)

    INDIVIDUAL_HP_DEPTH = next(DEPTH_COUNTER)
    INDIVIDUAL_ATK_DEPTH = next(DEPTH_COUNTER)
    INDIVIDUAL_DEF_DEPTH = next(DEPTH_COUNTER)
    INDIVIDUAL_SP_ATK_DEPTH = next(DEPTH_COUNTER)
    INDIVIDUAL_SP_DEF_DEPTH = next(DEPTH_COUNTER)
    INDIVIDUAL_SPEED_DEPTH = next(DEPTH_COUNTER)

    EFFORT_HP_DEPTH = next(DEPTH_COUNTER)
    EFFORT_ATK_DEPTH = next(DEPTH_COUNTER)
    EFFORT_DEF_DEPTH = next(DEPTH_COUNTER)
    EFFORT_SP_ATK_DEPTH = next(DEPTH_COUNTER)
    EFFORT_SP_DEF_DEPTH = next(DEPTH_COUNTER)
    EFFORT_SPEED_DEPTH = next(DEPTH_COUNTER)

    def __init__(self):
        self.data = [[[0 for d in range(BinaryImageTeamPokemon.DEPTH)] \
                      for w in range(BinaryImageTeamPokemon.WIDTH)] \
                      for h in range(BinaryImageTeamPokemon.HEIGHT)]
        self.poke_name = None
        self.nature = None
        self.ability = None
        self.gender = None
        self.item = None
        self.move_names = []
        self.point_ups = []
        self.individual = None
        self.individual = None

    def print_2d(self, depth):
        height = BinaryImageTeamPokemon.HEIGHT
        width = BinaryImageTeamPokemon.WIDTH
        v = [[self.data[h][w][depth] for w in range(width)] for h in range(height)]
        for ele in v:
            print(ele)

    def is_all_zero(self, depth):
        return all([self.data[h][w][depth] == 0 for h in range(BinaryImageTeamPokemon.HEIGHT) \
                    for w in range(BinaryImageTeamPokemon.WIDTH)])

    def count(self, v, depth):
        return [self.data[h][w][depth] for h in range(BinaryImageTeamPokemon.HEIGHT) \
                                       for w in range(BinaryImageTeamPokemon.WIDTH)].count(v)

    def set_features(self, all_features, features, depth, assert_msg):
        assert self.is_all_zero(depth), assert_msg
        index_1d_to_2d = BinaryImageTeamPokemon.FEATURE_INDEX_1D_TO_2D_LIST[depth]

        for feature in features:
            index = all_features.index(feature)
            for h, w in range(index):
                self.data[h][w][depth] = 1

    def set_poke_name(self, poke_name):
        self.set_features(parts.RATE_POKE_NAMES, [poke_name], BinaryImageTeamPokemon.POKE_NAME_DEPTH,
                          "ポケモン名を再入力しようとした")
        poke_data = POKEDEX[poke_name]
        self.set_features(parts.ALL_TYPES, poke_data.types, BinaryImageTeamPokemon.POKE_TYPE_DEPTH,
                          "ポケモンのタイプを再度入力しようとした")
        self.set_features(parts.ALL_MOVE_NAMES, poke_data.learnset, BinaryImageTeamPokemon.LEARNSET_DEPTH,
                          "覚える事が出来る技を再度入力しようとした")
        self.set_features(ALL_BASE_STATES, [poke_data.base_hp], BinaryImageTeamPokemon.BASE_HP_STATE_DEPTH,
                          "HP種族値を再度入力しようとした")
        self.set_features(ALL_BASE_STATES, [poke_data.base_atk], BinaryImageTeamPokemon.BASE_ATK_STATE_DEPTH,
                          "攻撃種族値を再度入力しようとした")
        self.set_features(ALL_BASE_STATES, [poke_data.base_def], BinaryImageTeamPokemon.BASE_DEF_STATE_DEPTH,
                          "防御種族値を再度入力しようとした")
        self.set_features(ALL_BASE_STATES, [poke_data.base_sp_atk], BinaryImageTeamPokemon.BASE_SP_ATK_STATE_DEPTH,
                          "特攻種族値を再度入力しようとした")
        self.set_features(ALL_BASE_STATES, [poke_data.base_sp_def], BinaryImageTeamPokemon.BASE_SP_DEF_STATE_DEPTH,
                          "特防種族値を再度入力しようとした")
        self.set_features(ALL_BASE_STATES, [poke_data.base_speed], BinaryImageTeamPokemon.BASE_SPEED_STATE_DEPTH,
                          "素早さ種族値を再度入力しようとした")
        self.poke_name = poke_name

    def set_nature(self, nature):
        self.set_features(parts.ALL_NATURES, [nature], BinaryImageTeamPokemon.NATURE_DEPTH,
                          "性格を再度入力しようとした")

    def set_ability(self, ability):
        assert self.name is not None
        assert ability in POKEDEX[self.name].all_abilities
        self.set_features(parts.ALL_ABILITIES, [ability], BinaryImageTeamPokemon.ABILITY_DEPTH,
                          "特性を再度入力しようとした")

    def set_gender(self, gender):
        assert self.name is not None
        assert gender in valid_genders(poke_name, gender)
        self.set_features(parts.ALL_GENDERS, [gender], BinaryImageTeamPokemon.GENDER_DEPTH,
                          "性別を再度入力しようとした")

    def set_item(self, item):
        self.set_features(parts.ALL_ITEMS, [item], BinaryImageTeamPokemon.ITEM_DEPTH,
                          "アイテムを再度入力しようとした")

    def set_move_name(self, move_name, depth):
        poke_data = POKEDEX[poke_name]

        assert move_name in ALL_MOVE_NAMES

        depth_index = [MOVE1_NAME_DEPTH, MOVE2_NAME_DEPTH, MOVE3_NAME_DEPTH, MOVE4_NAME_DEPTH].index(depth)
        move_type_depth = [MOVE1_TYPE_DEPTH, MOVE2_TYPE_DEPTH, MOVE3_TYPE_DEPTH, MOVE4_TYPE_DEPTH][index]
        move_power_depth = [MOVE1_POWER_DEPTH, MOVE2_POWER_DEPTH, MOVE3_POWER_DEPTH, MOVE4_POWER_DEPTH][index]
        accuracy_depth = [MOVE1_ACCURACY_DEPTH, MOVE2_ACCURACY_DEPTH, MOVE3_ACCURACY_DEPTH, MOVE4_ACCURACY_DEPTH][index]
        half_heal_depth = [MOVE1_HALF_HEAL, MOVE2_HALF_HEAL, MOVE3_HALF_HEAL, MOVE4_HALF_HEAL][index]
        one_hit_ko_depth = [MOVE1_ONE_HIT_KO, MOVE2_ONE_HIT_KO, MOVE3_ONE_HIT_KO, MOVE4_ONE_HIT_KO][index]

        index = ALL_MOVE_NAMES.index(move_name)
        for h, w in range(INDEX_1D_TO_2D[index]):
            assert self.data[h][w][depth] == 0
            self.data[h][w][depth] = 1

        move_data = MOVEDEX[move_name]
        self.set_features(parts.ALL_TYPES, [move_data.type], move_type_depth, "技タイプを再度入力しようとした")

        if move_data.power > 0:
            if move_data.type in poke_data.types:
                power = int(power * 1.5)
            else:
                power = move_data.power
            self.set_features(ALL_MOVE_POWERS, power, move_power_depth, "技威力を再度入力しようとした")

        accuracy = move_data.accuracy
        if accuracy == -1:
            accuracy = 100

        if accuracy != 0:
            self.set_features(ALL_ACCURACY, [accuracy], accuracy_depth, "命中率が再度入力された")

        if move_name in parts.HALF_HEAL_MOVE_NAMES:
            for h in range(BinaryImageTeamPokemon.HEIGHT):
                for w in range(BinaryImageTeamPokemon.WIDTH):
                    assert self.data[h][w][half_heal_depth] == 0
                    self.data[h][w][half_heal_depth] = 1

        if move_name in parts.ONE_HIT_KO_MOVE_NAMES:
            for h in range(BinaryImageTeamPokemon.HEIGHT):
                for w in range(BinaryImageTeamPokemon.WIDTH):
                    assert self.data[h][w][half_heal_depth] == 0
                    self.data[h][w][one_hit_ko_depth] = 1

    def set_move1_name(self, move_name):
        assert move_name != "なし"
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE1_NAME_DEPTH)

    def set_move2_name(self, move_name):
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE2_NAME_DEPTH)

    def set_move3_name(self, move_name):
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE3_NAME_DEPTH)

    def set_move4_name(self, move_name):
        self.set_move_name(move_name, BinaryImageTeamPokemon.MOVE4_NAME_DEPTH)

    def set_point_up(self, point_up, depth):
        assert is_valid_point_up(point_up)
        assert self.count(1, BinaryImageTeamPokemon.MOVE_NAMES_DEPTH) == MAX_MOVESET_NUM

        self.set_features(parts.ALL_POINT_UPS, [point_up], BinaryImageTeamPokemon.POINT_UP_DEPTH,
                          "ポイントアップを再度入力しようとした")

    def set_individual_v(self, individual_v, depth, state_type):
        assert individual_v in ALL_INDIVIDUAL_VALUES
        self.set_features(parts.ALL_INDIVIDUAL_VALUES, [individual_v], depth, "個体値" + state_type + "を再入力した")

    def set_individual_hp(self, individual_v):
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_HP_DEPTH, "HP")

    def set_individual_atk(self, individual_v):
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_ATK_DEPTH, "攻撃")

    def set_individual_def(self, individual_v):
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_DEF_DEPTH, "防御")

    def set_individual_sp_atk(self, individual_v):
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_SP_ATK_DEPTH, "特攻")

    def set_individual_sp_def(self, individual_v):
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_SP_DEF_DEPTH, "特防")

    def set_individual_speed(self, individual_v):
        self.set_individual_v(individual_v, BinaryImageTeamPokemon.INDIVIDUAL_SPEED_DEPTH, "素早さ")

    def set_effort_v(self, effort_v, depth, state_type):
        assert effort_v in parts.ALL_EFFORT_VALUES
        self.set_features(parts.ALL_EFFORT_VALUES, [effort_v], depth, "努力値" + state_type + "を再入力した")

    def set_effort_hp(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_HP_DEPTH, "HP")

    def set_effort_atk(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_ATK_DEPTH, "攻撃")

    def set_effort_def(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_DEF_DEPTH, "防御")

    def set_effort_sp_atk(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_SP_ATK_DEPTH, "特攻")

    def set_effort_sp_def(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_SP_DEF_DEPTH, "特防")

    def set_effort_speed(self, effort_v):
        self.set_effort_v(effort_v, BinaryImageTeamPokemon.EFFORT_SPEED_DEPTH, "素早さ")

binary_image_team_pokemon = BinaryImageTeamPokemon()
