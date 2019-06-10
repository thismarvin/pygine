from pygame.math import Vector2
from entities.geometry.rectangle import Rectangle
from utilities.color import Color
from utilities.input import Input
from utilities.input import InputType


class Playfield:
    def __init__(self, camera):
        self.camera = camera
        self.camera_location = Vector2(0, 0)
        self.input = Input()

    def update_camera(self):
        self.camera.update()

    def update_input(self, delta_time):
        self.input.update()

    def update(self, delta_time):
        self.update_camera()
        self.update_input()

    def draw(self, surface):
        ""
