import random
import seviper.parts as parts
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

def final_power(spov, move_name):
    move_data = parts.MOVEDEX[move_name]
    assert move_data.category != parts.STATUS, \
        "ダメージ計算関連のメソッドは、物理技か変化技の技名でなければならない"

    result = five_over_rounding(float(move_data.power) * float(INIT_POWER_BONUS) / 4096.0)
    return max([result, 1])

def physics_attack_bonus(spov):
    result = INIT_PHYSICS_ATTACK_BONUS
    if spov.self_fighters[0].item == "こだわりハチマキ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def special_attack_bonus(spov):
    result = INIT_SPECIAL_ATTACK_BONUS
    if spov.self_fighters[0].item == "こだわりメガネ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def final_attack(spov, move_name, is_critical):
    move_data = parts.MOVEDEX[move_name]

    if move_data.category == parts.PHYSICS:
        attack_state = spov.self_fighters[0].atk
        rank = spov.self_fighters[0].atk_rank
        attack_bonus = physics_attack_bonus(spov)
    elif move_data.category == parts.SPECIAL:
        attack_state = spov.self_fighters[0].sp_atk
        rank = spov.self_fighters[0].sp_atk_rank
        attack_bonus = special_attack_bonus(spov)
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

def physics_defense_bonus(spov):
	result = INIT_PHYSICS_DEFENSE_BONUS
	return result

def special_defense_bonus(spov):
    result = INIT_SPECIAL_DEFENSE_BONUS
    if spov.self_fighters[0].item == "とつげきチョッキ":
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def final_defense(spov, move_name, is_critical):
    category = parts.MOVEDEX[move_name].category

    if category == parts.PHYSICS:
        defense_state = spov.self_fighters[0].defe
        rank = spov.self_fighters[0].def_rank
        defense_bonus = physics_defense_bonus(spov)
    elif category == parts.SPECIAL:
        defense_state = spov.self_fighters[0].sp_def
        rank = spov.self_fighters[0].sp_def_rank
        defense_bonus = special_defense_bonus(spov)
    else:
        assert False, "ダメージ計算関連の関数で、変化技の技名が入力された"

    if (rank > 0) and is_critical:
        rank = 0

    rank_bonus = RANK_BONUS[rank]

    result = int(float(defense_state) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(defense_bonus) / 4096.0)
    return max([result, 1])

def same_type_attack_bonus(pokemon, move_name):
    move_type = parts.MOVEDEX[move_name].type
    if move_type in pokemon.types:
        return 6144.0 / 4096.0
    else:
        return 1.0

def effectiveness_bonus(pokemon, move_name):
    result = 1.0
    move_type = parts.MOVEDEX[move_name].type
    for poke_type in pokemon.types:
        result *= parts.TYPEDEX[move_type][poke_type]
    return result

INIT_DAMAGE_BONUS = 4096

def damage_bonus(spov):
    result = INIT_DAMAGE_BONUS
    if spov.self_fighters[0].item == "いのちのたま":
        result = five_over_rounding(float(result) * 5324.0 / 4096.0)
    return result

FINAL_DAMAGE_RANDOM_BONUSES = [
    0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0
]

FINAL_DAMAGE_RANDOM_BONUSES_LENGTH = len(FINAL_DAMAGE_RANDOM_BONUSES)

def final_damage(spov, move_name, final_damage_random_bonus, is_critical):
    move_data = parts.MOVEDEX[move_name]
    opov = spov.reverse()

    final_power_v = final_power(spov, move_name)
    final_attack_v = final_attack(spov, move_name, is_critical)
    final_defense_v = final_defense(opov, move_name, is_critical)

    critical_bonus = CRITICAL_BONUS[is_critical]
    stab = same_type_attack_bonus(spov.self_fighters[0], move_name)
    effectiveness_bonus_v = effectiveness_bonus(spov.opponent_fighters[0], move_name)
    damage_bonus_v = damage_bonus(spov)

    result = parts.DEFAULT_LEVEL*2//5 + 2
    result = int(float(result) * float(final_power_v) * float(final_attack_v) / float(final_defense_v))
    result = result // 50 + 2
    result = five_over_rounding(float(result) * critical_bonus)
    result = int(float(result) * final_damage_random_bonus)
    result = five_over_rounding(float(result) * stab)
    result = int(float(result) * effectiveness_bonus_v)
    result = five_over_rounding(float(result) * float(damage_bonus_v) / 4096.0)
    return result

def damage_probability_distribution(spov, move_name):
	critical_n = spov.critical_n(move_name)
	critical_p = 1.0 / float(critical_n)
	no_critical_p = 1.0 - critical_p
	bool_to_critical_p = {True:critical_p, False:no_critical_p}
	accuracy_p = spov.real_accuracy(move_name) / 100.0
	final_damage_random_bonus_p = 1.0 / float(FINAL_DAMAGE_RANDOM_BONUSES_LENGTH)

	result = {0:1.0 - accuracy_p}

	for is_critical in [False, True]:
		for final_damage_random_bonus in FINAL_DAMAGE_RANDOM_BONUSES:
			final_damage_v = final_damage(spov, move_name, final_damage_random_bonus, is_critical)
			p = accuracy_p * final_damage_random_bonus_p * bool_to_critical_p[is_critical]

			if final_damage_v not in result:
				result[final_damage_v] = p
			else:
				#確率の加法定理
			    result[final_damage_v] += p
	return result
