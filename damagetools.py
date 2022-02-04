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
	after_the_decimal_point := float(x) - float(int(x))
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

def final_power(spovb, move_name):
    move_data = MOVEDEX[move_name]
    assert move_data.category != STATUS, \
        "ダメージ計算関連のメソッドは、物理技か変化技の技名でなければならない"

    result = five_over_rounding(float(move_data.power) * float(INIT_POWER_BONUS) / 4096.0)
    if result < 1:
        return 1
    else:
        return result

def physics_attack_bonus(spovb):
    result = INIT_PHYSICS_ATTACK_BONUS
    if spovb.self_fighters[0].item == "こだわりハチマキ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def special_attack_bonus(spovb):
    result = INIT_SPECIAL_ATTACK_BONUS
    if spovb.self_fighters[0].item == "こだわりメガネ":
        result = five_over_rounding(float(result) * 6144.0 / 4096.0)
    return result

def final_attack(spovb, move_name, is_critical):
    move_data = parts.MOVEDEX[move_name]

    if move_data.category == PHYSICS:
        attack_state = spovb.self_fighters[0].atk
        rank = spovb.self_fighters[0].atk_rank
        attack_bonus = physics_attack_bonus()
    elif move_data.category == SPECIAL:
        attack_state = spovb.self_fighters[0].sp_atk
        rank = spovb.self_fighters[0].sp_atk_rank
        attack_bonus = special_attack_bonus()
    else:
        assert False, "ダメージ計算関連の関数で、変化技の技名が入力された"

    if (rank < 0) and is_critical:
        rank = 0

    rank_bonus = RANK_BONUS[rank]

    result = int(float(attack_state) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(attack_bonus))

    if result < 1:
        return 1
    else:
        return result

INIT_PHYSICS_DEFENSE_BONUS = 4096
INIT_SPECIAL_DEFENSE_BONUS = 4096
INIT_DEFENSE_BONUS = 4096

def special_defense_bonus(spovb):
    result = INIT_SPECIAL_DEFENSE_BONUS
    if spovb.self_fighters[0].item == "とつげきチョッキ":
        result = five_or_more_rounding(float(result) * 6144.0 / 4096.0)
    return result

def finel_defense(spovb, move_name, is_critical):
    category = parts.MOVEDEX[move_name].category

    if category == PHYSICS:
        defense_state = spovb.self_fighters[0].defe
        rank = spovb.self_fighters[0].def_rank
        defense_bonus = INIT_PHYSICS_DEFENSE_BONUS
    elif category == SPECIAL:
        defense_state = spovb.self_fighters[0].sp_def
        rank = spovb.self_fighters[0].sp_def_rank
        defense_bonus = special_defense_bonus(spovb)
    else:
        assert False, "ダメージ計算関連の関数で、変化技の技名が入力された"

    if rank > 0 && is_critical:
        rank = 0

    rank_bonus = RANK_BONUS[rank]

    result = int(float(defense_state) * float(rank_bonus))
    result = five_over_rounding(float(result) * float(defense_bonus) / 4096.0)

    if result < 1:
        return 1
    else:
        return result

def same_type_attack_bonus(pokemon, move_name):
    move_type = MOVEDEX[move_name].type
    if move_type in pokemon.types:
        return 6144.0 / 4096.0
    else:
        return 1.0

def effectiveness_bonus(pokemon, move_name):
    result = 1.0
    move_type = MOVEDEX[move_name].type
    for poke_type in pokemon.types:
        result *= parts.TYPEDEX[move_type][poke_type]
    return result

INIT_DAMAGE_BONUS = 4096

def damage_bonus(spovb):
    result = INIT_DAMAGE_BONUS
    if spovb.self_fighters[0].item == "いのちのたま":
        result = five_over_rounding(float(result) * 5324.0 / 4096.0)
    return result

FINAL_DAMAGE_RANDOM_BONUSES = [
    0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0
]

def final_damage(spovb, move_name, is_critical):
    move_data = MOVEDEX[move_name]
    opovb = spovb.reverse()

    final_power_v = final_power(spovb, move_name)
    final_attack_v = final_attack(spovb, move_name)
    final_defense = final_defense(opovb, move_name)

    critical_bonus = CRITICAL_BONUS[is_critical]
    stab = same_type_attack_bonus(spovb.self_fighters[0], move_name)
    effectiveness_bonus_v = effectiveness_bonus(spovb.opponent_fighters[0], move_name)
    damage_bonus_v = damage_bonus()

    result = DEFAULT_LEVEL*2/5 + 2
    result = int(float(result) * float(final_power_v) * float(final_attack_v) / float(final_defense_v))
    result = result / 50 + 2
    result = five_over_rounding(float(result) * critical_bonus)
    result = int(float(result) * random.choice(FINAL_DAMAGE_RANDOM_BONUSES))
    result = five_over_rounding(float(result) * same_type_attack_bonus)
    result = int(float(result) * effectiveness_bonus_v)
    result = five_over_rounding(float(result) * damage_bonus_v / 4096.0)
    return result
