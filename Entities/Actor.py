class Actor:
    def __init__(self):
        self.maxHp = 2
        self.currentHp = self.maxHp
        self.items = []
        self.damage = 1
    
    def take_damage(self, amount):
        self.currentHp -= amount

    def is_alive(self):
        return self.currentHp > 0
    
    def use_item(self, index):
        item = self.items.pop(index)
        item.use(self)

    def obtain_item(self, item):
        self.items.append(item)

    def level_up(self):
        self.maxHp += 2
        self.currentHp = self.maxHp