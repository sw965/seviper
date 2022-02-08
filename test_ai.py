import seviper.parts as parts

for move_name, move_data in parts.MOVEDEX.items():
    if move_data.min_attack_num > 1:
        print(move_name, move_data.min_attack_num, move_data.max_attack_num)
