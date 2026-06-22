import pygame

from UI.Screens.Screen import Screen
from UI.Screens.End_Screen import EndScreen


class GameScreen(Screen):

    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(None, 80)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                from UI.Screens.End_Screen import EndScreen
                self.next_screen = EndScreen()

    def draw(self, screen):

        screen.fill((0, 30, 20))

        text = self.font.render(
            "GAME - PRESS ENTER",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (250, 300))