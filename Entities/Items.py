class Items:
    def __init__(self, name):
        self.name = name

    def use(self, user, shotgun):
        pass


class Hp_Pill(Items):
    def __init__(self):
        super().__init__("Hp pill")

    def use(self, user, shotgun):
        user.currentHp += 1


class Monster_Drink(Items):
    def __init__(self):
        super().__init__("Monster drink")

    def use(self, user, shotgun):
        shell = shotgun.bullets.pop(0)
        print(f"{shell} has been ejected to chamber")
        

class Hacksaw(Items):
    def __init__(self):
        super().__init__("Hacksaw")

    def use(self, user, shotgun):
        user.damage_multiplier += 1


class Xray(Items):
    def __init__(self):
        super().__init__("Xray glasses")

    def use(self, user, shotgun):
        print(f"The current chamber is: {shotgun.peek_current_shell()}")