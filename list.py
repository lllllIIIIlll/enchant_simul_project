import json

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

table_path = "list_table.json"
rate_path = "list_rate.json"

table = load_json(table_path)

level = list(range(1, 31))
level_try = table["level_try"]
success = table["success"]
m_s = table["m_s"]
mini_game_success = table.get("mini_game_success", [0]*30)  # 추가

a_s_rate = []
a_try = []
m_s_rate = []

for i in range(30):
    if level_try[i] > 0:
        s_rate = success[i] / level_try[i]
        a_s_rate.append(s_rate)
        a_try.append(1 / s_rate if s_rate > 0 else 0)
        # 미니게임 성공 시 강화 성공 확률 = m_s / mini_game_success
        if mini_game_success[i] > 0:
            m_s_rate.append(m_s[i] / mini_game_success[i])
        else:
            m_s_rate.append(0)
    else:
        a_s_rate.append(0)
        a_try.append(0)
        m_s_rate.append(0)

rate_data = {
    "level": level,
    "a_try": a_try,
    "a_s_rate": a_s_rate,
    "m_s_rate": m_s_rate
}

save_json(rate_path, rate_data)

def load_table_data():
    data = load_json("list_rate.json")
    level = data["level"]
    a_try = data["a_try"]
    a_s_rate = data["a_s_rate"]
    m_s_rate = data["m_s_rate"]
    table_data = [["강화 단계", "평균 시도 횟수", "평균 성공률", "미니게임 성공 성공률"]]
    for i in range(30):
        table_data.append([
            str(level[i]),
            f"{a_try[i]:.2f}",
            f"{a_s_rate[i]*100:.2f}%",
            f"{m_s_rate[i]*100:.2f}%"
        ])
    return table_data

def reset_json():
    # list_rate.json 초기화
    data = load_json("list_rate.json")
    for key in data:
        if key != "level":
            data[key] = [0]*30
    save_json("list_rate.json", data)
    # list_table.json 초기화
    table_data = load_json("list_table.json")
    for key in table_data:
        if key != "level":
            table_data[key] = [0]*30
    # mini_game_success도 0으로 초기화
    if "mini_game_success" in table_data:
        table_data["mini_game_success"] = [0]*30
    save_json("list_table.json", table_data)
