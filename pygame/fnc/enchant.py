import rate

def enchant(equipment, enchant_level, mini_game_result=0):
    result = rate.enchant_rate(enchant_level, mini_game_result)
    if result == 0:
        enchant_level = 0
        equipment["image1"] 
        msg = "파괴되었습니다"
    elif result == 1:
        enchant_level += 1
        msg = "강화 성공"
    elif result == 2:
        msg = "강화 실패"
    elif result == 3:
        msg = "더 이상 강화할 수 없습니다"
    else:
        msg = "알 수 없는 결과"
    return enchant_level, msg