import pygame


class GameScreen:

    def __init__(self):

        self.font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 55)

        # Buttons
        self.shoot_self_button = pygame.Rect(
            420, 500, 180, 60
        )

        self.shoot_enemy_button = pygame.Rect(
            680, 500, 180, 60
        )

    def draw(self, surface):

        surface.fill((20, 20, 20))

        # =====================
        # PLAYER HP
        # =====================

        player_text = self.font.render(
            "PLAYER ♥♥♥♥",
            True,
            (255, 255, 255)
        )

        surface.blit(player_text, (50, 40))

        # =====================
        # ENEMY HP
        # =====================

        enemy_text = self.font.render(
            "ENEMY ♥♥♥♥",
            True,
            (255, 255, 255)
        )

        surface.blit(enemy_text, (950, 40))

        # =====================
        # TURN INDICATOR
        # =====================

        turn_text = self.title_font.render(
            "PLAYER TURN",
            True,
            (255, 220, 220)
        )

        surface.blit(turn_text, (500, 40))

        # =====================
        # PLAYER PLACEHOLDER
        # =====================

        pygame.draw.circle(
            surface,
            (80, 80, 80),
            (250, 280),
            80
        )

        p_text = self.title_font.render(
            "P",
            True,
            (255, 255, 255)
        )

        surface.blit(p_text, (235, 260))

        # =====================
        # ENEMY PLACEHOLDER
        # =====================

        pygame.draw.circle(
            surface,
            (80, 80, 80),
            (1030, 280),
            80
        )

        e_text = self.title_font.render(
            "E",
            True,
            (255, 255, 255)
        )

        surface.blit(e_text, (1015, 260))

        # =====================
        # SHOTGUN PLACEHOLDER
        # =====================

        pygame.draw.rect(
            surface,
            (140, 140, 140),
            (490, 250, 300, 40)
        )

        shotgun_text = self.font.render(
            "SHOTGUN",
            True,
            (0, 0, 0)
        )

        surface.blit(shotgun_text, (575, 255))

        # =====================
        # SHOOT SELF BUTTON
        # =====================

        pygame.draw.rect(
            surface,
            (60, 60, 60),
            self.shoot_self_button
        )

        self_text = self.font.render(
            "Shoot Self",
            True,
            (255, 255, 255)
        )

        surface.blit(self_text, (445, 517))

        # =====================
        # SHOOT ENEMY BUTTON
        # =====================

        pygame.draw.rect(
            surface,
            (60, 60, 60),
            self.shoot_enemy_button
        )

        enemy_button_text = self.font.render(
            "Shoot Enemy",
            True,
            (255, 255, 255)
        )

        surface.blit(enemy_button_text, (695, 517))

        # =====================
        # DIALOGUE BOX
        # =====================

        pygame.draw.rect(
            surface,
            (30, 30, 30),
            (50, 600, 1180, 100)
        )

        pygame.draw.rect(
            surface,
            (200, 200, 200),
            (50, 600, 1180, 100),
            2
        )

        dialogue = self.font.render(
            "Welcome to Taste Your Luck.",
            True,
            (255, 255, 255)
        )

        surface.blit(dialogue, (80, 635))