from Logic.Combat import shoot
from System.Fate import draw_fate_card
from System.Fate import apply_fate_card
from AI_Logic.AI import get_ai_choice
import os
import time
    
"""
def item_distribution(player, enemy, level):
    
    if level == 2:
        amount = 2
    elif level == 4:
        amount = 4

    for _ in range(amount):
        player.obtain(generate_random_item())

        enemy.obtain(generate_random_item())
"""

def play_level(player, enemy, shotgun, level):
    final_showdown = False


    while player.is_alive() and enemy.is_alive(): # level loop
        shotgun.reload()
        
        if not final_showdown: # removing buff each round unless final showdown
            shotgun.damage = 1
            player.damage_multiplier = 1
        
        current_turn = "player"

    # -- Application of fate cards --
        if final_showdown:
            current_fate = "death"
        else:
            current_fate = draw_fate_card(level)
            apply_fate_card(current_fate, player, shotgun)


        while len(shotgun.bullets) > 0: # round loop

            # --- Player Turn ---
            if current_turn == "player":
                print(f"===PLAYER TURN===\nHP: {player.currentHp}\nEnemyHP: {enemy.currentHp}\nCurrent Level: {level}\n")
                choice = int(input("What'll you do?\n1.Shoot enemy\n2. Shoot self\n\n"))
                
                if choice == 1:
                    if shoot(player, enemy, shotgun) == "blank":
                        print("Player shot nothing to enemy")
                    else:
                        print("Player hit the enemy!")
                    
                    current_turn = "enemy"

                elif choice == 2:
                    if shoot(player, player, shotgun) == "blank":
                        current_turn = "player"
                        print("Player dodged the bullet of death\n\n")
                    else:
                        print("Tough luck boy\n\n")
                        current_turn = "enemy"
            # --- Enemy Turn ---
            else:
                print(f"===ENEMY TURN===\nHP: {player.currentHp}\nEnemyHP: {enemy.currentHp}\nCurrent Level: {level}\n")
                choice = get_ai_choice(player, enemy, shotgun, current_fate, level)

                if choice == 1:
                    if shoot(enemy, player, shotgun) == "blank":
                        print("Enemy shot nothing to player")
                    else:
                        print("Enemy hit the player!")

                else:
                    if shoot(enemy, enemy, shotgun) == "blank":
                        print("Enemy dodged the bullet of death")
                    else:
                        print("Enemy shot itself!")

                current_turn = "player"


            if not player.is_alive() or not enemy.is_alive():
                break


        # --- Checking if player trigger final showdown ---
            final_showdown = check_final_showdown(player, enemy, level, final_showdown)
            
            if final_showdown:
                current_fate = "death"
                apply_fate_card(current_fate, player, shotgun)

            
            time.sleep(2)
            #os.system('cls')

    # --- Determining who won ---
    if player.is_alive():
        if level < 3:
            print("You won, proceeding to next stage")

        time.sleep(2)
        
        return "player"
    else:
        return "enemy"


def next_level(player, enemy, level):
    level += 1

    # player.items.clear()
    # enemy.items.clear()

    player.maxHp += 2
    player.currentHp = player.maxHp

    enemy.maxHp += 2
    enemy.currentHp = enemy.maxHp

    return level

def check_final_showdown(player, enemy, level, final_showdown):

    if (level == 3 and not final_showdown and (player.currentHp <= 2 or enemy.currentHp <= 2)):
        return True

    return final_showdown