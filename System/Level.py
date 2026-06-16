from Logic.Combat import shoot
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
    
    while player.is_alive() and enemy.is_alive(): # level loop
        shotgun.reload()

        current_turn = "player"


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
                print(f"===ENEMY TURN===\nHP: {player.currentHp}\nEnemyHP: {enemy.currentHp}\n\nCurrent Level: {level}\n")
                if shoot(enemy, player, shotgun) == "blank":
                    print("enemy shoot nothing to player")
                else:
                    print("Enemy hit the player!")
                current_turn = "player"
            
            if not player.is_alive() or not enemy.is_alive():
                break
            
            time.sleep(2)
            os.system('cls')

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

    player.items.clear()
    enemy.items.clear()

    player.maxHp += 2
    player.currentHp = player.maxHp

    enemy.maxHp += 2
    enemy.currentHp = enemy.maxHp

    return level