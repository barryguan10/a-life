import pygame


class Button:
    """Class for Buttons that are clickable"""
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
        """Draws Button

        Args:
            param1: pygame screen to draw the button on

        Returns:
            None, draws button to screen
        """
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def update_text(self, text):
        """Update Button text

        Args:
            param1: text (string), represents the new text for the button

        Returns:
            None
        """
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update_hover(self, mouse_pos):
        """Changes the button color if mouse is positioned on button

        Args:
            param1: mouse_pos (tuple) - x, y coordinates of the mouse

        Returns:
            None
        """
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.main_color

    def is_button_clicked(self, event):
        """Return True if Button is clicked, false otherwise

        Args:
            param1: event (pygame event)

        Returns:
            True if Button is clicked, False Otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
