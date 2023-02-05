import pygame
import scene


# Logan Reneau, initial gameloop and display
# Noah converted Engine to a class
class Engine:
    _running: bool
    _fps: int
    _active_scene: scene.Scene
    screen_width: int
    screen_height: int
    clock: pygame.time.Clock
    delta_time: int
    event_queue: list
    scene_list: list = []
    screen: pygame.Surface

    def __init__(self, game_fps, screen_width, screen_height):
        pygame.init()
        Engine._running = False
        Engine._fps = game_fps
        Engine.screen_width = screen_width
        Engine.screen_height = screen_height
        Engine.screen = pygame.display.set_mode((screen_width, screen_height))
        Engine.clock = pygame.time.Clock()
        Engine.delta_time = 0
        Engine.event_queue = pygame.event.get()

    # Noah created game loop
    def loop(self):
        self._running = True
        pygame.key.set_repeat(500)
        while self._running:
            # INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                # Logan Reneau click recognition
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._active_scene.update_all_objects(type="click", position=event.pos)
                elif event.type == pygame.KEYDOWN:
                    self._active_scene.update_all_objects(type="keydown", key=event.key)

            # Update
            # check win condition
            if self._active_scene.check_win():
                self._running = False
            else:
                # update objects if win condition isnt met
                self._active_scene.update_all_objects(type="main")
            # DISPLAY
            # Logan Reneau, made a display loop that loops through drawn rectangles
            self.screen.fill(pygame.Color('dimgrey'))
            self._active_scene.draw()
            pygame.display.flip()
            self.delta_time = self.clock.tick(self._fps)

    def add_scene(self, game_scene):
        self.scene_list.append(game_scene)

    def set_active_scene(self, game_scene):
        self._active_scene = game_scene
        self.screen.fill(pygame.Color('dimgrey'))
        game_scene.initial_grid(True)
        game_scene.draw()
        pygame.display.flip()
