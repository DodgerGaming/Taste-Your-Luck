from UI.Main_Menu import MainMenu
from UI.Game_Screen import GameScreen

import pygame

pygame.init()

window_width = 1000
window_height = 500

window = pygame.display.set_mode(
    (window_width, window_height)
)

pygame.display.set_caption("Taste Your Luck")

clock = pygame.time.Clock()

# Create screens
main_menu = MainMenu()
game_screen = GameScreen()

# Current screen
current_screen = "menu"

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "menu":

                if main_menu.start_button.collidepoint(event.pos):
                    current_screen = "game"

                if main_menu.quit_button.collidepoint(event.pos):
                    running = False

    # Draw current screen
    if current_screen == "menu":
        main_menu.draw(window)

    elif current_screen == "game":
        game_screen.draw(window)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()