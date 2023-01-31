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
    rectList: list

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

        #self.rectList = []  #this will eventually be moved to scene as the game object list
    #Noah created game loop
    def loop(self):
        self._running = True
        scene1 = scene.Scene(self)
        scene1.initial_grid()
        self._scene_list.append(scene1)

        while self._running:
            # TODO move event actions to dictionary & probably move to either custom scene or gameobjects
            #INPUT

            #UPDATE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                #Logan Reneau click recognition
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for currentRect in scene1.game_objects:
                            rect = pygame.Rect(currentRect.x, currentRect.y, self._tile_size-1, self._tile_size-1)
                            if rect.collidepoint(event.pos):
                                if currentRect.isAlive:
                                    currentRect.color = (0, 0, 0)
                                    currentRect.isAlive = False
                                else:
                                    currentRect.color = (255, 0, 0)
                                    currentRect.isAlive = True

            scene1.input()
            scene1.update()
            #DISPLAY
            #Logan Reneau, made a display loop that loops through drawn rectangles
            self._screen.fill(pygame.Color('grey'))
            scene1.draw()
            pygame.display.flip()
            self.delta_time = self.clock.tick(self._fps)

    # TODO
    def add_scene(self):
        pass

    # TODO
    def set_active_scene(self):
        pass

