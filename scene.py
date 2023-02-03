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

    def draw(self):
        pass

# Logan Reneau
def valid_input(x, y):
    if 0 <= x < engine.Engine.screen_width:
        if 0 <= y < engine.Engine.screen_height:
            return 1
    return 0


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

    # TODO temporary until checkcell code is moved to Rectangle game object
    def update_all_objects(self):
        # calls update() method for all updatable game objects in scene
        [self.check_cell(game_obj) for game_obj in self.game_objects if isinstance(game_obj, game_object.Rectangle)]

    # Logan Reneau
    def initial_grid(self):
        for y in range(0, engine.Engine.screen_height, self.tile_size):
            for x in range(0, engine.Engine.screen_width, self.tile_size):
                temp = random.randint(0, 1)
                if temp == 1:
                    life = True
                else:
                    life = False
                rectangle = game_object.Rectangle(life, x, y, self)
                rectangle.add(self.groups.get("rectangles"))
                rectangle.add(self.groups.get("all_sprites"))
                if life:
                    rectangle.add(self.groups.get("walls"))
                else:
                    rectangle.add(self.groups.get("paths"))
                self.game_objects.append(rectangle)

                self.draw()

        # make sure that the player object is able to spawn in
        self.game_objects[0].is_wall = False
        self.game_objects[0].color = (0, 0, 0)
        player_obj = game_object.PlayerCircle(self)
        player_obj.add(self.groups.get("all_sprites"))
        player_obj.add(self.groups.get("player"))

    # Logan Reneau
    def check_cell(self, cell):
        current_index = self.game_objects.index(cell)
        count = 0
        # top left
        if valid_input(cell.x - self.tile_size, cell.y - self.tile_size) == 1:
            if self.game_objects[int(current_index - (engine.Engine.screen_width / self.tile_size) + 1)].is_wall:
                count = count + 1
        # top
        if valid_input(cell.x, cell.y - self.tile_size) == 1:
            if self.game_objects[int(current_index - (engine.Engine.screen_width / self.tile_size))].is_wall:
                count = count + 1
        # top right
        if valid_input(cell.x + self.tile_size, cell.y - self.tile_size) == 1:
            if self.game_objects[int(current_index - (engine.Engine.screen_width / self.tile_size) - 1)].is_wall:
                count = count + 1
        # left
        if valid_input(cell.x - self.tile_size, cell.y) == 1:
            if self.game_objects[current_index - 1].is_wall:
                count = count + 1
        # right
        if valid_input(cell.x + self.tile_size, cell.y) == 1:
            if self.game_objects[current_index + 1].is_wall:
                count = count + 1
        # bottom left
        if valid_input(cell.x - self.tile_size, cell.y + self.tile_size) == 1:
            if self.game_objects[int(current_index + (engine.Engine.screen_width / self.tile_size) - 1)].is_wall:
                count = count + 1
        # bottom
        if valid_input(cell.x, cell.y + self.tile_size) == 1:
            if self.game_objects[int(current_index + (engine.Engine.screen_width / self.tile_size))].is_wall:
                count = count + 1
        # bottom right
        if valid_input(cell.x + self.tile_size, cell.y + self.tile_size) == 1:
            if self.game_objects[int(current_index + (engine.Engine.screen_width / self.tile_size) + 1)].is_wall:
                count = count + 1

        if cell.is_wall:
            if count < 1 or count > 4:
                cell.update()
                cell.remove(self.groups.get("walls"))
                cell.add(self.groups.get("paths"))

        else:
            if count == 3:
                cell.update()
                cell.remove(self.groups.get("paths"))
                cell.add(self.groups.get("walls"))

    # Noah Betz
    def draw(self):
        sprite_group = self.groups.get("all_sprites")
        sprite_group.draw(engine.Engine.screen)
