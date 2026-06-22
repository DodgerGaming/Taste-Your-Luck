import pygame

from UI.Screens.Menu_Screen import MenuScreen

pygame.init()

# Window Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Taste Your Luck")

clock = pygame.time.Clock()

# Starting Screen
current_screen = MenuScreen()

running = True

while running:

    dt = clock.tick(60) / 1000

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        current_screen.handle_event(event)

    # Update Current Screen
    current_screen.update(dt)

    # Screen Switching
    next_screen = current_screen.get_next_screen()

    if next_screen is not None:
        current_screen = next_screen

    # Draw Current Screen
    current_screen.draw(screen)

    pygame.display.flip()

pygame.quit()