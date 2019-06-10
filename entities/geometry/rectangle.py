import pygame
from pygame import Rect
from entities.entity import Entity
from utilities.color import Color


class Rectangle(Entity):
    def __init__(self, x=0, y=0, width=1, height=1, thickness=0, color=Color.WHITE):
        Entity.__init__(self, x, y, width, height)
        self.thickness = thickness
        self.color = color

    def draw(self, surface, camera):
        pygame.draw.rect(
            surface,
            self.color,
            (
                -camera.top_left.x + self.x * camera.scale,
                -camera.top_left.y + self.y * camera.scale,
                self.width * camera.scale,
                self.height * camera.scale
            ),
            int(self.thickness * camera.scale)
        )
