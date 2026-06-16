import random
from Entities.Items import (Hp_Pill, Xray, Hacksaw)

def generate_random_item():

    item_pool = [
        Hp_Pill,
        Xray,
        Hacksaw
    ]

    return random.choice(item_pool)()