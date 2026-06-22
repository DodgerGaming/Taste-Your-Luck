import pygame

from UI.Screens.Screen import Screen


class EndScreen(Screen):

    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(None, 80)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                from UI.Screens.Menu_Screen import MenuScreen
                self.next_screen = MenuScreen()

    def draw(self, screen):

        screen.fill((20, 20, 20))

        text = self.font.render(
            "END - PRESS ESC",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (250, 300))