import game_object
import pygame
import random
import engine


class Scene:

    def __init__(self, tile_size):
        all_sprites = pygame.sprite.Group()
        self.game_objects = []
        self.groups = {"all_sprites": all_sprites}
        self.previous_game_objects = []
        self.rand = random.Random
        self.user_object: game_object.GameObject
        self.tile_size = tile_size

    def update_all_objects(self, *args, **kwargs):
        # calls update() method for all updatable game objects in scene
        all_sprites = self.groups.get("all_sprites")
        all_sprites.update(*args, **kwargs)

    def draw(self):
        pass

    def check_win(self):
        return False

    def initial_grid(self, **kwargs):
        pass


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

    def initial_grid(self, **kwargs):
        has_walls = True
        if kwargs.get("has_walls") is not None:
            has_walls = kwargs.get("has_walls")
        if has_walls:
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

        else:
            for y in range(0, engine.Engine.screen_height, self.tile_size):
                for x in range(0, engine.Engine.screen_width, self.tile_size):
                    wall = False
                    rectangle = game_object.Rectangle(wall, x, y, self)
                    self.game_objects.append(rectangle)

        # Create player object
        player_obj = game_object.PlayerCircle(self)
        player_obj.add(self.groups.get("all_sprites"))
        player_obj.add(self.groups.get("player"))

    def check_win(self):
        # odd way to get it but the only way
        for players in self.groups.get("player"):
            player = players

        if player.x + player.centerX == engine.Engine.screen_width - player.centerX \
                and player.y + player.centerY == engine.Engine.screen_height - player.centerY:
            print("Congrats! You have won!")
            return True
        return False

    def draw(self):
        self.groups.get("rectangles").draw(engine.Engine.screen)
        self.groups.get("player").draw(engine.Engine.screen)
