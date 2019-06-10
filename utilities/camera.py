from pygame.math import Vector2
from pygame import Rect


class Camera:
    def __init__(self, top_left=Vector2(0, 0), dimensions=(0, 0), scale=1):
        self.top_left = Vector2(top_left)
        self.bounds = Rect(self.top_left.x, self.top_left.y,
                           dimensions[0], dimensions[1])
        self.scale = scale

    def update(self, top_left=Vector2(0, 0)):
        self.top_left = Vector2(top_left)
        self.bounds.x = self.top_left.x
        self.bounds.y = self.top_left.y
