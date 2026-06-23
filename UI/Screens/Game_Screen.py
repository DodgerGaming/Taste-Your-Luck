import pygame

from UI.Screens.Screen import Screen
from System.Game import Game
from System.TurnManager import TurnManager
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

        # Game Data
        self.game = Game()
        self.turn_manager = TurnManager(self.game)
        self.dialogue_text = "What will you do?"
        self.pending_messages = []
        self.message_timer = 0
        self.game_over = None

        # Snapshots — what draw() reads
        self.display_player_hp = self.game.player.currentHp
        self.display_enemy_hp  = self.game.enemy.currentHp
        self.display_turn      = "PLAYER TURN"

        # Initial reload
        reload_messages = self.turn_manager.reload()
        self._queue_messages(reload_messages, None)

        # Background
        self.background = pygame.image.load(MAIN_BG).convert()
        self.background = pygame.transform.scale(self.background, (1280, 630))

        # Sprites
        self.player = pygame.image.load(PLAYER).convert_alpha()
        self.enemy  = pygame.image.load(ENEMY).convert_alpha()
        self.shotgun = pygame.image.load(SHOTGUN).convert_alpha()

        self.player  = pygame.transform.scale(self.player,  (300, 300))
        self.enemy   = pygame.transform.scale(self.enemy,   (300, 300))
        self.shotgun = pygame.transform.scale(self.shotgun, (250, 120))

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

    # ------------------------------------------------------------------

    def handle_event(self, event):

        shoot_self_clicked  = self.shoot_self_button.handle_event(event)
        shoot_enemy_clicked = self.shoot_enemy_button.handle_event(event)

        if self.turn_manager.current_turn != "player":
            return

        if self.pending_messages:
            return

        if shoot_self_clicked:
            messages, game_over = self.turn_manager.player_shoot_self()
            self._queue_messages(messages, game_over)

        if shoot_enemy_clicked:
            messages, game_over = self.turn_manager.player_shoot_enemy()
            self._queue_messages(messages, game_over)

    def _queue_messages(self, messages, game_over):
        self.pending_messages = list(messages)
        self.game_over = game_over
        self._show_next_message()

    def _show_next_message(self):
        if self.pending_messages:
            msg = self.pending_messages.pop(0)

            # msg is a dict with text + state snapshot
            self.dialogue_text     = msg["text"]
            self.display_player_hp = msg["player_hp"]
            self.display_enemy_hp  = msg["enemy_hp"]
            self.display_turn      = "PLAYER TURN" if msg["turn"] == "player" else "ENEMY TURN"

            self.message_timer = 1.5
        else:
            if self.game_over:
                from UI.Screens.End_Screen import EndScreen
                self.next_screen = EndScreen(self.game_over)

    def update(self, dt):
        if self.pending_messages:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self._show_next_message()
        elif self.game_over:
            self.message_timer -= dt
            if self.message_timer <= 0:
                from UI.Screens.End_Screen import EndScreen
                self.next_screen = EndScreen(self.game_over)

    # ------------------------------------------------------------------

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        # Turn Banner
        turn_text = self.turn_font.render(self.display_turn, True, (220, 185, 130))
        turn_rect = turn_text.get_rect(center=(640, 40))
        screen.blit(turn_text, turn_rect)

        # HP
        player_hp_text = self.hp_font.render(f"HP: {self.display_player_hp}", True, (255, 255, 255))
        enemy_hp_text  = self.hp_font.render(f"HP: {self.display_enemy_hp}",  True, (255, 255, 255))
        screen.blit(player_hp_text, (50, 50))
        screen.blit(enemy_hp_text,  (1050, 50))

        # Labels
        screen.blit(self.label_font.render("PLAYER",  True, (255, 255, 255)), (180, 230))
        screen.blit(self.label_font.render("SHOTGUN", True, (255, 255, 255)), (560, 290))
        screen.blit(self.label_font.render("ENEMY",   True, (255, 255, 255)), (980, 190))

        # Sprites
        screen.blit(self.player,  (120, 260))
        screen.blit(self.enemy,   (860, 220))
        screen.blit(self.shotgun, (515, 310))

        # Buttons
        self.shoot_self_button.draw(screen)
        self.shoot_enemy_button.draw(screen)

        # Dialogue Box
        dialogue_rect = pygame.Rect(40, 555, 1200, 60)
        pygame.draw.rect(screen, (25, 15, 15),   dialogue_rect, border_radius=8)
        pygame.draw.rect(screen, (140, 90, 60),  dialogue_rect, width=2, border_radius=8)

        dialogue_surface = self.dialogue_font.render(self.dialogue_text, True, (225, 200, 165))
        screen.blit(dialogue_surface, (60, 572))