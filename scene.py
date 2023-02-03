import game_object
import pygame
import random
import engine


class Scene:

    def __init__(self, tile_size):
        updatable = pygame.sprite.Group()
        self.game_objects = []
        self.groups = {"updatable": updatable}
        self.previous_game_objects = []
        self.rand = random.Random
        self.user_object: game_object.GameObject
        self.tile_size = tile_size

    def update_all_objects(self):
        # calls update() method for all updatable game objects in scene
        [game_obj.update() for game_obj in self.game_objects if isinstance(game_obj, game_object.GameObject)]


class MazeScene(Scene):
    def __init__(self, tile_size):
        Scene.__init__(self, tile_size)
        walls = pygame.sprite.Group()
        paths = pygame.sprite.Group()
        player = pygame.sprite.Group()
        rectangles = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        self.groups.update({"walls": walls, "paths": paths, "player": player, "rectangles": rectangles,
                            "all_sprites": all_sprites})

    # Logan Reneau
    def initial_grid(self):
        for y in range(0, engine.Engine.screen_height, self.tile_size):
            for x in range(0, engine.Engine.screen_width, self.tile_size):
                temp = random.randint(0, 1)
                if x == 0 and y == 0:
                    wall = False
                elif temp == 1:
                    wall = True
                else:
                    wall = False
                rectangle = game_object.Rectangle(wall, x, y, self)
                self.game_objects.append(rectangle)

    # Noah Betz
    def draw(self):
        self.groups.get("rectangles").draw(engine.Engine.screen)
        self.groups.get("player").draw(engine.Engine.screen)
