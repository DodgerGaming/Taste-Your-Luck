import pygame
from Entities.Actor import Actor
from Entities.Shotgun import Shotgun
from System.Level import play_level
from System.Level import next_level


player = Actor()
enemy = Actor()
shotgun = Shotgun()

current_level = 1
win_count = 0

while current_level <= 3:
    winner = play_level(player, enemy, shotgun, current_level)

    if winner == "player":
        current_level = next_level(player, enemy, current_level)
        win_count += 1
    else:
        break

if win_count == 3:
    print("Congratulations, you've won the game!")
else:
    print("You've lost, try again next life.")
print(f"===GAME STATUS ===\nLevels won: {win_count}\nTo be implemented...")


"""
pygame.init()

windowWidth = 1000
windowHeight = 500

window = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption("Taste Your Luck")

clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shell = shotgun.shoot()
                print(shell)
    
    window.fill((0, 0, 0)) # turn the background screen black


    pygame.draw.rect(window, (150, 75, 0), (425, 150, 150, 25)) # shotgun imitation
    pygame.draw.circle(window, (0, 0, 255), (250, 150), 60)
    pygame.draw.circle(window, (255, 0, 0), (750, 150), 60)
    
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

"""

