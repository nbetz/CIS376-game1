import pygame

#Logan Reneau
class Rectangle(pygame.Rect):
    def __init__(self, scene, isAlive, x, y):
        super().__init__(x, y, scene.tile_size-1, scene.tile_size-1)
        self.x = x
        self.y = y
        self.isAlive = isAlive
        if self.isAlive:
            self.color = (21, 71, 52)
        else:
            self.color = (0, 0, 0)


class userCircle():
    def __init__(self, scene):
        self.scene = scene
        self.x = 0
        self.y = 0
        self.centerX = 15
        self.centerY = 15
        self.radius = 5
        self.color = (255, 0, 0)

    def move(self, direction):
        if direction == 'r':
            self.x = self.x + self.scene.tile_size
        if direction == 'l':
            self.x = self.x - self.scene.tile_size
        if direction == 'u':
            self.y = self.y + self.scene.tile_size
        if direction == 'd':
            self.y = self.y - self.scene.tile_size

    def check_bound(self, coordinate_plane, cp_coordinate):
        if coordinate_plane == 'x':
            if cp_coordinate - self.scene.tile_size > 0:
                if cp_coordinate + self.scene.tile_size < self.scene.width:
                    return 1
            return 0
        elif cp_coordinate == 'y':
            if cp_coordinate - self.scene.tile_size > 0:
                if cp_coordinate + self.scene.tile_size < self.scene.height:
                    return 1
            return 0

