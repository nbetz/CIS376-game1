import pygame
import scene


# Logan Reneau, initial gameloop and display
# Noah converted Engine to a class
class Engine:
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

    #Noah created game loop
    def loop(self):
        self._running = True
        scene1 = scene.Scene(self)
        scene1.initial_grid()

        while self._running:
            # TODO move event actions to dictionary & probably move to either custom scene or gameobjects
            #INPUT

            #UPDATE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                #Logan Reneau click recognition
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for gameObject in scene1.game_objects:
                            if gameObject.collidepoint(event.pos):
                                if gameObject.isAlive:
                                    gameObject.color = (0, 0, 0)
                                    gameObject.isAlive = False
                                else:
                                    gameObject.color = (21, 71, 52)
                                    gameObject.isAlive = True

            scene1.input()
            scene1.update()
            #DISPLAY
            #Logan Reneau, made a display loop that loops through drawn rectangles
            self._screen.fill(pygame.Color('dimgrey'))
            scene1.draw()
            pygame.display.flip()
            self.delta_time = self.clock.tick(self._fps)
