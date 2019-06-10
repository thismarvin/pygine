import pygame
from enum import Enum


class InputType(Enum):
    NONE = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    TOGGLE_FULLSCREEN = 5
    QUIT = 6


class Input:
    def __init__(self):
        self.key_state = None

    def pressing(self, type=InputType.NONE):
        if type == InputType.UP:
            return self.key_state[pygame.K_UP] or self.key_state[pygame.K_w]
        if type == InputType.LEFT:
            return self.key_state[pygame.K_LEFT] or self.key_state[pygame.K_a]
        if type == InputType.DOWN:
            return self.key_state[pygame.K_DOWN] or self.key_state[pygame.K_s]
        if type == InputType.RIGHT:
            return self.key_state[pygame.K_RIGHT] or self.key_state[pygame.K_d]
        if type == InputType.TOGGLE_FULLSCREEN:
            return self.key_state[pygame.K_F10]
        if type == InputType.QUIT:
            return self.key_state[pygame.K_ESCAPE]
        return False

    def update(self):
        self.key_state = pygame.key.get_pressed()
