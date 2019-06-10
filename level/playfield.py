from pygame.math import Vector2
from entities.geometry.rectangle import Rectangle
from utilities.color import Color


class Playfield:
    def __init__(self, camera):
        self.camera = camera
        self.camera_location = Vector2(0,0)

    def update(self, delta_time):
        self.camera.update()

    def draw(self, surface):
        ""
