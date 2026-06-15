from Logic.Combat import shoot
def play_round(player, enemy, shotgun):
    


    while player.is_alive() and enemy.is_alive():
        shotgun.reload()

        current_turn = "player"

        while len(shotgun.bullets) > 0:

            if current_turn == "player":
                shoot(enemy, shotgun)
                current_turn = "enemy"
                
            else:
                shoot(player, shotgun)
                current_turn = "player"
            
            if not player.is_alive() or not enemy.is_alive():
                break

    # --- Determining who win ---
    if player.is_alive():
        print("You won")
    else:
        print("You suck. Try again next life")