import pygame
from settings import *

class Keyboard:
    def __init__(self, layout, x, y):
        self.layout = layout
        self.x = x
        self.y = y
        self.keys = []
        self.create_keys()

    def create_keys(self):
        self.keys = []
        for row_index, row in enumerate(self.layout):
            row_width = len(row) * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN
            start_x = (SCREEN_WIDTH - row_width) // 2
            for col_index, letter in enumerate(row):
                key_x = start_x + col_index * (TILE_SIZE + TILE_MARGIN)
                key_y = self.y + row_index * (TILE_SIZE + TILE_MARGIN)
                self.keys.append(Key(letter, key_x, key_y, TILE_SIZE))
        self.keys.append(BackspaceKey(self.y, len(self.layout)))
        self.keys.append(EnterKey(self.y, len(self.layout)))

    def draw(self, screen, font):
        for key in self.keys:
            key.draw(screen, font)

    def get_key(self, pos):
        for key in self.keys:
            if key.is_clicked(pos):
                return key.letter
        return None
    
    def get_green_keys(self):
        green_letters = []
        for key in self.keys:
            if key.color == GREEN:
                green_letters.append(key.letter)
        return green_letters

    def update_colors(self, letter, color):
        for key in self.keys:
            if key.letter == letter:
                if letter in self.get_green_keys():
                    color = GREEN
                key.color = color

class Key:
    def __init__(self, letter, x, y, width):
        self.letter = letter
        self.rect = pygame.Rect(x, y, width, TILE_SIZE)
        self.color = WHITE

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        text_surface = font.render(self.letter, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class BackspaceKey(Key):
    def __init__(self, y_offset, num_rows):
        x = SCREEN_WIDTH // 2 - WIDE_TILE_SIZE - TILE_MARGIN
        y = y_offset + num_rows * (TILE_SIZE + TILE_MARGIN)
        super().__init__("BACKSPACE", x, y, WIDE_TILE_SIZE)

class EnterKey(Key):
    def __init__(self, y_offset, num_rows):
        x = SCREEN_WIDTH // 2 + TILE_MARGIN // 2
        y = y_offset + num_rows * (TILE_SIZE + TILE_MARGIN)
        super().__init__("ENTER", x, y, WIDE_TILE_SIZE)
