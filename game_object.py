"""Game objects built upon pygame.sprite.Dirtysprite

Provides basic functions for creating GameObjects for a game. Also includes Objects for MazeGame demo game.
"""

import pygame
import random

from pygame.sprite import AbstractGroup

import engine
import scene


class GameObject(pygame.sprite.DirtySprite):
    """GameObject class providing basic GameObject info ontop of pygame.sprite.DirtySprite

        Intended to be extended by other classes to provide a base for creating game objects.

        Attributes:
            x: int for x position of object.
            y: int for x position of object.
            last_x: int for last x value during update sequence.
            last_y: int for last y value during update sequence.
            in_scene: scene.Scene that the object belongs to
            *groups: Tuple of pygame Groups that the object belongs to
            image: image of the sprite to be drawn.
            rect: bounding box of the sprite.
        """
    def __init__(self, x: int, y: int, in_scene: "Scene", *groups: AbstractGroup):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.scene = in_scene


# check that the x and y coordinates are within the bounds of the board
def valid_input(x: int, y: int) -> bool:
    """determines if a given point is out of the bounds of the screen

        Args:
            x: An int representing the X coordinate.
            y: An int representing the Y coordinate.

        Returns:
            True if the point is in bounds or False if the point is out of bounds
        """

    if 0 <= x < engine.Engine.screen_width:
        if 0 <= y < engine.Engine.screen_height:
            return True
    return False


def generate_random_color() -> tuple:
    """generates a random color tuple with 3 values between 15-255 representing R,G,B

            Returns:
                A random color tuple with 3 values between 15-255 representing R,G,B.
            """
    return random.randint(15, 255), random.randint(15, 255), random.randint(15, 255)


class Rectangle(GameObject):
    """GameObject class representing a rectangle as a wall or path for MazeGame

        Attributes:
            x: int for x position of object.
            y: int for x position of object.
            is_wall: bool representing if object is wall or path.
            last_x: int for last x value during update sequence.
            last_y: int for last y value during update sequence.
            last_is_wall: bool for last is_wall value during update sequence.
            in_scene: scene.Scene that the object belongs to.
            *groups: Tuple of pygame Groups that the object belongs to.
            color: tuple representing R,G,B color of the circle.
            image: image of the sprite to be drawn.
            rect: bounding box of the sprite.
            skip_update: bool representing if object should skip the main update loop for any reason.
        """
    def __init__(self, is_wall: bool, x: int, y: int, in_scene: "Scene"):
        GameObject.__init__(self, x, y, in_scene)
        self.is_wall = is_wall
        self.last_is_wall = is_wall
        self.skip_update = False
        self.add(self.scene.groups.get("rectangles"))
        self.add(self.scene.groups.get("all_sprites"))
        if self.is_wall:
            self.color = generate_random_color()
            self.add(self.scene.groups.get("walls"))
        else:
            self.color = (0, 0, 0)
            self.add(self.scene.groups.get("paths"))

        # create sprite image and rectangle
        self.image = pygame.Surface([self.scene.tile_size - 1, self.scene.tile_size - 1])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _should_flip(self) -> bool:
        # get the index of the current object in the game_scene game_objects list
        current_index = self.scene.game_objects.index(self)
        count = 0

        # set count to be the number of adjacent Rectangle objects that are walls
        count = count + self._check_top_row(current_index)
        count = count + self._check_current_row(current_index)
        count = count + self._check_bottom_row(current_index)

        # return true if the current object is a wall and there not between 1-4 adjacent walls
        if self.last_is_wall:
            if count < 1 or count > 4:
                return True
            return False
        else:
            # don't flip if the player is in the space of the object and the object is a path
            if pygame.sprite.spritecollideany(self, self.scene.groups.get("player")) is None:
                # return true if there are exactly 3 adjacent walls and the current object is a path
                if count == 3:
                    return True
            return False

    def _check_top_row(self, current_index: int) -> int:
        count = 0
        # set new_index to be same x position in row above
        new_index = current_index - int((engine.Engine.screen_width / self.scene.tile_size))

        # uses last values for all because anything above will be updated earlier this update cycle
        # top right
        if valid_input(self.last_x + self.scene.tile_size, self.last_y - self.scene.tile_size):
            if self.scene.game_objects[new_index + 1].last_is_wall:
                count = count + 1
        # top
        if valid_input(self.last_x, self.last_y - self.scene.tile_size):
            if self.scene.game_objects[new_index].last_is_wall:
                count = count + 1
        # top left
        if valid_input(self.last_x - self.scene.tile_size, self.last_y - self.scene.tile_size):
            if self.scene.game_objects[new_index - 1].last_is_wall:
                count = count + 1
        return count

    def _check_current_row(self, current_index: int) -> int:
        count = 0
        # left
        # uses last values for left because object to the left will be updated before this object
        if valid_input(self.last_x - self.scene.tile_size, self.last_y):
            if self.scene.game_objects[current_index - 1].last_is_wall:
                count = count + 1
        # right
        if valid_input(self.x + self.scene.tile_size, self.y):
            if self.scene.game_objects[current_index + 1].is_wall:
                count = count + 1
        return count

    def _check_bottom_row(self, current_index: int) -> int:
        count = 0
        # set new_index to be same x position in row above
        new_index = current_index + int((engine.Engine.screen_width / self.scene.tile_size))
        # bottom left
        if valid_input(self.x - self.scene.tile_size, self.y + self.scene.tile_size):
            if self.scene.game_objects[new_index - 1].is_wall:
                count = count + 1
        # bottom
        if valid_input(self.x, self.y + self.scene.tile_size):
            if self.scene.game_objects[new_index].is_wall:
                count = count + 1
        # bottom right
        if valid_input(self.x + self.scene.tile_size, self.y + self.scene.tile_size):
            if self.scene.game_objects[new_index + 1].is_wall:
                count = count + 1
        return count

    def update(self, *args, **kwargs):
        """override of pygame.sprite.Sprite update method. Updates the object according to the parameters and the
        environment. Flips the Rectangle from wall to path (and vice versa) if it is clicked. flips the rectangle if
        it is a wall and there are not between 1-4 neighboring walls. Flips the rectangle if it is a path and there
        are exactly 3 neighboring walls.

            Args:
                *args: A tuple of arguments to be passed to each updatable object.
                **kwargs: A dictionary of named arguments to be passed to each updatable object. Valid kwargs are type="click" and position=event.pos which are used in tandem for checking if rectangle has been clicked.
        """
        # if update was of type "click" for mouseclick, check if the click was on the current object
        if kwargs.get("type") == "click":
            if self.rect.collidepoint(kwargs.get("position")):
                # verify player is not in this spot
                if pygame.sprite.spritecollideany(self, self.scene.groups.get("player")) is None:
                    # flip the object from wall to path or from path to wall if clicked on
                    # set skip_update to true so the object won't update again during main update
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
        # if update param type is "main" do the normal logic
        elif kwargs.get("type") == "main":
            if not self.skip_update:
                # store important params in last_x, last_y, last_is_wall, to act as double buffer
                self.last_x = self.x
                self.last_y = self.y
                self.last_is_wall = self.is_wall

                # check if the object should flip and do so
                if self._should_flip():
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
            # consume the skip_update so the object will resume being updated like normal
            else:
                self.skip_update = False


class PlayerCircle(GameObject):
    """GameObject class representing a Player as a circle for MazeGame

        Attributes:
            x: int for x position of object.
            y: int for x position of object.
            in_scene: scene.Scene that the object belongs to
            *groups: Tuple of pygame Groups that the object belongs to
            center_x: int representing the X value of the center of the circle
            CenterY: int representing the Y value of the center of the circle
            radius: int representing the radius of the circle
            color: tuple representing R,G,B color of the circle
            image: image of the sprite to be drawn
            rect: bounding box of the sprite
        """
    def __init__(self, in_scene: "Scene"):
        super().__init__(0, 0, in_scene)
        self.center_x = int(self.scene.tile_size / 2)
        self.center_y = int(self.scene.tile_size / 2)
        self.radius = (self.scene.tile_size / 2) - 1
        self.color = (255, 0, 0)

        # https://www.reddit.com/r/pygame/comments/6v9os5/how_to_draw_a_sprite_with_a_circular_shape/
        self.image = pygame.Surface([self.scene.tile_size, self.scene.tile_size], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.center_x, self.center_y), self.radius)
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))

    def _move_player(self, direction: str):
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

    def _check_bound(self, coordinate_plane: str, cp_coordinate: int, direction: str) -> bool:
        if coordinate_plane == 'x':
            if cp_coordinate - self.scene.tile_size < 0 and direction == "left":
                return False
            if cp_coordinate + self.scene.tile_size >= engine.Engine.screen_width and direction == "right":
                return False
            return True
        elif coordinate_plane == 'y':
            if cp_coordinate - self.scene.tile_size < 0 and direction == "up":
                return False
            if cp_coordinate + self.scene.tile_size >= engine.Engine.screen_height and direction == "down":
                return False
            return True

    def _check_collision(self, direction: str) -> bool:
        count = 0
        row_count = int((engine.Engine.screen_width / self.scene.tile_size))

        # find the index of the game_object with the same x and y coordinate as the player
        for item in self.scene.game_objects:
            if item.x == self.x and item.y == self.y:
                break
            count = count + 1
        current_index = count

        # check if player can move 1 space right
        if direction == "right":
            if self.scene.game_objects[current_index + 1].is_wall:
                return True
            return False

        # check if player can move 1 space left
        if direction == "left":
            if self.scene.game_objects[current_index - 1].is_wall:
                return True
            return False

        # check if player can move 1 space up
        if direction == "up":
            if self.scene.game_objects[current_index - row_count].is_wall:
                return True
            return False

        # check if player can move 1 space down
        if direction == "down":
            if self.scene.game_objects[current_index + row_count].is_wall:
                return True
            return False

    def update(self, *args, **kwargs):
        """override of pygame.sprite.Sprite update method. Updates the object according to the parameters given.

            Args:
                *args: A tuple of arguments to be passed to each updatable object.
                **kwargs: A dictionary of named arguments to be passed to each updatable object. Valid kwargs are type="keydown" and key=pygame.key which are used in tandem for checking if the player needs to move based on user input.
        """
        if kwargs.get("type") == "keydown":
            direction = ""
            # set the direction based on the key being pressed
            if kwargs.get("key") == pygame.K_w or kwargs.get("key") == pygame.K_UP:
                direction = "up"
            if kwargs.get("key") == pygame.K_s or kwargs.get("key") == pygame.K_DOWN:
                direction = "down"
            if kwargs.get("key") == pygame.K_a or kwargs.get("key") == pygame.K_LEFT:
                direction = "left"
            if kwargs.get("key") == pygame.K_d or kwargs.get("key") == pygame.K_RIGHT:
                direction = "right"

            # check validity of move and then move player on X axis
            if direction == "right" or direction == "left":
                if self._check_bound('x', self.x, direction):
                    if not self._check_collision(direction):
                        self._move_player(direction)

            # check validity of move and then move player on Y axis
            elif direction == "up" or direction == "down":
                if self._check_bound('y', self.y, direction):
                    if not self._check_collision(direction):
                        self._move_player(direction)
            self.dirty = 1
