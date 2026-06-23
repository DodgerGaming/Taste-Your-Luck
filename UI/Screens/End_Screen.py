import pygame

from UI.Screens.Screen import Screen


class EndScreen(Screen):

    def __init__(self, result):
        super().__init__()

        self.result = result 
        self.font = pygame.font.Font(None, 80)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                from UI.Screens.Menu_Screen import MenuScreen
                self.next_screen = MenuScreen()

    def draw(self, screen):

        screen.fill((20, 20, 20))

        if self.result == "player_win":
            message = "YOU WIN!"
        else:
            message = "YOU LOSE."

        text = self.font.render(message, True, (255, 255, 255))
        subtext = self.font.render(
            "PRESS ESC TO RETURN",
            True,
            (160, 120, 80)
        )

        text_rect = text.get_rect(center=(640, 280))
        sub_rect = subtext.get_rect(center=(640, 370))

        screen.blit(text, text_rect)
        screen.blit(subtext, sub_rect)