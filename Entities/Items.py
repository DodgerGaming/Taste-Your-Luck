class Items:
    def __init__(self, name):
        self.name = name

    def use(self, user):
        pass


class Hp_Pill(Items):
    def __init__(self):
        super().__init__("Hp pill")

    def use(self, user):
        user.current_Hp += 1


class Monster_Drink(Items):
    def __init__(self):
        super().__init__("Monster drink")

    def use(self, shotgun):
        shell = shotgun.bullets.pop(0)
        print(f"{shell} has been ejected to chamber")
        

class Hacksaw(Items):
    def __init__(self):
        super().__init__("Hacksaw")

    def use(self, user):
        user.damage += 1


class Xray(Items):
    def __init__(self):
        super().__init__("Xray glasses")

    def use(self, shotgun):
        shotgun.show_current_shell()