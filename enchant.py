import random
import time
import math 

def enchant(enchant_level, equipment):
    base_success_rate = 0.9

    # 감소치 계산 (성공확률이 0.3 미만이 되기 전까지)
    reduction = enchant_level * 0.05
    temp_success_rate = base_success_rate - reduction
    if temp_success_rate < 0.3:
        reduction = base_success_rate - 0.3
        temp_success_rate = 0.3

    # 미니게임 성공 확률 (곱셈)
    mini_success = mini_enchant(equipment, enchant_level)
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

def mini_enchant(game, enchant_level):
    # 미니 게임 성공 시 최종 강화 성공 확률을 증가시키는 함수 (곱셈용 비율 반환)
    if game:
        return enchant_level * 0.05
    else:
        return 0.0
