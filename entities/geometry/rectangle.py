import pygame
from pygame import Rect
from entities.entity import Entity
from utilities.color import Color
from utilities.cameras import Camera


class Rectangle(Entity):
    def __init__(self, x=0, y=0, width=1, height=1, thickness=0, color=Color.WHITE):
        Entity.__init__(self, x, y, width, height)
        self.thickness = thickness
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (
                -Camera.TOP_LEFT.x + self.x * Camera.SCALE,
                -Camera.TOP_LEFT.y + self.y * Camera.SCALE,
                self.width * Camera.SCALE,
                self.height * Camera.SCALE
            ),
            int(self.thickness * Camera.SCALE)
        )
