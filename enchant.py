import random

def enchant(enchant_level, mini_game):
    base_success_rate = 0.9

    reduction = enchant_level * 0.05
    temp_success_rate = base_success_rate - reduction
    if temp_success_rate < 0.3:
        reduction = base_success_rate - 0.3
        temp_success_rate = 0.3

    mini_success = mini_enchant(mini_game, enchant_level)
    success_rate = temp_success_rate * (1 + mini_success)

    destroy_rate = 0.001 + enchant_level * 0.005
    fail_rate = 1 - success_rate - destroy_rate

    rand = random.random()
    if rand < success_rate:
        return 1
    elif rand < success_rate + fail_rate:
        return 2
    else:
        return 0

def mini_enchant(mini_game, enchant_level):
    if mini_game == 1:
        return 0.05 * enchant_level
    elif mini_game == 2:
        return 0