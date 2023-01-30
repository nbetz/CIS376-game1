import pygame

class Rectangle():
    x: int
    y: int
    color: tuple
    isAlive: bool
    def __init__(self, isAlive, x, y):
        self.x = x
        self.y = y
        self.isAlive = isAlive
        if self.isAlive:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 0)
        pass



