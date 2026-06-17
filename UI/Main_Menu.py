import pygame


class MainMenu:

    def __init__(self):

        self.title_font = pygame.font.SysFont(None, 80)
        self.button_font = pygame.font.SysFont(None, 50)

        self.start_button = pygame.Rect(
            490, 250, 300, 80
        )

        self.quit_button = pygame.Rect(
            490, 370, 300, 80
        )

    def draw(self, surface):

        surface.fill((15, 15, 15))

        title = self.title_font.render(
            "TASTE YOUR LUCK",
            True,
            (180, 40, 40)
        )

        surface.blit(title, (300, 100))

        pygame.draw.rect(
            surface,
            (40, 40, 40),
            self.start_button
        )

        pygame.draw.rect(
            surface,
            (40, 40, 40),
            self.quit_button
        )

        start_text = self.button_font.render(
            "START GAME",
            True,
            (255, 255, 255)
        )

        quit_text = self.button_font.render(
            "QUIT",
            True,
            (255, 255, 255)
        )

        surface.blit(start_text, (530, 275))
        surface.blit(quit_text, (590, 395))