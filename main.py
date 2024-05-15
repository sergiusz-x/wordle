import pygame

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()



#pętla gry
window_open = True
while window_open:
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        if event.type == pygame.QUIT:
            window_open = False


    # aktualizacja okna gry
    pygame.display.flip()

    clock.tick(60)


pygame.quit()