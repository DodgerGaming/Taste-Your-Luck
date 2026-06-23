import pygame

from UI.Screens.Screen import Screen
from UI.Elements.Button import Button

from assets import get_font
from assets import MAIN_BG


class MenuScreen(Screen):

    def __init__(self):
        super().__init__()

        # Background
        self.background = pygame.image.load(MAIN_BG).convert()
        self.background = pygame.transform.scale(
            self.background,
            (1280, 680)
        )

        # Fonts
        self.title_font = get_font(45)
        self.button_font = get_font(30)

        # Colors
        self.title_color = (220, 185, 130)

        self.button_color = (40, 20, 18)
        self.button_hover = (85, 40, 30)
        self.button_text = (225, 200, 165)

        # Buttons
        self.start_button = Button(
            490,
            340,
            300,
            70,
            "START GAME",
            self.button_font,
            bg_color=self.button_color,
            hover_color=self.button_hover,
            text_color=self.button_text
        )

        self.quit_button = Button(
            490,
            440,
            300,
            70,
            "QUIT",
            self.button_font,
            bg_color=self.button_color,
            hover_color=self.button_hover,
            text_color=self.button_text
        )

    def handle_event(self, event):

        if self.start_button.handle_event(event):

            from UI.Screens.Game_Screen import GameScreen

            self.next_screen = GameScreen()

        if self.quit_button.handle_event(event):

            pygame.quit()
            raise SystemExit

    def update(self, dt):
        pass

    def draw(self, screen):

        # Background
        screen.blit(self.background, (0, 0))

        # Title
        title = self.title_font.render(
            "TASTE YOUR LUCK",
            True,
            self.title_color
        )

        title_rect = title.get_rect(
            center=(640, 180)
        )

        screen.blit(title, title_rect)

        # Buttons
        self.start_button.draw(screen)
        self.quit_button.draw(screen)