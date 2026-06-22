import pygame

from UI.Screens.Screen import Screen
from UI.Elements.Button import Button

class MenuScreen(Screen):

    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(None, 80)
        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 50)

        self.start_button = Button(
            490,
            300,
            300,
            70,
            "START GAME",
            self.button_font
        )

        self.quit_button = Button(
            490,
            400,
            300,
            70,
            "QUIT",
            self.button_font
        )
    def handle_event(self, event):

        if self.start_button.handle_event(event):

            from UI.Screens.Game_Screen import GameScreen

            self.next_screen = GameScreen()

        if self.quit_button.handle_event(event):

            pygame.quit()
            raise SystemExit

    def draw(self, screen):

        screen.fill((25, 10, 20))

        title = self.title_font.render(
            "TASTE YOUR LUCK",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(640, 180)
        )

        screen.blit(title, title_rect)

        self.start_button.draw(screen)
        self.quit_button.draw(screen)