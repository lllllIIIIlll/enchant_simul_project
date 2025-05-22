import random

def enchant(enchant_level, mini_game):
    base_success_rate = 0.9

    # 감소치 계산 (성공확률이 0.3 미만이 되기 전까지)
    reduction = enchant_level * 0.05
    temp_success_rate = base_success_rate - reduction
    if temp_success_rate < 0.3:
        reduction = base_success_rate - 0.3
        temp_success_rate = 0.3

    # 미니게임 성공 확률 (곱셈)
    mini_success = mini_enchant(mini_game, enchant_level)
    success_rate = temp_success_rate * (1 + mini_success)

    # 파괴 확률
    destroy_rate = 0.001 + enchant_level * 0.005

    # 실패 확률
    fail_rate = 1 - success_rate - destroy_rate

    # 결과 결정
    rand = random.random()
    if rand < success_rate:
        return "성공"
    elif rand < success_rate + fail_rate:
        return "실패"
    else:
        return "파괴"

def mini_enchant(mini_game, enchant_level):
    if mini_game == "성공":
        return 0.05 * enchant_level
    elif mini_game == "실패":
        return 0