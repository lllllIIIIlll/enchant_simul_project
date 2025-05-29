import random

base_rate = [
    (0.95, 0.0), (0.90, 0.0), (0.85, 0.0), (0.85, 0.0), (0.80, 0.0),
    (0.75, 0.0), (0.70, 0.0), (0.65, 0.0), (0.60, 0.0), (0.55, 0.0),
    (0.50, 0.0), (0.45, 0.0), (0.40, 0.0), (0.35, 0.0), (0.30, 0.021),
    (0.30, 0.021), (0.30, 0.068), (0.15, 0.068), (0.15, 0.085), (0.15, 0.105),
    (0.30, 0.1275), (0.15, 0.17), (0.15, 0.18), (0.10, 0.18), (0.10, 0.18),
    (0.07, 0.186), (0.05, 0.19), (0.03, 0.194), (0.10, 0.198), (0.10, 0.198)
]
if len(base_rate) != 30:
    raise ValueError(f"base_rate의 길이는 30이어야 합니다. 현재: {len(base_rate)}")

input_rate = base_rate.copy()

def get_input_rate():
    if len(input_rate) != 30:
        raise ValueError(f"input_rate의 길이는 30이어야 합니다. 현재: {len(input_rate)}")
    return input_rate

def set_input_rate(new_rate):
    global input_rate
    if len(new_rate) != 30:
        raise ValueError("input_rate의 길이는 30이어야 합니다.")
    input_rate = new_rate.copy()

def enchant_rate(enchant_level, mini_game):
  
    if enchant_level < 0 or enchant_level > 29:
        return 3 

    base_success, destroy_rate = input_rate[enchant_level]
    success_rate = base_success * (1 + mini_enchant(mini_game))
    
    rand = random.random()
    if rand < success_rate:
        print(f"Enchant success: {success_rate}, Destroy rate: {destroy_rate}, mini_game bonus: {mini_enchant(mini_game)}")  # 디버깅용 출력
        return 1  
    elif rand < destroy_rate:
        print(f"Enchant success: {success_rate}, Destroy rate: {destroy_rate}, mini_game bonus: {mini_enchant(mini_game)}")
        return 0 
    else:
        print(f"Enchant success: {success_rate}, Destroy rate: {destroy_rate}, mini_game bonus: {mini_enchant(mini_game)}") 
        return 2  

def mini_enchant(mini_game):
    if mini_game == 1:
        return 0.05
    return 0

