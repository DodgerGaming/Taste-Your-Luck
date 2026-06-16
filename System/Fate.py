import random

def draw_fate_card(level):

    if level == 1:
        return None

    if level == 2:
        chance = 50
    else:
        chance = 75

    roll = random.randint(1, 100)

    if roll > chance:
        return None
    
    card = random.choice([
        "fortune",
        "devil",
        "hanged_man"
    ])

    return card

def apply_fate_card(card, player, shotgun):
    if card == "fortune":
        print("=== FORTUNE ACTIVATES! ===")
        effect = random.choice([
            "hp up",
            "damage up",
            "none"
        ])

        if effect == "hp up":
            player.heal(1)
            print("Player recover 1 hp!")

        elif effect == "damage up":
            print("Player damage goes up by 1!")
            player.damage_multiplier += 1

        else:
            print("Nothing happens...")

        return effect
        
    elif card == "devil":
        shotgun.damage += 1
        print("=== DEVIL ACTIVATED!")
        print("Shotgun damage increased!")

    elif card == "death":
        print("=== DEATH ACTIVATES! ===")
        shotgun.damage = 10

    elif card == "hanged_man":
        pass