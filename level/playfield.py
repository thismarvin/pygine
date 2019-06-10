from pygame.math import Vector2
from entities.geometry.rectangle import Rectangle
from utilities.color import Color
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera


class Playfield:
    def __init__(self):
        self.camera_location = Vector2(0, 0)
        self.input = Input()

    def update_camera(self):
        Camera.update()

    def update_input(self):
        self.input.update()

    def update(self, delta_time):
        self.update_camera()
        self.update_input()

    def draw(self, surface):
        ""
