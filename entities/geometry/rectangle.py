import pygame
from entities.entity import Entity
from utilities.color import Color
from utilities.camera import Camera
from utilities.camera import CameraType


class Rectangle(Entity):
    def __init__(self, x=0, y=0, width=1, height=1, thickness=0, color=Color.WHITE):
        super(Rectangle, self).__init__(x, y, width, height)
        self.thickness = thickness
        self.color = color

    def update(self, delta_time):
        pass

    def draw(self, surface, camera_type=CameraType.DYNAMIC):
        pygame.draw.rect(
            surface,
            self.color,
            (
                self.scaled_location(camera_type).x,
                self.scaled_location(camera_type).y,
                self.scaled_width(),
                self.scaled_height()
            ),
            int(self.thickness * Camera.SCALE)
        )
