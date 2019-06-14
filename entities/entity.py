from pygame import Rect 
from root.pyobject import PyObject
from utilities.vector import Vector2
from utilities.camera import Camera


class Entity(PyObject):
    def __init__(self, x=0, y=0, width=1, height=1):
        super(Entity, self).__init__(x,y)
        self.width = width
        self.height = height
        self.bounds = Rect(self.x, self.y, self.width, self.height)
        self.layer = 0

    def set_location(self, x, y):
        super().set_location(x,y)
        self.bounds = Rect(self.x, self.y, self.width, self.height)

    def set_width(self, width):
        self.width = width
        self.bounds = Rect(self.x, self.y, self.width, self.height)

    def set_height(self, height):
        self.height = height
        self.bounds = Rect(self.x, self.y, self.width, self.height)

    def scaled_width(self):
        return self.width * Camera.SCALE

    def scaled_height(self):
        return self.height * Camera.SCALE

    def update(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the update(delta_time) method")

    def draw(self, surface):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the draw(surface) method")
