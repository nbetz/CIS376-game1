import pygame

class Rectangle(pygame.Rect):
    def __init__(self, isAlive, x, y):
        super().__init__(x, y, 29, 29)
        self.x = x
        self.y = y
        self.isAlive = isAlive
        if self.isAlive:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 0)



