import pygame


class Button:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        bg_color=(60, 60, 60),
        hover_color=(100, 100, 100),
        text_color=(255, 255, 255)
    ):

        self.rect = pygame.Rect(x, y, width, height)

        self.text = text
        self.font = font

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.is_hovered = False

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True

        return False

    def draw(self, screen):

        color = self.hover_color if self.is_hovered else self.bg_color

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=8
        )

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        screen.blit(text_surface, text_rect)