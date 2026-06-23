import pygame

from UI.Screens.Screen import Screen
from UI.Elements.Button import Button
from assets import get_font

from assets import (
    MAIN_BG,
    PLAYER,
    ENEMY,
    SHOTGUN
)


class GameScreen(Screen):

    def __init__(self):
        super().__init__()

        # Fonts
        self.hp_font = get_font(20)
        self.label_font = get_font(16)
        self.turn_font = get_font(20)
        self.dialogue_font = get_font(14)
        self.button_font = get_font(16)

        # Temporary Game Data (still placeholder — real wiring is next step)
        self.player_hp = 4
        self.enemy_hp = 4

        self.current_turn = "PLAYER TURN"

        self.dialogue_text = (
            "Welcome to Taste Your Luck."
        )

        # Background
        self.background = pygame.image.load(
            MAIN_BG
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (1280, 630)
        )

        # Sprites
        self.player = pygame.image.load(
            PLAYER
        ).convert_alpha()

        self.enemy = pygame.image.load(
            ENEMY
        ).convert_alpha()

        self.shotgun = pygame.image.load(
            SHOTGUN
        ).convert_alpha()

        # Scale Sprites
        self.player = pygame.transform.scale(
            self.player,
            (300, 300)
        )

        self.enemy = pygame.transform.scale(
            self.enemy,
            (300, 300)
        )

        self.shotgun = pygame.transform.scale(
            self.shotgun,
            (250, 120)
        )

        # Buttons
        self.shoot_self_button = Button(
            120, 490, 300, 55,
            "SHOOT SELF",
            self.button_font,
            bg_color=(40, 20, 18),
            hover_color=(85, 40, 30),
            text_color=(225, 200, 165)
        )

        self.shoot_enemy_button = Button(
            860, 490, 300, 55,
            "SHOOT ENEMY",
            self.button_font,
            bg_color=(40, 20, 18),
            hover_color=(85, 40, 30),
            text_color=(225, 200, 165)
        )

    def handle_event(self, event):

        # Just hover/click detection for now — wiring these into the
        # actual game logic is the next step.
        self.shoot_self_button.handle_event(event)
        self.shoot_enemy_button.handle_event(event)

        if event.type == pygame.KEYDOWN:

            # Temporary test key
            if event.key == pygame.K_RETURN:

                from UI.Screens.End_Screen import EndScreen

                self.next_screen = EndScreen()

    def update(self, dt):
        pass

    def draw(self, screen):

        # Background
        screen.blit(self.background, (0, 0))

        # Turn Banner
        turn_text = self.turn_font.render(
            self.current_turn,
            True,
            (220, 185, 130)
        )

        turn_rect = turn_text.get_rect(
            center=(640, 40)
        )

        screen.blit(turn_text, turn_rect)

        # HP
        player_hp_text = self.hp_font.render(
            f"HP: {self.player_hp}",
            True,
            (255, 255, 255)
        )

        enemy_hp_text = self.hp_font.render(
            f"HP: {self.enemy_hp}",
            True,
            (255, 255, 255)
        )

        screen.blit(player_hp_text, (50, 50))
        screen.blit(enemy_hp_text, (1050, 50))

        # Labels — moved above the sprites (the dialogue box used to
        # paint over them when they sat at y=580)
        player_text = self.label_font.render(
            "PLAYER",
            True,
            (255, 255, 255)
        )

        enemy_text = self.label_font.render(
            "ENEMY",
            True,
            (255, 255, 255)
        )

        shotgun_text = self.label_font.render(
            "SHOTGUN",
            True,
            (255, 255, 255)
        )

        screen.blit(player_text, (180, 230))
        screen.blit(shotgun_text, (560, 290))
        screen.blit(enemy_text, (980, 190))

        # Sprites
        screen.blit(
            self.player,
            (120, 260)
        )

        screen.blit(
            self.enemy,
            (860, 220)
        )

        screen.blit(
            self.shotgun,
            (515, 310)
        )

        # Buttons
        self.shoot_self_button.draw(screen)
        self.shoot_enemy_button.draw(screen)

        # Dialogue Box — moved down slightly to make room for the buttons
        dialogue_rect = pygame.Rect(
            40,
            555,
            1200,
            60
        )

        pygame.draw.rect(
            screen,
            (25, 15, 15),
            dialogue_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (140, 90, 60),
            dialogue_rect,
            width=2,
            border_radius=8
        )

        dialogue_surface = self.dialogue_font.render(
            self.dialogue_text,
            True,
            (225, 200, 165)
        )

        screen.blit(
            dialogue_surface,
            (60, 572)
        )