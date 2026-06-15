class Actor:
    def __init__(self):
        self.maxHp = 2
        self.currentHp = self.maxHp
        self.items = []
    
    def take_damage(self, amount):
        self.currentHp -= amount

    def is_alive(self):
        return self.currentHp > 0
    
    def level_up(self):
        self.maxHp += 2
        self.currentHp = self.maxHp