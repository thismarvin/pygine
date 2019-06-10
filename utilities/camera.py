import pygame
from pygame.math import Vector2
from pygame import Rect
from utilities.color import Color
from utilities.static_camera import StaticCamera


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
