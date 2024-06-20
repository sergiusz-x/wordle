import os

# Rozdzielczość ekranu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (163, 170, 190)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (37, 150, 190)

# Ścieżki do zasobów
BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
WORDLIST_EN = os.path.join(ASSETS_PATH, "words_en.csv")
WORDLIST_PL = os.path.join(ASSETS_PATH, "words_pl.csv")

# Ustawienia gry
FPS = 30
FONT_SIZE = 24
TILE_SIZE = 50
WIDE_TILE_SIZE = 150
TILE_MARGIN = 5
BUTTON_WIDTH = 230
BUTTON_HEIGHT = 50
BUTTON_RADIUS = 25

# Animowane tło
BACKGROUND_ANIM_SPEED = 1

# Klawiatury
KEYBOARD_LAYOUT_EN = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

KEYBOARD_LAYOUT_PL = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM",
    "ĄĆĘŁŃÓŚŹŻ"
]

