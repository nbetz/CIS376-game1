import pygame
import scene


# Logan Reneau, initial gameloop and display
# Noah converted Engine to a class
class Engine:
    # technically the private vars don't need to be static, but makes it more readable
    _running: bool
    _fps: int
    _tile_size: int
    _screen_width: int
    _screen_height: int
    _screen: pygame.Surface
    _scene_list: list
    _active_scene: scene
    clock: pygame.time.Clock
    delta_time: int
    event_queue: list

    def __init__(self, game_fps, tile_size, screen_width, screen_height):
        pygame.init()
        self._running = False
        self._fps = game_fps
        self._tile_size = tile_size
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.event_queue = pygame.event.get()
        self._scene_list = []

    def loop(self):
        self._running = True

        while self._running:
            self._screen.fill(pygame.Color('black'))

            # TODO move event actions to dictionary & probably move to either custom scene or gameobjects
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # TODO grab active scene if non-null & call update_all and draw_all on scene

            # TODO move to draw_all function of a custom scene object
            # draws the lines that make the grids
            [pygame.draw.line(self._screen, pygame.Color('gray'), (x, 0), (x, self._screen_height))
             for x in range(0, self._screen_width, self._tile_size)]
            [pygame.draw.line(self._screen, pygame.Color('gray'), (0, y), (self._screen_width, y))
             for y in range(0, self._screen_height, self._tile_size)]

            pygame.display.flip()
            self.delta_time = self.clock.tick(self._fps)

    # TODO
    def add_scene(self):
        pass

    # TODO
    def set_active_scene(self):
        pass

