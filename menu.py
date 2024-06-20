import pygame
from settings import *

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = LIGHT_GRAY

    def draw(self, screen, font):
        pygame.draw.rect(screen, BLACK, self.rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4), border_radius=BUTTON_RADIUS-2)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Menu:
    def __init__(self, game):
        self.game = game
        self.update_buttons()

    def update_buttons(self):
        self.buttons = [
            Button("Start", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, BUTTON_WIDTH, BUTTON_HEIGHT, self.start_game),
            Button(f"Muzyka: {"Tak" if self.game.music_on else "Nie"}", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, self.toggle_music),
            Button(f"Język: {self.game.language.upper()}", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 75, BUTTON_WIDTH, BUTTON_HEIGHT, self.change_language),
            Button("Wyjdź", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, BUTTON_WIDTH, BUTTON_HEIGHT, self.exit_game)
        ]

    def draw(self):
        self.game.background.draw()
        self.game.draw_logo(self.game.menu_logo, (SCREEN_WIDTH // 2, 150))
        for button in self.buttons:
            button.draw(self.game.screen, self.game.font)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(pos):
                    button.callback()

    def start_game(self):
        self.game.new_game()
        self.game.state = "game"

    def toggle_music(self):
        if self.game.music_on:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1)
        self.game.music_on = not self.game.music_on
        self.update_buttons()

    def change_language(self):
        if self.game.language == "en":
            self.game.language = "pl"
        else:
            self.game.language = "en"
        self.game.load_words()
        self.update_buttons()

    def exit_game(self):
        self.game.running = False
