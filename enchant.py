import enchant_rate

def enchant(equipment, enchant_level):
  
    result = enchant_rate.enchant_rate(enchant_level, 1)  # 0,1,2,3 중 하나 반환
    print(f"Enchant result: {result}")  # 디버깅용 출력
    if result == 0:
        enchant_level = 0
        equipment["image1"] = equipment["image2"]
        result_msg = "파괴되었습니다"
    elif result == 1:
        enchant_level += 1
        result_msg = "성공"
    elif result == 2:
        result_msg = "실패"
        enchant_level = enchant_level
    elif result == 3:
        result_msg = "더 이상 강화할 수 없습니다"
        enchant_level = enchant_level
    else:
        result_msg = "알 수 없는 결과"
        enchant_level = enchant_level

    return enchant_level, result_msg