import pygame


# Logan Reneau, initial gameloop and display
# Noah converted Engine to a class
class Engine:
    _running: bool
    _fps: int
    _tile_size: int
    _screen_width: int
    _screen_height: int
    _screen: pygame.Surface

    def __init__(self, game_fps, tile_size, screen_width, screen_height):
        pygame.init()
        self._running = False
        self._fps = game_fps
        self._tile_size = tile_size
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = pygame.display.set_mode((screen_width, screen_height))

    def loop(self):
        self._running = True
        clock = pygame.time.Clock()

        while self._running:
            self._screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # draws the lines that make the grids
            [pygame.draw.line(self._screen, pygame.Color('gray'), (x, 0), (x, self._screen_height))
             for x in range(0, self._screen_width, self._tile_size)]
            [pygame.draw.line(self._screen, pygame.Color('gray'), (0, y), (self._screen_width, y))
             for y in range(0, self._screen_height, self._tile_size)]

            pygame.display.flip()
            clock.tick(self._fps)
