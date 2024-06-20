from settings import *
import random
from tile import Tile

class WordleBoard:
    def __init__(self, words, x, y):
        self.words = words
        self.target_word = self.choose_word()
        self.tiles = [[Tile(x + (TILE_SIZE + TILE_MARGIN) * col, y + (TILE_SIZE + TILE_MARGIN) * row) for col in range(5)] for row in range(6)]
        self.current_row = 0
        self.current_col = 0
        print(f"Target word: {self.target_word}")

    def choose_word(self):
        return random.choice(self.words).upper()

    def enter_letter(self, letter):
        if self.current_col < 5:
            self.tiles[self.current_row][self.current_col].letter = letter
            self.current_col += 1

    def delete_letter(self):
        if self.current_col > 0:
            self.current_col -= 1
            self.tiles[self.current_row][self.current_col].letter = ""

    def submit_guess(self):
        if self.current_col < 5:
            return
        guess = "".join([tile.letter for tile in self.tiles[self.current_row]])
        if guess == self.target_word:
            for tile in self.tiles[self.current_row]:
                tile.color = GREEN
            return "win"
        else:
            for col, letter in enumerate(guess):
                if letter == self.target_word[col]:
                    self.tiles[self.current_row][col].color = GREEN
                elif letter in self.target_word:
                    self.tiles[self.current_row][col].color = YELLOW
                else:
                    self.tiles[self.current_row][col].color = RED
            self.current_row += 1
            self.current_col = 0
            if self.current_row == 6:
                return "lose"
        return None

    def get_current_guess(self):
        if self.current_col < 5:
            return None
        return "".join([tile.letter for tile in self.tiles[self.current_row]])

    def draw(self, screen, font):
        for row in self.tiles:
            for tile in row:
                tile.draw(screen, font)