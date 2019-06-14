from enum import Enum
from entities.entity import Entity
from entities.geometry.rectangle import Rectangle
from utilities.vector import Vector2
from utilities.color import Color


class Direction(Enum):
    NONE=0,
    UP=1,
    DOWN=2,
    LEFT=3,
    RIGHT=4


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
        self.collision_rectangles=[
            Rectangle(self.x + self.collision_width, self.y - self.collision_width, self.width - self.collision_width * 2, self.collision_width, 0, Color.RED),
            Rectangle(self.x + self.collision_width, self.y + self.height, self.width - self.collision_width * 2, self.collision_width, 0, Color.RED),
            Rectangle(self.x - self.collision_width, self.y + self.collision_width, self.collision_width, self.height - self.collision_width * 2, 0, Color.RED),
            Rectangle(self.x + self.width, self.y + self.collision_width, self.collision_width, self.height - self.collision_width * 2, 0, Color.RED)
            ]

    def calculate_scaled_speed(self, delta_time):
        self.move_speed = self.default_move_speed * delta_time

