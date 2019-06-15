import pygame
from enum import Enum
from utilities.vector import Vector2
from utilities.color import Color


class CameraType(Enum):
    DYNAMIC = 0
    STATIC = 1


class StaticCamera:
    SCALE = 0
    HORIZONTAL_LETTERBOX = 0
    VERTICAL_LETTERBOX = 0
    TOP_LEFT = Vector2()
    BOUNDS = pygame.Rect(0, 0, 0, 0)

    def __init__(self, dimensions=(0, 0), scale=1):
        StaticCamera.HORIZONTAL_LETTERBOX = 0
        StaticCamera.VERTICAL_LETTERBOX = 0
        StaticCamera.TOP_LEFT = Vector2(
            -StaticCamera.HORIZONTAL_LETTERBOX, - StaticCamera.VERTICAL_LETTERBOX)
        StaticCamera.SCALE = scale
        StaticCamera.BOUNDS = pygame.Rect(
            0, 0, dimensions[0], dimensions[1])

    def apply_horizontal_letterbox(self, horizontal_letterbox=0):
        StaticCamera.HORIZONTAL_LETTERBOX = horizontal_letterbox
        StaticCamera.TOP_LEFT.x = -StaticCamera.HORIZONTAL_LETTERBOX

    def apply_vertical_letterbox(self, vertical_letterbox=0):
        StaticCamera.VERTICAL_LETTERBOX = vertical_letterbox
        StaticCamera.TOP_LEFT.y = -StaticCamera.VERTICAL_LETTERBOX

    def draw(self, surface):
        # Top
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                -32 * StaticCamera.SCALE,
                -32 * StaticCamera.SCALE,
                StaticCamera.BOUNDS.width * StaticCamera.SCALE + 64 * StaticCamera.SCALE,
                StaticCamera.VERTICAL_LETTERBOX + 32 * StaticCamera.SCALE
            )
        )

        # Bottom
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                -32 * StaticCamera.SCALE,
                StaticCamera.VERTICAL_LETTERBOX +
                StaticCamera.BOUNDS.height * StaticCamera.SCALE,
                StaticCamera.BOUNDS.width * StaticCamera.SCALE + 64 * StaticCamera.SCALE,
                StaticCamera.VERTICAL_LETTERBOX + 32 * StaticCamera.SCALE
            )
        )

        # Left
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                -32 * StaticCamera.SCALE,
                -32 * StaticCamera.SCALE,
                StaticCamera.HORIZONTAL_LETTERBOX + 32 * StaticCamera.SCALE,
                StaticCamera.BOUNDS.height * StaticCamera.SCALE + 64 * StaticCamera.SCALE
            )
        )

        # Right
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                StaticCamera.HORIZONTAL_LETTERBOX + StaticCamera.BOUNDS.width * StaticCamera.SCALE,
                -32 * StaticCamera.SCALE,
                StaticCamera.HORIZONTAL_LETTERBOX,
                StaticCamera.BOUNDS.height * StaticCamera.SCALE + 64 * StaticCamera.SCALE
            )
        )


class Camera:
    SCALE = 0
    TOP_LEFT = Vector2()
    BOUNDS = pygame.Rect(0, 0, 0, 0)

    def __init__(self, top_left=Vector2(0, 0)):
        Camera.SCALE = StaticCamera.SCALE
        Camera.TOP_LEFT.x = top_left.x - StaticCamera.HORIZONTAL_LETTERBOX
        Camera.TOP_LEFT.y = top_left.y - StaticCamera.VERTICAL_LETTERBOX
        Camera.BOUNDS = pygame.Rect(
            Camera.TOP_LEFT.x, Camera.TOP_LEFT.y, StaticCamera.BOUNDS.width, StaticCamera.BOUNDS.height)

    def stay_within_bounds(self, top_left, world_bounds):
        if world_bounds.width == 0 or world_bounds.height == 0:
            world_bounds = pygame.Rect(
                0, 0, Camera.BOUNDS.width, Camera.BOUNDS.height)

        if top_left.x < world_bounds.left:
            top_left.x = world_bounds.left
        if top_left.x + Camera.BOUNDS.width > world_bounds.right:
            top_left.x = world_bounds.right - Camera.BOUNDS.width
        if top_left.y < world_bounds.top:
            top_left.y = world_bounds.top
        if top_left.y + Camera.BOUNDS.height > world_bounds.bottom:
            top_left.y = world_bounds.bottom - Camera.BOUNDS.height

        Camera.TOP_LEFT.x = top_left.x * Camera.SCALE - StaticCamera.HORIZONTAL_LETTERBOX
        Camera.TOP_LEFT.y = top_left.y * Camera.SCALE - StaticCamera.VERTICAL_LETTERBOX

    def update(self, top_left=Vector2(0, 0), world_bounds=pygame.Rect(0, 0, 0, 0)):
        Camera.SCALE = StaticCamera.SCALE
        self.stay_within_bounds(top_left, world_bounds)
