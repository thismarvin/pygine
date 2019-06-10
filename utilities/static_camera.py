import pygame
from pygame.math import Vector2
from pygame import Rect
from utilities.color import Color


class StaticCamera:
    HORIZONTAL_LETTERBOX = 0
    VERTICAL_LETTERBOX = 0
    BOUNDS = Rect(0, 0, 0, 0)

    def initialize(dimensions=(0, 0), scale=1):
        StaticCamera.BOUNDS = Rect(
            0, 0, dimensions[0] * scale, dimensions[1] * scale)
        StaticCamera.HORIZONTAL_LETTERBOX = 0
        StaticCamera.VERTICAL_LETTERBOX = 0

    def apply_horizontal_letterbox(horizontal_letterbox=0):
        StaticCamera.HORIZONTAL_LETTERBOX = horizontal_letterbox

    def apply_vertical_letterbox(vertical_letterbox=0):
        StaticCamera.VERTICAL_LETTERBOX = vertical_letterbox

    def draw(surface):
        pygame.draw.rect(surface, Color.BLACK, (-32, -32,
                                                StaticCamera.BOUNDS.width + 64, StaticCamera.VERTICAL_LETTERBOX + 32))
        pygame.draw.rect(surface, Color.BLACK, (-32, StaticCamera.VERTICAL_LETTERBOX +
                                                StaticCamera.BOUNDS.height, StaticCamera.BOUNDS.width + 64, StaticCamera.VERTICAL_LETTERBOX + 32))
        pygame.draw.rect(surface, Color.BLACK, (-32, -32,
                                                StaticCamera.HORIZONTAL_LETTERBOX + 32, StaticCamera.BOUNDS.height + 64))
        pygame.draw.rect(surface, Color.BLACK, (StaticCamera.HORIZONTAL_LETTERBOX +
                                                StaticCamera.BOUNDS.width, -32, StaticCamera.HORIZONTAL_LETTERBOX, StaticCamera.BOUNDS.height + 64))
