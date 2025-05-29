import json

table_path = "list_table.json"
rate_path = "list_rate.json"

with open(table_path, encoding="utf-8") as f:
    table = json.load(f)

level = list(range(1, 31))
level_try = table["level_try"]
success = table["success"]
m_s = table["m_s"]

a_s_rate = []
a_try = []
m_s_rate = []

for i in range(30):
    if level_try[i] > 0:
        s_rate = success[i] / level_try[i]
        a_s_rate.append(s_rate)
        a_try.append(1 / s_rate if s_rate > 0 else 0)
        if m_s[i] > 0:
            m_s_rate.append(1-(1-s_rate/1.05)**level[i])
        else:
            m_s_rate.append(s_rate)
    else:
        a_s_rate.append(0)
        a_try.append(0)
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