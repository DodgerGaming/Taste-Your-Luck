from Logic.Combat import shoot
import os

def play_round(player, enemy, shotgun):
    


    while player.is_alive() and enemy.is_alive():
        shotgun.reload()

        current_turn = "player"


        while len(shotgun.bullets) > 0:

            # --- Player Turn ---
            if current_turn == "player":
                print(f"===PLAYER TURN===\nHP:{player.currentHp}\n")
                choice = int(input("What'll you do?\n1.Shoot enemy\n2. Shoot self\n3.Use Item\n\n"))
                
                if choice == 1:
                    shoot(enemy, shotgun)
                    current_turn = "enemy"
                elif choice == 2:
                    if shoot(player, shotgun) == "blank":
                        current_turn == "player"
                        print("Player dodged the bullet of death\n\n")
                    else:
                        print("Tough luck boy\n\n")
                        current_turn == "enemy"
                else: #TODO: add item implementation
                    pass

            # --- Enemy Turn ---
            else:
                print(f"===ENEMY TURN===\nHP:{enemy.currentHp}\n")
                shoot(player, shotgun)
                current_turn = "player"
            
            if not player.is_alive() or not enemy.is_alive():
                break
            
            os.system('cls')

    # --- Determining who won ---
    if player.is_alive():
        print("You won")
    else:
        print("You suck. Try again next life")