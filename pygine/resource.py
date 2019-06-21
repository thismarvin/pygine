import pygame
from pygine.base import PygineObject
from pygine.draw import draw_image
from enum import IntEnum


class SpriteType(IntEnum):
    NONE = 0
    PLAYER = 1
    BLOCK = 2


class Sprite(PygineObject):
    def __init__(self, x=0.0, y=0.0, sprite_type=SpriteType.NONE):
        super(Sprite, self).__init__(x, y, 0, 0)
        self.type = sprite_type
        self.load_sprite()

    def sprite_setup(self, sprite_x=0, sprite_y=0, width=0, height=0, sprite_sheet_name=""):
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.set_width(width)
        self.set_height(height)
        self.sprite_sheet = pygame.image.load(
            'pygine/assets/sprites/{}'.format(sprite_sheet_name)
        )

    def load_sprite(self):
        if self.type == SpriteType.NONE:
            pass
        elif (self.type == SpriteType.PLAYER):
            self.sprite_setup(0, 0, 32, 32, "sprites.png")
        elif (self.type == SpriteType.BLOCK):
            self.sprite_setup(0, 32, 32, 32, "sprites.png")

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(self.sprite_sheet, (0, 0),
                        (self.sprite_x, self.sprite_y, self.width, self.height))

    def draw(self, surface, camera_type):
        draw_image(surface, self.image, self.bounds, camera_type)
