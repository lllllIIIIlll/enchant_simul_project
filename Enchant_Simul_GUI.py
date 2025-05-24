import tkinter as tk
from tkinter import messagebox
from Enchant_Simul_Core import Item
from Enchant_Simul_MiniGame import play_guessing_game

class EnhanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("강화 시뮬레이터")
        self.item = Item("전설의 검")

        self.status_label = tk.Label(root, text=f"현재 단계: {self.item.level}강", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.guess_entry = tk.Entry(root, font=("Arial", 12))
        self.guess_entry.pack(pady=5)

        self.guess_button = tk.Button(root, text="숫자 맞추기 미니게임 (1~5)", command=self.play_minigame)
        self.guess_button.pack(pady=5)

        self.upgrade_button = tk.Button(root, text="강화 시도", command=self.try_upgrade, state=tk.DISABLED)
        self.upgrade_button.pack(pady=10)

        self.log_box = tk.Text(root, height=10, width=40, state='disabled')
        self.log_box.pack()

        self.bonus_rate = 0.0

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.config(state='disabled')
        self.log_box.see(tk.END)

    def play_minigame(self):
        user_input = self.guess_entry.get()
        success, correct = play_guessing_game(user_input)
        if success:
            self.bonus_rate = 0.05
            messagebox.showinfo("미니게임", f"정답! 강화 확률 +5%!")
        else:
            self.bonus_rate = 0.0
            messagebox.showinfo("미니게임", f"실패! 정답은 {correct}였습니다.")
        self.upgrade_button.config(state=tk.NORMAL)

    def try_upgrade(self):
        success, rate = self.item.upgrade(self.bonus_rate)
        result = "성공!" if success else "실패!"
        self.log(f"{self.item.level}강 도전 ({rate*100:.1f}%) ➡️ {result}")
        self.status_label.config(text=f"현재 단계: {self.item.level}강")
        self.bonus_rate = 0.0
        self.upgrade_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhanceApp(root)
    root.mainloop()
