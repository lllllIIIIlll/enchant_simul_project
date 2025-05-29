import json

# 파일 경로
table_path = "list_table.json"
rate_path = "list_rate.json"

# 데이터 불러오기
with open(table_path, encoding="utf-8") as f:
    table = json.load(f)

level = list(range(1, 31))
level_try = table["level_try"]
success = table["success"]
m_s = table["m_s"]
mini_game_success = table.get("mini_game_success", [0]*30)

a_s_rate = []
a_try = []
m_s_rate = []

for i in range(30):
    # a_s_rate: 해당 레벨 성공 횟수 / 해당 레벨 시도 횟수
    if level_try[i] > 0:
        a_s = success[i] / level_try[i]
        a_s_rate.append(a_s)
    else:
        a_s_rate.append(0)

# a_try: 1 / 성공확률(a_s_rate)
for i in range(30):
    if a_s_rate[i] > 0:
        a_try.append(1 / a_s_rate[i])
    else:
        a_try.append(0)

# m_s_rate: 미니게임 성공 횟수 / 해당 레벨 시도 횟수
for i in range(30):
    if level_try[i] > 0:
        m_s_rate.append(m_s[i] / level_try[i])
    else:
        m_s_rate.append(0)

# 결과 저장
rate_data = {
    "level": level,
    "a_try": a_try,
    "a_s_rate": a_s_rate,
    "m_s_rate": m_s_rate
}

with open(rate_path, "w", encoding="utf-8") as f:
    json.dump(rate_data, f, ensure_ascii=False, indent=2)