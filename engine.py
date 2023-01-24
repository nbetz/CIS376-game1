import pygame

#Logan Reneau, initial gameloop and display
fps = 10
pygame.init()
tile = 30
size = width, height = 720, 480
display = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:
    display.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #draws the lines that make the grids
    [pygame.draw.line(display,pygame.Color('gray'), (x, 0), (x, height))
     for x in range (0, width, tile)]
    [pygame.draw.line(display, pygame.Color('gray'), (0, y), (width, y))
     for y in range(0, height, tile)]

    pygame.display.flip()
    clock.tick(fps)
