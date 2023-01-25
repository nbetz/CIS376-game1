import abc

import pygame.sprite


class GameObject:
    x: int
    y: int
    tags: list

    # TODO
    def __init__(self):
        pass


class Updatable(abc.ABC):

    @abc.abstractmethod
    def update(self):
        pass


class Drawable(abc.ABC):
    sprite: pygame.sprite.Sprite

    @abc.abstractmethod
    def draw(self):
        pass


class DGameObject(GameObject, Drawable):
    # TODO add override constructor to create Sprite for object

    # TODO
    def draw(self):
        pass


class DUGameObject(GameObject, Drawable, Updatable):
    # TODO add override constructor to create Sprite for object

    # TODO
    def update(self):
        pass

    # TODO
    def draw(self):
        pass


class UGameObject(GameObject, Updatable):
    # TODO
    def update(self):
        pass
