import pygame
import random

from pygame.sprite import AbstractGroup

import engine


class GameObject(pygame.sprite.DirtySprite):
    def __init__(self, x, y, in_scene, *groups: AbstractGroup):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.scene = in_scene


class Rectangle(GameObject):
    def __init__(self, is_wall, x, y, in_scene):
        GameObject.__init__(self, x, y, in_scene)
        self.is_wall = is_wall
        if self.is_wall:
            self.color = (random.randint(15, 255), random.randint(15, 255), random.randint(15, 255))
        else:
            self.color = (0, 0, 0)

        # create sprite image and rectangle
        self.image = pygame.Surface([self.scene.tile_size, self.scene.tile_size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.is_wall:
            self.is_wall = False
            self.color = (0, 0, 0)
            self.image.fill(self.color)
            self.dirty = 1
        elif not self.is_wall:
            self.is_wall = True
            self.color = (21, 71, 52)
            self.image.fill(self.color)
            self.dirty = 1


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

    # def check_collision(self, direction):
    #     self.move_player(direction)
    #     if(pygame.sprite.spritecollide(self, self.scene.groups.get("walls"), False, None):
    #         self.move_player()

    def update(self, direction):
        if direction == "right" or direction == "left":
            if self.check_bound('x', self.x, direction):
                #if not self.check_collision():
                    self.move_player(direction)

        elif direction == "up" or direction == "down":
            if self.check_bound('y', self.y, direction):
                #if self.check_collision():
                    self.move_player(direction)
        self.dirty = 1
