import enchant

def main():
    equipment = "무기"
    enchant_level = 10
    mini_game = "성공"  



    for i in range(100):
        result = enchant.enchant(enchant_level, mini_game)
        print(f"장비: {equipment}, 강화 레벨: {enchant_level}, 미니게임 결과: {mini_game}, 강화 결과: {result}")

if __name__ == "__main__":
    main()