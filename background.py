from settings import *

class Background:
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.direction_x = 1
        self.direction_y = 1
    
    def update(self):
        if self.x + SCREEN_WIDTH >= self.rect.width or self.x < 0:
            self.direction_x *= -1
        if self.y + SCREEN_HEIGHT >= self.rect.height or self.y < 0:
            self.direction_y *= -1

        self.x += self.direction_x * BACKGROUND_ANIM_SPEED
        self.y += self.direction_y * BACKGROUND_ANIM_SPEED
    
    def draw(self):
        self.update()
        self.screen.blit(self.image, (-self.x, -self.y))