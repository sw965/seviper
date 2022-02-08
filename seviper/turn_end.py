import seviper.parts as parts

#https://latest.pokewiki.net/%E3%83%90%E3%83%88%E3%83%AB%E4%B8%AD%E3%81%AE%E5%87%A6%E7%90%86%E3%81%AE%E9%A0%86%E7%95%AA

def leftovers(spov):
    if spov.self_fighters[0].item != "たべのこし":
        return spov

    if spov.self_fighters[0].is_faint():
        return spov

    if spov.self_fighters[0].is_full_hp():
        return spov

    heal = int(float(spov.self_fighters[0].max_hp) * 1.0 / 16.0)
    spov = spov.heal(heal)
    return spov

def black_sludge(spov):
    if spov.self_fighters[0].item != "くろいヘドロ":
        return spov

    if spov.self_fighters[0].is_faint():
        return spov

    if parts.POISON in spov.self_fighters[0].types:
        heal = int(float(spov.self_fighters[0].max_hp) * 1.0 / 16.0)
        spov = spov.heal(heal)
    else:
        damage = int(float(spov.self_fighters[0].max_hp) * 1.0 / 8.0)
        spov = spov.damage(damage)
    return spov

def leech_seed(spov):
    if spov.self_fighters[0].is_faint():
        return spov

    if spov.opponent_fighters[0].is_faint():
        return spov

    if not spov.opponent_fighters[0].is_leech_seed:
        return spov

    damage = int(float(spov.opponent_fighters[0].max_hp) * 1.0 / 8.0)
    heal = damage

    opov = spov.reverse()
    opov = opov.damage(damage)
    spov = opov.reverse()
    spov = spov.heal(heal)
    return spov

def bad_poison(spov):
    if spov.self_fighters[0].status_ailment != parts.BAD_POISON:
        return spov

    if spov.self_fighters[0].bad_poison_elapsed_turn < 16:
        spov.self_fighters[0].bad_poison_elapsed_turn += 1

    damage = int(float(spov.self_fighters[0].max_hp) * float(spov.self_fighters[0].bad_poison_elapsed_turn) / 16.0)
    if damage < 1:
        damage = 1
    return spov.damage(damage)
