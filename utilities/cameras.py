import pygame
from pygame import Rect
from utilities.Vector2 import Vector2
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


class Camera:
    SCALE = 0
    TOP_LEFT = Vector2(0, 0)
    BOUNDS = Rect(0, 0, 0, 0)

    def initialize(dimensions=(0, 0), scale=1):
        Camera.SCALE = scale
        Camera.TOP_LEFT = Vector2(0,  0)
        Camera.BOUNDS = Rect(
            Camera.TOP_LEFT.x, Camera.TOP_LEFT.y, dimensions[0], dimensions[1])

    def update(top_left=Vector2(0, 0)):
        Camera.TOP_LEFT.x = top_left.x - StaticCamera.HORIZONTAL_LETTERBOX
        Camera.TOP_LEFT.y = top_left.y - StaticCamera.VERTICAL_LETTERBOX
        Camera.BOUNDS.x = Camera.TOP_LEFT.x
        Camera.BOUNDS.y = Camera.TOP_LEFT.y
