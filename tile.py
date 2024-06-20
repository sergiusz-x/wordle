import pygame
from settings import WHITE, BLACK

class Tile:
    def __init__(self, letter, x, y, size):
        self.letter = letter
        self.rect = pygame.Rect(x, y, size, size)
        self.color = WHITE
        self.text_color = BLACK

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.letter, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
