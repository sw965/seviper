import copy
import itertools
import numpy as np
import seviper.parts as parts
import seviper.battle as battle

BUILD_POKE_NAME_FEATURES = ["なし"] + parts.RATE_POKE_NAMES
BATTLE_POKE_NAME_FEATURES = parts.RATE_POKE_NAMES

BASE_HP_FEATURES = [state + 1 for state in range(parts.MAX_BASE_HP)]
BASE_STATE_FEATURES = [state + 1 for state in range(parts.MAX_BASE_STATE)]
HP_FEATURES = [i + 1 for i in range(parts.MAX_HP)]
STATE_FEATURES = [i + 1 for i in range(parts.MAX_STATE)]

MOVE_NAME_FEATURES = ["なし"] + parts.ALL_MOVE_NAMES
MOVE_POWER_FEATURES = [power + 1 for power in range(parts.MAX_MOVE_POWER)]
MOVE_ACCURACY_FEATURES = [i + 1 for i in range(100)]
POWER_POINT_FEATURES = [i + 1 for i in range(parts.MAX_POWER_POINT)]

ITEM_FEATURES = ["なし"] + parts.ALL_ITEMS

class Image2D:
    SIZE = Image2D.size()
    HEIGHT = BINARY_IMAGE_2D_SIZE[0]
    WIDTH = BINARY_IMAGE_2D_SIZE[1]
    INDICES = [(h, w) for h in range(HEIGHT) for w in range(WIDTH)]

    @classmethod
    def new():
        return [[0 for w in range(Image2D.WIDTH)] for h in range(Image2D.HEIGHT)]

    @classmethod
    def size():
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

    @classmethod
    def print(image_2d):
        v = [[self.v[h][w] for w in range(Image2D.WIDTH)] for h in range(Image2D.HEIGHT)]
        for ele in v:
            print(ele)

    @classmethod
    def logical_disjunction(image_2d1, image_2d2):
        return [[image_2d1[h][w] | image_2d2[h][w] for w in range(Image2D.WIDTH)] for h in range(Image2D.HEIGHT)]


def input_ranges(features_length, is_inclusion_mode):
    count = (i for i in range(len(Image2D.INDICES)))
    result = [[Image2D.INDICES[next(count)] for j in range(len(Image2D.INDICES) // features_length)] \
               for i in range(features_length)]

    if is_inclusion_mode:
        return list(itertools.accumulate(result))
    else:
        return result


class FeatureValueTable:
    BUILD_POKE_NAME = FeatureValueTable.new(BUILD_POKE_NAME_FEATURES, False)
    BATTLE_POKE_NAME = FeatureValueTable.new(BATTLE_POKE_NAME_FEATURES, False)
    TYPE = FeatureValueTable.new(parts.ALL_TYPES, False)

    MOVE_NAME = FeatureValueTable.new(MOVE_NAME_FEATURES, False)
    LEARNSET = FeatureValueTable.new(parts.ALL_MOVE_NAMES, False)

    BASE_HP = FeatureValueTable.new(BASE_HP_FEATURES, True)
    BASE_STATE = FeatureValueTable.new(BASE_STATE_FEATURES, True)

    HP = FeatureValueTable.new(HP_FEATURES, True)
    STATE = FeatureValueTable.new(STATE_FEATURES, True)

    NATURE = FeatureValueTable.new(parts.ALL_NATURES, False)
    ABILITY = FeatureValueTable.new(parts.ALL_ABILITIES, False)
    GENDER = FeatureValueTable.new(parts.ALL_GENDERS, False)
    ITEM = FeatureValueTable.new(parts.ALL_ITEMS, False)

    MOVE_POWER = FeatureValueTable.new(MOVE_POWER_FEATURES, True)
    MOVE_ACCURACY = FeatureValueTable.new(MOVE_ACCURACY_FEATURES, True)
    HALF_HEAL = FeatureValueTable.new_half_heal()
    ONE_HIT_KO = FeatureValueTable.new_one_hit_ko()

    POINT_UP = FeatureValueTable.new(parts.ALL_POINT_UPS, True)
    POWER_POINT = FeatureValueTable.new(POWER_POINT_FEATURES, True)

    INDIVIDUAL_VALUE = FeatureValueTable.new(parts.ALL_INDIVIDUAL_VALUES, True)
    EFFORT_VALUE = FeatureValueTable.new(parts.ALL_EFFORT_VALUES, True)

    @classmethod
    def new(features, is_inclusion_mode):
        input_ranges = input_ranges(len(features), is_inclusion_mode)
        result = {}
        for feature in features:
            index = features.index(feature)
            v = Image2D.new()
            for h, w in input_ranges[index]:
                v[h][w] = 1

        image_2d = Image2D(v)
        result[feature] = image_2d
        return result

    @classmethod
    def new_half_heal():
        result = {}
        result[True] = [[1 for w in range(Image2D.WIDTH)] for h in range(Image2D.HEIGHT)]
        result[False] = Image2D.new()
        return result

    @classmethod
    def new_one_hit_ko():
        result = {}
        result[True] = [[1 for w in range(Image2D.WIDTH)] for h in range(Image2D.HEIGHT)]
        result[False] = Image2D.new()
        return result

    @classmethod
    def logical_disjunction(feature_values, keys):
        result = feature_values[keys[0]]
        for key in keys[1:]:
            result = Image2D.logical_disjunction(result, feature_values[key])
        return result


class PokemonBuilder:
    DEPTH = 57
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
        FeatureValueTable.POKE_NAME,
        FeatureValueTable.TYPE,
        FeatureValueTable.LEARNSET,
        FeatureValueTable.BASE_HP,
        FeatureValueTable.BASE_STATE,
        FeatureValueTable.BASE_STATE,
        FeatureValueTable.BASE_STATE,
        FeatureValueTable.BASE_STATE,
        FeatureValueTable.BASE_STATE,

        FeatureValueTable.NATURE,
        FeatureValueTable.ABILITY,
        FeatureValueTable.GENDER,
        FeatureValueTable.ITEM,

        FeatureValueTable.MOVE_NAME,
        FeatureValueTable.TYPE,
        FeatureValueTable.MOVE_POWER,
        FeatureValueTable.MOVE_ACCURACY,
        FeatureValueTable.HALF_HEAL,
        FeatureValueTable.ONE_HIT_KO,

        FeatureValueTable.MOVE_NAME,
        FeatureValueTable.TYPE,
        FeatureValueTable.MOVE_POWER,
        FeatureValueTable.MOVE_ACCURACY,
        FeatureValueTable.HALF_HEAL,
        FeatureValueTable.ONE_HIT_KO,

        FeatureValueTable.MOVE_NAME,
        FeatureValueTable.TYPE,
        FeatureValueTable.MOVE_POWER,
        FeatureValueTable.MOVE_ACCURACY,
        FeatureValueTable.HALF_HEAL,
        FeatureValueTable.ONE_HIT_KO,

        FeatureValueTable.MOVE_NAME,
        FeatureValueTable.TYPE,
        FeatureValueTable.MOVE_POWER,
        FeatureValueTable.MOVE_ACCURACY,
        FeatureValueTable.HALF_HEAL,
        FeatureValueTable.ONE_HIT_KO,

        FeatureValueTable.POINT_UP,
        FeatureValueTable.POINT_UP,
        FeatureValueTable.POINT_UP,
        FeatureValueTable.POINT_UP,

        FeatureValueTable.INDIVIDUAL_VALUE,
        FeatureValueTable.INDIVIDUAL_VALUE,
        FeatureValueTable.INDIVIDUAL_VALUE,
        FeatureValueTable.INDIVIDUAL_VALUE,
        FeatureValueTable.INDIVIDUAL_VALUE,
        FeatureValueTable.INDIVIDUAL_VALUE,

        FeatureValueTable.EFFORT_VALUE,
        FeatureValueTable.EFFORT_VALUE,
        FeatureValueTable.EFFORT_VALUE,
        FeatureValueTable.EFFORT_VALUE,
        FeatureValueTable.EFFORT_VALUE,
        FeatureValueTable.EFFORT_VALUE,
    ]

    assert len(TABLES) == (EFFORT_SPEED_DEPTH + 1)

    def __init__(self):
        data_2d = [Image2D([0 for w in range(Image2D.WIDTH)]) for h in range(Image2D.HEIGHT)]
        self.data = [copy.deepcopy(data_2d) for _ in range(PokemonBuilder.DEPTH)]

        self.poke_name = None
        self.nature = None
        self.ability = None
        self.gender = None
        self.item = None
        self.move_names = [None, None, None, None]
        self.point_ups = [None, None, None, None]
        self.individual = parts.Individual(None, None, None, None, None, None)
        self.effort = parts.Effort(None, None, None, None, None, None)

    def set_features(self, features, depth):
        table = PokemonBuilder.TABLES[depth]
        self.data[depth] = FeatureValueTable.logical_disjunction(table, features)

    def set_poke_name(self, poke_name):
        assert self.poke_name is None, "ポケモン名は既に入力済み"
        self.set_features([poke_name], PokemonBuilder.POKE_NAME_DEPTH)
        poke_data = POKEDEX[poke_name]
        self.set_features(poke_data.types, PokemonBuilder.POKE_TYPE_DEPTH)
        self.set_features(poke_data.learnset, PokemonBuilder.LEARNSET_DEPTH)
        self.set_features([poke_data.base_hp], PokemonBuilder.BASE_HP_DEPTH)
        self.set_features([poke_data.base_atk], PokemonBuilder.BASE_ATK_DEPTH)
        self.set_features([poke_data.base_def], PokemonBuilder.BASE_DEF_DEPTH)
        self.set_features([poke_data.base_sp_atk], PokemonBuilder.BASE_SP_ATK_DEPTH)
        self.set_features([poke_data.base_sp_def], PokemonBuilder.BASE_SP_DEF_DEPTH)
        self.set_features([poke_data.base_speed], PokemonBuilder.BASE_SPEED_DEPTH)
        self.poke_name = poke_name

    def set_nature(self, nature):
        assert self.nature is None, "性格は既に入力済み"
        self.set_features([nature], PokemonBuilder.NATURE_DEPTH)
        self.nature = nature

    def set_ability(self, ability):
        assert self.poke_name is not None, "特性を入力する時は、ポケモン名を入力してからでなければならない"
        assert self.ability is None, "特性は既に入力済み"
        assert ability in POKEDEX[self.name].all_abilities, "特性: " + ability + "と ポケモン名: " + poke_name + "の組み合わせは不適"
        self.set_features([ability], PokemonBuilder.ABILITY_DEPTH)
        self.ability = ability

    def set_gender(self, gender):
        assert self.poke_name is not None, "性別を入力する時は、ポケモン名を入力してからでなければならない"
        assert self.gender is None, "性別は既に入力済み"
        assert gender in valid_genders(poke_name, gender)
        self.set_features([gender], PokemonBuilder.GENDER_DEPTH)
        self.gender = gender

    def set_item(self, item):
        assert self.item is None, "アイテムは既に入力済み"
        self.set_feature([item], PokemonBuilder.ITEM_DEPTH)
        self.item = item

    def set_move_name(self, move_name, depth):
        assert self.poke_name is not None, "技名を入力する時は、ポケモン名を入力してからでなければならない"
        depth_i = [MOVE1_NAME_DEPTH, MOVE2_NAME_DEPTH, MOVE3_NAME_DEPTH, MOVE4_NAME_DEPTH].index(depth)
        assert self.move_names[depth_i] is None
        assert self.move_names.count(None) == battle.MAX_MOVESET_NUM - (depth_i - 1)

        move_type_depth = [MOVE1_TYPE_DEPTH, MOVE2_TYPE_DEPTH, MOVE3_TYPE_DEPTH, MOVE4_TYPE_DEPTH][depth_i]
        move_power_depth = [MOVE1_POWER_DEPTH, MOVE2_POWER_DEPTH, MOVE3_POWER_DEPTH, MOVE4_POWER_DEPTH][depth_i]
        accuracy_depth = [MOVE1_ACCURACY_DEPTH, MOVE2_ACCURACY_DEPTH, MOVE3_ACCURACY_DEPTH, MOVE4_ACCURACY_DEPTH][depth_i]
        half_heal_depth = [MOVE1_HALF_HEAL, MOVE2_HALF_HEAL, MOVE3_HALF_HEAL, MOVE4_HALF_HEAL][depth_i]
        one_hit_ko_depth = [MOVE1_ONE_HIT_KO, MOVE2_ONE_HIT_KO, MOVE3_ONE_HIT_KO, MOVE4_ONE_HIT_KO][depth_i]

        poke_data = POKEDEX[poke_name]
        move_data = MOVEDEX[move_name]

        self.set_features([move_name], depth)
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
        self.set_move_name(move_name, PokemonBuilder.MOVE1_NAME_DEPTH)
        self.move_names[0] = move_name

    def set_move2_name(self, move_name):
        assert move_name in ["なし"] + POKEDEX[self.poke_name].learnset
        self.set_move_name(move_name, PokemonBuilder.MOVE2_NAME_DEPTH)
        self.move_names[1] = move_name

    def set_move3_name(self, move_name):
        assert move_name in ["なし"] + POKEDEX[self.poke_name].learnset
        self.set_move_name(move_name, PokemonBuilder.MOVE3_NAME_DEPTH)
        self.move_names[2] = move_name

    def set_move4_name(self, move_name):
        assert move_name in ["なし"] + POKEDEX[self.poke_name].learnset
        self.set_move_name(move_name, PokemonBuilder.MOVE4_NAME_DEPTH)
        self.move_names[3] = move_name

    def set_point_up(self, point_up, depth):
        assert parts.is_valid_point_up(point_up)
        self.set_features([point_up], depth)

    def set_point_up1(self, point_up):
        assert self.move_names[0] is not None
        assert self.point_ups[0] is None
        self.set_point_up(point_up, PokemonBuilder.POINT_UP1_DEPTH)
        self.point_ups[0] = point_up

    def set_point_up2(self, point_up):
        assert self.move_names[1] is not None
        assert self.point_ups[1] is None
        self.set_point_up(point_up, PokemonBuilder.POINT_UP2_DEPTH)
        self.point_ups[1] = point_up

    def set_point_up3(self, point_up):
        assert self.move_names[2] is not None
        assert self.point_ups[2] is None
        self.set_point_up(point_up, PokemonBuilder.POINT_UP3_DEPTH)
        self.point_ups[2] = point_up

    def set_point_up4(self, point_up):
        assert self.move_names[3] is not None
        assert self.point_ups[3] is None
        self.set_point_up(point_up, PokemonBuilder.POINT_UP4_DEPTH)
        self.point_ups[3] = point_up

    def set_individual_v(self, individual_v, depth, state_type):
        assert individual_v in ALL_INDIVIDUAL_VALUES
        self.set_features([individual_v], depth)

    def set_individual_hp(self, individual_v):
        assert self.individual.hp is None
        self.set_individual_v(individual_v, PokemonBuilder.INDIVIDUAL_HP_DEPTH)
        self.individual.hp = individual_v

    def set_individual_atk(self, individual_v):
        assert self.individual.atk is None
        self.set_individual_v(individual_v, PokemonBuilder.INDIVIDUAL_ATK_DEPTH)
        self.individual.atk = individual_v

    def set_individual_def(self, individual_v):
        assert self.individual.defe is None
        self.set_individual_v(individual_v, PokemonBuilder.INDIVIDUAL_DEF_DEPTH)
        self.individual.defe = individual_v

    def set_individual_sp_atk(self, individual_v):
        assert self.individual.sp_atk is None
        self.set_individual_v(individual_v, PokemonBuilder.INDIVIDUAL_SP_ATK_DEPTH)
        self.individual.sp_atk = individual_v

    def set_individual_sp_def(self, individual_v):
        assert self.individual.sp_def is None
        self.set_individual_v(individual_v, PokemonBuilder.INDIVIDUAL_SP_DEF_DEPTH)
        self.individual.sp_def = individual_v

    def set_individual_speed(self, individual_v):
        assert self.individual.speed is None
        self.set_individual_v(individual_v, PokemonBuilder.INDIVIDUAL_SPEED_DEPTH)
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
        self.set_effort_v(effort_v, PokemonBuilder.EFFORT_HP_DEPTH)
        self.effort.hp = effort_v

    def set_effort_atk(self, effort_v):
        self.set_effort_v(effort_v, PokemonBuilder.EFFORT_ATK_DEPTH)
        self.effort.atk = effort_v

    def set_effort_def(self, effort_v):
        self.set_effort_v(effort_v, PokemonBuilder.EFFORT_DEF_DEPTH)
        self.effort.defe = effort_v

    def set_effort_sp_atk(self, effort_v):
        self.set_effort_v(effort_v, PokemonBuilder.EFFORT_SP_ATK_DEPTH)
        self.effort.sp_atk = effort_v

    def set_effort_sp_def(self, effort_v):
        self.set_effort_v(effort_v, PokemonBuilder.EFFORT_SP_DEF_DEPTH)
        self.effort.sp_def = effort

    def set_effort_speed(self, effort_v):
        self.set_effort_v(effort_v, PokemonBuilder.EFFORT_SPEED_DEPTH)
        self.effort.speed = effort_v


class TeamBuilder:
    def __init__(self):
        self.builders = [PokemonBuilder() for _ in range(battle.MAX_TEAM_NUM)]

    def get(self):
        return sum([builder.data for builder in self.builders], [])

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


class ImageBattlePokemon:
    DEPTH = 26
    depth_counter = (i for i in range(DEPTH))

    POKE_NAME_DEPTH = next(depth_counter)
    POKE_TYPE_DEPTH = next(depth_counter)
    NATURE_DEPTH = next(depth_counter)
    ABILITY_DEPTH = next(depth_counter)
    GENDER_DEPTH = next(depth_counter)
    ITEM_DEPTH = next(depth_counter)

    MOVE_NAME_DEPTH = next(depth_counter)

    MOVE1_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE2_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE3_HALF_HEAL_DEPTH = next(depth_counter)
    MOVE4_HALF_HEAL_DEPTH = next(depth_counter)

    MAX_POWER_POINT1_DEPTH = next(depth)
    CURRENT_POWER_POINT1_DEPTH = next(depth)
    MAX_POWER_POINT2_DEPTH = next(depth)
    CURRENT_POWER_POINT2_DEPTH = next(depth)
    MAX_POWER_POINT3_DEPTH = next(depth)
    CURRENT_POWER_POINT3_DEPTH = next(depth)
    MAX_POWER_POINT4_DEPTH = next(depth)
    CURRENT_POWER_POINT4_DEPTH = next(depth)

    MAX_HP_DEPTH = next(depth_counter)
    CURRENT_HP_DEPTH = next(depth_counter)
    ATK_DEPTH = next(depth_counter)
    DEF_DEPTH = next(depth_counter)
    SP_ATK_DEPTH = next(depth_counter)
    SP_DEF_DEPTH = next(depth_counter)
    SPEED_DEPTH = next(depth_counter)

    def __init__(self, pokemon):
        ibp = ImageBattlePokemon
        fvt = FeatureValueTable
        self.data = [Image2D.new() for _ in range(ImageBattlePokemon.DEPTH)]
        poke_data = POKEDEX[pokemon.name]

        self.data[ibp.POKE_NAME_DEPTH] = fvt.POKE_NAME[pokemon.name]
        self.data[ibp.POKE_TYPE_DEPTH] = fvt.logical_disjunction(fvt.TYPE, pokemon.types)
        self.data[ibp.NATURE_DEPTH] = fvt.NATURE[pokemon.nature]
        self.data[ibp.ABILITY_DEPTH] = fvt.ABILITY[pokemon.ability]
        self.data[ibp.ITEM_DEPTH] = fvt.ITEM[pokemon.item]

        half_heal_depths = [ibp.MOVE1_HALF_HEAL_DEPTH, ibp.MOVE2_HALF_HEAL_DEPTH, ibp.MOVE3_HALF_HEAL_DEPTH, ibp.MOVE4_HALF_HEAL_DEPTH]
        max_power_point_depths = [ibp.MAX_POWER_POINT1_DEPTH, ibp.MAX_POWER_POINT2_DEPTH, ibp.MAX_POWER_POINT3_DEPTH, ibp.MAX_POWER_POINT4_DEPTH]
        current_power_point_depths = [ibp.CURRENT_POWER_POINT1_DEPTH, ibp.CURRENT_POWER_POINT2_DEPTH, ibp.CURRENT_POWER_POINT3_DEPTH, ibp.CURRENT_POWER_POINT4_DEPTH]
        order_move_names = pokemon.moveset_order_keys()
        self.data[ibp.MOVE_NAME_DEPTH] = fvt.logical_disjunction(fvt.LEARNSET, order_move_names)

        for i, move_name in enumerate(order_move_names):
            half_heal_depth = half_heal_depths[i]
            max_power_point_depth = max_power_point_depths[i]
            current_power_point_depth = current_power_point_depths[i]

            self.data[half_heal_depth] = fvt.HALF_HEAL[move_name in parts.HALF_HEAL_MOVE_NAMES]
            self.data[max_power_point_depth] = fvt.POWER_POINT[power_point.max]
            self.data[current_power_point_depth] = fvt.POWER_POINT[power_point.current]

        self.data[ibp.MAX_HP_DEPTH] = fvt.HP[pokemon.max_hp]
        if pokemon.current_hp != 0:
            self.data[ibp.CURRENT_HP_DEPTH] = fvt.HP[pokemon.current_hp]
        self.data[ibp.ATK_DEPTH] = fvt.STATE[pokemon.atk]
        self.data[ibp.DEF_DEPTH] = fvt.STATE[pokemon.defe]
        self.data[ibp.SP_ATK_DEPTH] = fvt.STATE[pokemon.sp_atk]
        self.data[ibp.SP_DEF_DEPTH] = fvt.STATE[pokemon.sp_def]
        self.data[ibp.SPEED_DEPTH] = fvt.STATE[pokemon.speed]


class ImageFighters:
    def __init__(self, fighters):
        self.images = [ImageBattlePokemon() for _ in range(battle.FIGHTERS_NUM)]

    def get(self):
        return sum([image.data for image in self.images])


class ImageBattle:
    def __init__(self, p1_fighters, p2_fighters):
        self.p1_fighter_images = ImageFighters(p1_fighters)
        self.p2_fighter_images = ImageFighters(p2_fighters)

    def damage_probability_distribution():
