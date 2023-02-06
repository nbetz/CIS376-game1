"""Game scene for managing gameobjects for a game engine.

Provides basic functions of a game scene for creating games.
Also contains MazeScene object for creating demo MazeGame.

Typical usage example:
  game_scene = scene.Scene()
  engine.add_scene(game_scene)
"""

import game_object
import pygame
import random
import engine


class Scene:
    """Scene class providing basic info for managing a set of GameObjects in a game scene

    Intended to be extended by other classes to provide a base for creating game objects.

    Attributes:
    game_objects: list of game objects in the scene.
    groups: dictionary storing all the sprite groups and their string names.
    rand: random number generator
    user_object: GameObject of the player
    tile_size: int representing how large of a square each sprite should be.
    """
    def __init__(self, tile_size: int):
        all_sprites = pygame.sprite.Group()
        self.game_objects = []
        self.groups = {"all_sprites": all_sprites}
        self.rand = random.Random
        self.user_object: game_object.GameObject
        self.tile_size = tile_size

    def update_all_objects(self, *args, **kwargs):
        """calls update() method for all updatable game objects in scene

            Args:
                *args: A tuple of arguments to be passed to each updatable object.
                **kwargs: A dictionary of named arguments to be passed to each updatable object.
            """
        all_sprites = self.groups.get("all_sprites")
        all_sprites.update(*args, **kwargs)

    def draw(self):
        """calls pygame draw function for all objects in scene
        """
        self.groups.get("all_sprites").draw(engine.Engine.screen)

    def check_win(self) -> bool:
        """checks if win condition is met in scene.

        Returns:
            boolean representing if the win condition has been met. Defaults to always being False
        """
        return False

    def initial_grid(self, **kwargs):
        """initializes board upon being set. Only implemented in child classes.

        Args:
            **kwargs: A dictionary of named arguments to be used as initialization parameters.
        """
        pass


class MazeScene(Scene):
    """Scene class for managing the GameObjects for a demo maze game.

    Attributes:
    game_objects: list of game objects in the scene.
    groups: dictionary storing all the sprite groups and their string names.
    rand: random number generator
    user_object: GameObject of the player
    tile_size: int representing how large of a square each sprite should be.
    """

    def __init__(self, tile_size: int):
        Scene.__init__(self, tile_size)
        walls = pygame.sprite.Group()
        paths = pygame.sprite.Group()
        player = pygame.sprite.Group()
        rectangles = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        self.groups.update({"walls": walls, "paths": paths, "player": player, "rectangles": rectangles,
                            "all_sprites": all_sprites})

    def initial_grid(self, **kwargs):
        """initializes board upon being set. Only implemented in child classes.

        Args:
            **kwargs: A dictionary of named arguments to be used as initialization parameters. Valid kwargs are has_walls=True and has_walls=False. has_walls=False means the board will generate as all paths while has_walls=True means the board will generate walls and paths at random. has_walls defaults to True
        """
        has_walls = True
        if kwargs.get("has_walls") is not None:
            has_walls = kwargs.get("has_walls")

        # if has_walls param is true, randomize if objects should be paths or walls to start
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

        # if has_walls param is false, generate board as all paths
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

    def check_win(self) -> bool:
        """checks if win condition is met in scene by checking if player is in the bottom right position.

        Returns:
            boolean representing if the win condition has been met.
        """
        # odd way to get it but the only way
        for players in self.groups.get("player"):
            player = players

        # check if player is in bottom right spot on board
        if player.x + player.center_x == engine.Engine.screen_width - player.center_x \
                and player.y + player.center_y == engine.Engine.screen_height - player.center_y:
            print("Congrats! You have won!")
            return True
        return False

    def draw(self):
        """calls pygame draw function for all objects in scene
        """
        self.groups.get("rectangles").draw(engine.Engine.screen)
        self.groups.get("player").draw(engine.Engine.screen)
