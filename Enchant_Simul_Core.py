import random

class Item:
    def __init__(self, name):
        self.name = name
        self.level = 0

    def get_success_rate(self):
        rates = {
            0: 1.00, 1: 0.90, 2: 0.80, 3: 0.70,
            4: 0.60, 5: 0.50, 6: 0.40, 7: 0.30,
            8: 0.20, 9: 0.10
        }
        return rates.get(self.level, 0.05)

    def handle_failure(self):
        self.level = max(0, self.level - 1)

    def upgrade(self, bonus_rate=0.0):
        base_rate = self.get_success_rate()
        total_rate = min(1.0, base_rate + bonus_rate)
        success = random.random() < total_rate
        if success:
            self.level += 1
        else:
            self.handle_failure()
        return success, total_rate