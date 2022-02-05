def leftovers(spovb):
    if spovb.self_fighters[0].item != "たべのこし":
        return spovb

    if spovb.self_fighters[0].is_faint():
        return spovb

    if spovb.self_fighters[0].is_full_hp():
        return spovb

    heal = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 16.0)
    spovb = spovb.heal(heal)
    return spovb

def black_sludge(spovb):
    if spovb.self_fighters[0].item != "くろいヘドロ":
        return spovb

    if spovb.self_fighters[0].is_faint():
        return spovb

    if parts.POISON in spovb.self_fighters[0].types:
        heal = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 16.0)
        spovb = spovb.Heal(heal)
    else:
        damage = int(float(spovb.self_fighters[0].max_hp) * 1.0 / 8.0)
        spovb = spovb.damage(damage)
    return spovb

def leech_seed(spovb):
    if spovb.self_fighters[0].is_faint():
        return spovb

    if spovb.opponent_fighters[0].is_faint():
        return spovb

    if not spovb.opponent_fighters[0].is_leech_seed:
        return spovb

    damage = int(float(spovb.opponent_fighters[0].max_hp) * 1.0 / 8.0)
    heal = damage

    opovb = spovb.reverse()
    opovb = opovb.damage(damage)
    spovb = opovb.reverse()
    spovb = spovb.heal(heal)
    return spovb

def bad_poison(spovb):
    if spovb.self_fighters[0].status_ailment != BAD_POISON:
        return spovb

    if spovb.self_fighters[0].bad_poison_elapsed_turn < 16:
        spovb.self_fighters[0].bad_poison_elapsed_turn += 1

    damage = int(float(spovb.self_fighters[0].max_hp) * float(spovb.self_fighters[0].bad_poison_elapsed_turn) / 16.0)
    if damage < 1:
        damage = 1
    return spovb.damage(damage)
