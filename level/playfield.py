from pygame import Rect
from level.hud import HUD
from entities.user.player import Player
from utilities.vector import Vector2
from utilities.color import Color
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera
from entities.geometry.rectangle import Rectangle


class Playfield:
    ENTITIES = []

    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.hud = HUD()
        self.input = Input()
        self.reset()
        self.test = Rectangle(0, 0, Camera.BOUNDS.width,
                              Camera.BOUNDS.height, 5)

    def reset(self):
        self.player = Player(10, 10, 10, 10)

        Playfield.ENTITIES = []
        Playfield.ENTITIES.append(self.player)

    def update_camera(self):
        self.camera.update(
            Vector2(self.player.x - Camera.BOUNDS.width / 2,
                    self.player.y - Camera.BOUNDS.height / 2))

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.RESET):
            self.reset()
            self.hud.reset()

    def update_entities(self, delta_time):
        for i in range(len(Playfield.ENTITIES) - 1, -1, -1):
            Playfield.ENTITIES[i].update(delta_time)

    def update(self, delta_time):
        self.update_camera()
        self.update_input()
        self.update_entities(delta_time)
        self.hud.update(delta_time)

    def draw(self, surface):
        for i in range(len(Playfield.ENTITIES)):
            Playfield.ENTITIES[i].draw(surface)
        self.hud.draw(surface)
        self.test.draw(surface)
