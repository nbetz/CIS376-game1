import game_object
import pygame


class Scene:
    game_objects: list
    identifier: str

    def __init__(self, engine):
        self.engine = engine
        self.screen = engine._screen
        self.tile_size = engine._tile_size
        self.height = engine._screen_height
        self.width = engine._screen_width
        self.game_objects = []

    def initial_grid(self):
        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                rectangle = game_object.Rectangle(False, x, y)
                self.game_objects.append(rectangle)
                self.draw()
        pass

    def input(self):

        pass

    def update(self):
        pass

    def draw(self):
        for item in self.game_objects:
            color = item.color
            rect = pygame.Rect(item.x, item.y, self.tile_size-1, self.tile_size-1)
            pygame.draw.rect(self.screen, color, rect)
        pass

    #def update_all_objects(self):
        # calls update() method for all updatable game objects in scene
        #[game_obj.update() for game_obj in self.game_objects if isinstance(game_obj, game_object.Updatable)]

    #def draw_all_objects(self):
        # calls draw() method for all drawable game objects in scene
        #[game_obj.draw() for game_obj in self.game_objects if isinstance(game_obj, game_object.Drawable)]

