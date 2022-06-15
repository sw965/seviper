import seviper.base_data as base_data
import seviper.parts as parts

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
    move_data = base_data.MOVEDEX[move_name]
    assert move_data.category != parts.STATUS, \
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
    move_data = base_data.MOVEDEX[move_name]

    if move_data.category == parts.PHYSICS:
        attack_state = battle.p1_fighters[0].atk
        rank = battle.p1_fighters[0].atk_rank
        attack_bonus = get_physics_attack_bonus(battle)
    elif move_data.category == parts.SPECIAL:
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
    category = base_data.MOVEDEX[move_name].category

    if category == parts.PHYSICS:
        defense_state = battle.p1_fighters[0].defe
        rank = battle.p1_fighters[0].def_rank
        defense_bonus = get_physics_defense_bonus(battle)
    elif category == parts.SPECIAL:
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
    move_type = base_data.MOVEDEX[move_name].type
    if move_type in pokemon.types:
        return 6144.0 / 4096.0
    else:
        return 1.0

def get_effectiveness_bonus(pokemon, move_name):
    result = 1.0
    move_type = base_data.MOVEDEX[move_name].type
    for poke_type in pokemon.types:
        result *= base_data.TYPEDEX[move_type][poke_type]
    return result

INIT_DAMAGE_BONUS = 4096

def get_damage_bonus(battle):
    result = INIT_DAMAGE_BONUS
    if battle.p1_fighters[0].item == "いのちのたま":
        result = five_over_rounding(float(result) * 5324.0 / 4096.0)
    return result

RANDOM_DAMAGE_BONUSES = [
    0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0
]

RANDOM_DAMAGE_BONUSES_LENGTH = len(RANDOM_DAMAGE_BONUSES)

def get_final_damage(battle, move_name, random_damage_bonus, is_critical):
    move_data = base_data.MOVEDEX[move_name]

    final_power = get_final_power(battle, move_name)
    final_attack = get_final_attack(battle, move_name, is_critical)
    final_defense = get_final_defense(battle.reverse(), move_name, is_critical)

    critical_bonus = CRITICAL_BONUS[is_critical]
    stab = get_same_type_attack_bonus(battle.p1_fighters[0], move_name)
    effectiveness_bonus = get_effectiveness_bonus(battle.p2_fighters[0], move_name)
    damage_bonus = get_damage_bonus(battle)

    result = parts.DEFAULT_LEVEL*2//5 + 2
    result = int(float(result) * float(final_power) * float(final_attack) / float(final_defense))
    result = result // 50 + 2
    result = five_over_rounding(float(result) * critical_bonus)
    result = int(float(result) * random_damage_bonus)
    result = five_over_rounding(float(result) * stab)
    result = int(float(result) * effectiveness_bonus)
    result = five_over_rounding(float(result) * float(damage_bonus) / 4096.0)
    return result
