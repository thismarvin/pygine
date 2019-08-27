from pygame import Rect
from pygine.base import PygineObject
from pygine.draw import draw_rectangle
from pygine.geometry import Rectangle
from pygine import globals
from pygine.maths import Vector2
from pygine.resource import Sprite, SpriteType
from pygine.utilities import CameraType, Color, Input, InputType
from enum import IntEnum


class Entity(PygineObject):
    def __init__(self, x=0, y=0, width=1, height=1):
        super(Entity, self).__init__(x, y, width, height)
        self.color = Color.WHITE
        self.layer = 0
        self.remove = False
        self.__bounds_that_actually_draw_correctly = Rectangle(
            self.x, self.y, self.width, self.height, self.color, 2)

    def set_color(self, color):
        self.color = color
        self.__bounds_that_actually_draw_correctly.color = color

    def set_location(self, x, y):
        super(Entity, self).set_location(x, y)
        self.__bounds_that_actually_draw_correctly.set_location(self.x, self.y)

    def update(self, delta_time, entities):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the update(delta_time) method")

    def draw_bounds(self, surface, camera_type):
        self.__bounds_that_actually_draw_correctly.draw(surface, camera_type)

    def draw(self, surface):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the draw(surface) method")


class Direction(IntEnum):
    NONE = 0,
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4


class Kinetic(Entity):
    def __init__(self, x, y, width, height, speed):
        super(Kinetic, self).__init__(x, y, width, height)
        self.velocity = Vector2()
        self.default_move_speed = speed
        self.move_speed = 0
        self.facing = Direction.NONE
        self.collision_rectangles = []
        self.collision_width = 0

    def update_collision_rectangles(self):
        self.collision_width = 2
        self.collision_rectangles = [
            Rect(self.x + self.collision_width, self.y - self.collision_width,
                 self.width - self.collision_width * 2, self.collision_width),
            Rect(self.x + self.collision_width, self.y + self.height, self.width -
                 self.collision_width * 2, self.collision_width),
            Rect(self.x - self.collision_width, self.y + self.collision_width,
                 self.collision_width, self.height - self.collision_width * 2),
            Rect(self.x + self.width, self.y + self.collision_width,
                 self.collision_width, self.height - self.collision_width * 2)
        ]

    def calculate_scaled_speed(self, delta_time):
        self.move_speed = self.default_move_speed * delta_time

    def collision(self, entities):
        raise NotImplementedError(
            "A class that inherits Kinetic did not implement the collision(surface) method")

    def update(self, delta_time, entities):
        raise NotImplementedError(
            "A class that inherits Kinetic did not implement the update(delta_time, entities) method")

    def draw_collision_rectangles(self, surface):
        for r in self.collision_rectangles:
            draw_rectangle(
                surface,
                r,
                CameraType.DYNAMIC,
                Color.RED,
            )


class Actor(Kinetic):
    def __init__(self, x, y, width, height, speed):
        super(Actor, self).__init__(x, y, width, height, speed)
        self.input = Input()

    def _update_input(self):
        raise NotImplementedError(
            "A class that inherits Actor did not implement the _update_input() method")



class Player(Actor):
    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 14, 8, 50)
        self.sprite = Sprite(self.x - 9, self.y - 24, SpriteType.PLAYER)

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.sprite.set_location(self.x - 9, self.y - 24)

    def move(self, direction=Direction.NONE):
        self.facing = direction
        if self.facing == Direction.UP:
            self.set_location(self.x, self.y - self.move_speed)
            self.velocity.y = -1
        if self.facing == Direction.DOWN:
            self.set_location(self.x, self.y + self.move_speed)
            self.velocity.y = 1
        if self.facing == Direction.LEFT:
            self.set_location(self.x - self.move_speed, self.y)
            self.velocity.x = -1
        if self.facing == Direction.RIGHT:
            self.set_location(self.x + self.move_speed, self.y)
            self.velocity.x = 1

    def _update_input(self, delta_time):
        self.input.update(delta_time)
        if self.input.pressing(InputType.UP):
            self.move(Direction.UP)
        if self.input.pressing(InputType.DOWN):
            self.move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT):
            self.move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self.move(Direction.RIGHT)

    def rectanlge_collision_logic(self, entity):
        # Bottom
        if self.collision_rectangles[0].colliderect(entity.bounds) and self.velocity.y < 0:
            self.set_location(self.x, entity.bounds.bottom)
        # Top
        if self.collision_rectangles[1].colliderect(entity.bounds) and self.velocity.y > 0:
            self.set_location(self.x, entity.bounds.top - self.bounds.height)
        # Right
        if self.collision_rectangles[2].colliderect(entity.bounds) and self.velocity.x < 0:
            self.set_location(entity.bounds.right, self.y)
        # Left
        if self.collision_rectangles[3].colliderect(entity.bounds) and self.velocity.x > 0:
            self.set_location(entity.bounds.left - self.bounds.width, self.y)

    def collision(self, entities):
        for e in entities:
            if isinstance(e, Block):
                self.rectanlge_collision_logic(e)

    def update(self, delta_time, entities):
        self.calculate_scaled_speed(delta_time)
        self._update_input(delta_time)
        self.update_collision_rectangles()
        self.collision(entities)

    def draw(self, surface):       
        if globals.debugging:
            self.draw_collision_rectangles(surface)
            draw_rectangle(surface, self.bounds, CameraType.DYNAMIC, self.color)
        else:
             self.sprite.draw(surface, CameraType.DYNAMIC)



class Block(Entity):
    def __init__(self, x, y):
        super(Block, self).__init__(x, y, 32, 24)
        self.sprite = Sprite(self.x, self.y - 8, SpriteType.BLOCK)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        if globals.debugging:
            draw_rectangle(surface, self.bounds, CameraType.DYNAMIC, self.color)
        else:
             self.sprite.draw(surface, CameraType.DYNAMIC)
