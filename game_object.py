import pygame
import random

from pygame.sprite import AbstractGroup

import engine


class GameObject(pygame.sprite.DirtySprite):
    def __init__(self, x, y, in_scene, *groups: AbstractGroup):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.scene = in_scene


# Logan Reneau
# check that the x and y coordinates are within the bounds of the board
def valid_input(x, y):
    if 0 <= x < engine.Engine.screen_width:
        if 0 <= y < engine.Engine.screen_height:
            return 1
    return 0


def generate_random_color():
    return random.randint(15, 255), random.randint(15, 255), random.randint(15, 255)


class Rectangle(GameObject):
    def __init__(self, is_wall, x, y, in_scene):
        GameObject.__init__(self, x, y, in_scene)
        self.is_wall = is_wall
        self.last_is_wall = is_wall
        self.skip_update = False
        self.add(self.scene.groups.get("rectangles"))
        self.scene.groups.get("all_sprites")
        if self.is_wall:
            self.color = generate_random_color()
            self.add(self.scene.groups.get("walls"))
        else:
            self.color = (0, 0, 0)
            self.add(self.scene.groups.get("paths"))

        # create sprite image and rectangle
        self.image = pygame.Surface([self.scene.tile_size, self.scene.tile_size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def should_flip(self):
        current_index = self.scene.game_objects.index(self)
        count = 0
        count = count + self.check_top_row(current_index)
        count = count + self.check_current_row(current_index)
        count = count + self.check_bottom_row(current_index)

        if self.last_is_wall:
            if count < 1 or count > 4:
                return True
            return False
        else:
            if pygame.sprite.spritecollideany(self, self.scene.groups.get("player")) is None:
                if count == 3:
                    return True
            return False

    def check_top_row(self, current_index):
        count = 0
        # set new_index to be same x position in row above
        new_index = current_index - int((engine.Engine.screen_width / self.scene.tile_size))
        # top right
        if valid_input(self.last_x + self.scene.tile_size, self.last_y - self.scene.tile_size) == 1:
            if self.scene.game_objects[new_index + 1].last_is_wall:
                count = count + 1
        # top
        if valid_input(self.last_x, self.last_y - self.scene.tile_size) == 1:
            if self.scene.game_objects[new_index].last_is_wall:
                count = count + 1
        # top left
        if valid_input(self.last_x - self.scene.tile_size, self.last_y - self.scene.tile_size) == 1:
            if self.scene.game_objects[new_index - 1].last_is_wall:
                count = count + 1
        return count

    def check_current_row(self, current_index):
        count = 0
        # left
        if valid_input(self.last_x - self.scene.tile_size, self.last_y) == 1:
            if self.scene.game_objects[current_index - 1].last_is_wall:
                count = count + 1
        # right
        if valid_input(self.x + self.scene.tile_size, self.y) == 1:
            if self.scene.game_objects[current_index + 1].is_wall:
                count = count + 1
        return count

    def check_bottom_row(self, current_index):
        count = 0
        # set new_index to be same x position in row above
        new_index = current_index + int((engine.Engine.screen_width / self.scene.tile_size))
        # bottom left
        if valid_input(self.x - self.scene.tile_size, self.y + self.scene.tile_size) == 1:
            if self.scene.game_objects[new_index - 1].is_wall:
                count = count + 1
        # bottom
        if valid_input(self.x, self.y + self.scene.tile_size) == 1:
            if self.scene.game_objects[new_index].is_wall:
                count = count + 1
        # bottom right
        if valid_input(self.x + self.scene.tile_size, self.y + self.scene.tile_size) == 1:
            if self.scene.game_objects[new_index + 1].is_wall:
                count = count + 1
        return count

    def update(self, *args, **kwargs):
        if kwargs.get("type") == "click":
            self.skip_update = True
            if self.last_is_wall:
                self.add(self.scene.groups.get("paths"))
                self.remove(self.scene.groups.get("walls"))
                self.is_wall = False
                self.color = (0, 0, 0)
                self.image.fill(self.color)
                self.dirty = 1
            else:
                self.add(self.scene.groups.get("walls"))
                self.remove(self.scene.groups.get("paths"))
                self.is_wall = True
                self.color = generate_random_color()
                self.image.fill(self.color)
                self.dirty = 1
        elif not self.skip_update:
            self.last_x = self.x
            self.last_y = self.y
            self.last_is_wall = self.is_wall
            if self.should_flip():
                if self.last_is_wall:
                    self.add(self.scene.groups.get("paths"))
                    self.remove(self.scene.groups.get("walls"))
                    self.is_wall = False
                    self.color = (0, 0, 0)
                    self.image.fill(self.color)
                    self.dirty = 1
                else:
                    self.add(self.scene.groups.get("walls"))
                    self.remove(self.scene.groups.get("paths"))
                    self.is_wall = True
                    self.color = generate_random_color()
                    self.image.fill(self.color)
                    self.dirty = 1
        else:
            self.skip_update = False


class PlayerCircle(GameObject):
    def __init__(self, in_scene):
        super().__init__(0, 0, in_scene)
        self.centerX = 15
        self.centerY = 15
        self.radius = 5
        self.color = (255, 0, 0)

        # https://www.reddit.com/r/pygame/comments/6v9os5/how_to_draw_a_sprite_with_a_circular_shape/
        self.image = pygame.Surface([self.scene.tile_size, self.scene.tile_size], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.centerX, self.centerY), self.radius)
        self.rect = self.image.get_rect(center=(self.centerX, self.centerY))

    # TODO need to use engine delta time,
    #  also don't move entire tiles at a time
    def move_player(self, direction):
        if direction == "right":
            self.x = self.x + self.scene.tile_size
            self.rect.x = self.x
        if direction == "left":
            self.x = self.x - self.scene.tile_size
            self.rect.x = self.x
        if direction == "up":
            self.y = self.y - self.scene.tile_size
            self.rect.y = self.y
        if direction == "down":
            self.y = self.y + self.scene.tile_size
            self.rect.y = self.y

    def check_bound(self, coordinate_plane, cp_coordinate, direction):
        if coordinate_plane == 'x':
            if cp_coordinate - self.scene.tile_size < 0 and direction == "left":
                return 0
            if cp_coordinate + self.scene.tile_size >= engine.Engine.screen_width and direction == "right":
                return 0
            return 1
        elif coordinate_plane == 'y':
            if cp_coordinate - self.scene.tile_size < 0 and direction == "up":
                return 0
            if cp_coordinate + self.scene.tile_size >= engine.Engine.screen_height and direction == "down":
                return 0
            return 1

    def check_collision(self, direction):
        pass

    def update(self, *args, **kwargs):
        if kwargs.get("type") == "keydown":
            direction = ""
            if(kwargs.get("key") == pygame.K_w or kwargs.get("key") == pygame.K_UP):
                direction = "up"
            if (kwargs.get("key") == pygame.K_s or kwargs.get("key") == pygame.K_DOWN):
                direction = "down"
            if (kwargs.get("key") == pygame.K_a or kwargs.get("key") == pygame.K_LEFT):
                direction = "left"
            if (kwargs.get("key") == pygame.K_d or kwargs.get("key") == pygame.K_RIGHT):
                direction = "right"

            if direction == "right" or direction == "left":
                if self.check_bound('x', self.x, direction):
                    #if not self.check_collision():
                        self.move_player(direction)

            elif direction == "up" or direction == "down":
                if self.check_bound('y', self.y, direction):
                    #if self.check_collision():
                        self.move_player(direction)
            self.dirty = 1
