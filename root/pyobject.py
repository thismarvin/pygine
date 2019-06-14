from utilities.vector import Vector2
from utilities.camera import Camera


class PyObject(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = Vector2(self.x, self.y)

    def scaled_location(self):
        return Vector2(self.x * Camera.SCALE - Camera.TOP_LEFT.x, self.y * Camera.SCALE - Camera.TOP_LEFT.y)

    def set_location(self, x, y):
        self.x = x
        self.y = y        
        self.location = Vector2(self.x, self.y)

    