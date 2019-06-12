from pygame import Rect
from utilities.Vector2 import Vector2


class Entity:
    def __init__(self, x=0, y=0, width=1, height=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounds = Rect(self.x, self.y, self.width, self.height)
        self.location = Vector2(self.x, self.y)
        self.layer = 0

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.bounds = Rect(self.x, self.y, self.width, self.height)
        self.location = Vector2(self.x, self.y)
