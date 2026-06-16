
class Actor:
    # MAX_ITEMS = 8

    def __init__(self):
        self.maxHp = 2
        self.currentHp = self.maxHp
        # self.items = []
        self.damage_multiplier = 1
    
    def take_damage(self, amount):
        self.currentHp -= amount
        
        if self.currentHp < 0: # validation for over damage
            self.currentHp = 0

    def is_alive(self):
        return self.currentHp > 0
    
    """
    def use_item(self, index, shotgun):
        item = self.items.pop(index)
        item.use(self, shotgun)

    def obtain_item(self, item):
        if len(self.items) < self.MAX_ITEMS:
            self.items.append(item)
    """

    def level_up(self):
        self.maxHp += 2
        self.currentHp = self.maxHp

    def heal(self, amount):
        self.currentHp += amount 
        
        if self.currentHp > self.maxHp: # validation for overheal
            self.currentHp = self.maxHp