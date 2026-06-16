import random

class Shotgun:
    
    def __init__(self):
        self.bullets = []
        self.damage = 1
    
    def reload(self):

        quantity = random.randint(2, 8) # determine the # of bullets by picking randomly between 2 - 8

        # --- Random assigment of live and blank bullets ---
        live = random.randint(1, (quantity-1)) # ensure that there will be at least 1 live and all bullets aren't live
        blank = quantity - live # the remaining bullets will be the blank bullet.

        shells = []

        # --- Randomizing the order ---
        for x in range(quantity): # adding the live and blank bullets to bullet list
            if x < live:
                shells.append("live")
            else:
                shells.append("blank")

        print(shells)

        random.shuffle(shells)

        print(shells)

        self.bullets = shells   

    def fire(self):
        if len(self.bullets) == 0:
            return None
        
        return self.bullets.pop(0)

    def peek_current_shell(self):
        if len(self.bullets) > 0:
            return self.bullets[0]
        
        return None