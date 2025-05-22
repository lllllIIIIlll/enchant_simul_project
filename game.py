import enchant
import tkinter as tk

# 전역 변수로 강화 레벨 관리
equipment_level = 1

def do_enchant():
    global equipment_level
    mini_game = "성공"  # 예시로 항상 성공 처리
    result = enchant.enchant(equipment_level, mini_game)
    if result == "성공":
        equipment_level += 1
    elif result == "파괴":
        equipment_level = 1
    # 실패 시에는 변화 없음
    result_label.config(text=f"강화 결과: {result} (현재 강화 레벨: {equipment_level})")
    level_var.set(str(equipment_level))

root = tk.Tk()
root.title("강화 시뮬레이터")

tk.Label(root, text="장비: 무기").pack()
tk.Label(root, text="강화 레벨:").pack()

level_var = tk.StringVar(value="1")
level_entry = tk.Entry(root, textvariable=level_var)
level_entry.pack()

enchant_button = tk.Button(root, text="강화하기", command=do_enchant)
enchant_button.pack()

result_label = tk.Label(root, text="강화 결과: ")
result_label.pack()

root.mainloop()

