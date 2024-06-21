import pygame
import csv
import os
from settings import *
from wordle_board import WordleBoard
from keyboard import Keyboard
from menu import Menu, Button
from background import Background
import requests

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wordle")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(os.path.join(ASSETS_PATH, "font.ttf"), FONT_SIZE)
        self.load_assets()
        pygame.display.set_icon(self.menu_logo)
        self.language = "pl"
        self.music_on = True
        self.state = "menu"
        self.menu = Menu(self)
        self.load_words()
        # self.keyboard = Keyboard()
        # self.board = WordleBoard()
        self.end_message = ""
        self.end_buttons = []
        self.background = Background(self.screen, self.background_image)
        self.escape_press_count = 0

    def load_assets(self):
        self.background_image = pygame.image.load(os.path.join(ASSETS_PATH, "background.png")).convert()
        self.correct_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "correct_sound.wav"))
        self.wrong_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "wrong_sound.wav"))
        pygame.mixer.music.load(os.path.join(ASSETS_PATH, "music.mp3"))
        pygame.mixer.music.play(-1)
        self.menu_logo = pygame.image.load(os.path.join(ASSETS_PATH, "menu_logo.png")).convert_alpha()
        self.game_logo = pygame.image.load(os.path.join(ASSETS_PATH, "game_logo.png")).convert_alpha()

    def load_words(self):
        path = WORDLIST_EN if self.language == "en" else WORDLIST_PL
        with open(path, encoding="utf-8") as csvfile:
            self.words = [row[0] for row in csv.reader(csvfile) if len(row[0]) == 5]

    def get_keyboard_layout(self):
        return KEYBOARD_LAYOUT_EN if self.language == "en" else KEYBOARD_LAYOUT_PL

    def get_keyboard_width(self):
        return max(len(row) for row in self.get_keyboard_layout()) * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN

    def new_game(self):
        self.load_words()
        self.keyboard = Keyboard(self.get_keyboard_layout(), (SCREEN_WIDTH - self.get_keyboard_width()) // 2, 700)
        self.board = WordleBoard(self.words, self.keyboard, (SCREEN_WIDTH - (5 * TILE_SIZE + 4 * TILE_MARGIN)) // 2, 150)
        self.end_message = ""
        self.end_buttons = []
        self.escape_press_count = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.escape_press_count += 1
                if self.escape_press_count >= 3:
                    self.return_to_menu()
                return
            elif self.state == "menu":
                self.menu.handle_event(event)
            elif self.state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        self.check_guess_validity()
                    elif event.key == pygame.K_BACKSPACE:
                        self.board.delete_letter()
                    else:
                        self.handle_text_input(event.unicode.upper())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    letter = self.keyboard.get_key(pos)
                    if letter:
                        if letter == "ENTER":
                            pygame.event.set_blocked(pygame.KEYDOWN)
                            self.check_guess_validity()
                        elif letter == "BACKSPACE":
                            self.board.delete_letter()
                        else:
                            self.board.enter_letter(letter)
                #
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.escape_press_count = 0
            elif self.state == "end":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in self.end_buttons:
                        if button.is_clicked(pos):
                            button.callback()

    def handle_text_input(self, char):
        if len(char) == 1 and char != " ":
            self.board.enter_letter(char)

    def check_guess_validity(self):
        guess = self.board.get_current_guess()
        if guess:
            if self.is_valid_word(guess):
                result = self.board.submit_guess()
                if result == "win":
                    self.end_message = f"Gratulacje! Poprawnie odgadnięte słowo {self.board.target_word}!"
                    self.add_end_buttons()
                    self.state = "end"
                    if self.music_on:
                        self.correct_sound.play()
                elif result == "lose":
                    self.end_message = f"Przegrana! Ukryte słowo to: {self.board.target_word}"
                    self.add_end_buttons()
                    self.state = "end"
                    if self.music_on:
                        self.wrong_sound.play()
                else:
                    self.update_keyboard_colors()
                    if self.music_on:
                        self.wrong_sound.play()
            else:
                self.show_invalid_word_message()
        pygame.event.set_allowed(pygame.KEYDOWN)


    def is_valid_word(self, word):
        if self.language == "en":
            url = f"https://www.dictionary.com/browse/{word.lower()}"
        else:
            url = f"https://sjp.pwn.pl/szukaj/{word.lower()}.html"
        
        try:
            response = requests.get(url)
            if self.language == "en":
                return "No results found" not in response.text
            else:
                return "Nie znaleziono żadnych wyników" not in response.text and "Czy chodziło Ci o" not in response.text
        except:
            return False

    def show_invalid_word_message(self):
        invalid_word_message = "Nie ma takiego słowa!"
        self.draw_text(invalid_word_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 0)
        pygame.display.flip()
        if self.music_on:
            self.wrong_sound.play()
        pygame.time.delay(1000)

    def add_end_buttons(self):
        self.end_buttons.append(Button("Powrót do menu", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, self.return_to_menu))

    def update_keyboard_colors(self):
        for row in self.board.tiles:
            for tile in row:
                if tile.color == GREEN:
                    self.keyboard.update_colors(tile.letter, GREEN)
                elif tile.color == YELLOW:
                    self.keyboard.update_colors(tile.letter, YELLOW)
                elif tile.color == RED:
                    self.keyboard.update_colors(tile.letter, RED)

    def draw(self):
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "game":
            self.background.draw()
            self.draw_logo(self.game_logo, (SCREEN_WIDTH // 2, 100))
            self.board.draw(self.screen, self.font)
            self.keyboard.draw(self.screen, self.font)
        elif self.state == "end":
            self.background.draw()
            self.draw_text(self.end_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
            for button in self.end_buttons:
                button.draw(self.screen, self.font)
        pygame.display.flip()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_logo(self, logo, position):
        rect = logo.get_rect(center=position)
        self.screen.blit(logo, rect)

    def return_to_menu(self):
        self.state = "menu"
        self.menu.update_buttons()

if __name__ == "__main__":
    game = Game()
    game.run()
