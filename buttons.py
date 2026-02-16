import pygame


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.hover_color = (125, 0, 0)
        self.main_color = (255, 0, 0)
        self.color = self.main_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 25)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def update_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.main_color
