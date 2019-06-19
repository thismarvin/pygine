from pygame import Rect
from pygine.entities import *
from pygine.maths import Vector2
from pygine.transitions import Pinhole, PinholeType
from pygine.utilities import Camera, Input, InputType
from enum import IntEnum


class SceneType(IntEnum):
    NONE = 0
    EXAMPLE = 1


class Scene(object):
    def __init__(self):
        self.next_scene = SceneType.NONE
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.bounds = Rect(0, 0, Camera.BOUNDS.width, Camera.BOUNDS.height)
        self.entities = []
        self.input = Input()
        self.transition = None

    def reset(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the reset() method")

    def update_transition(self, delta_time):
        self.transition.update(delta_time)

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.RESET):
            self.reset()

    def update_entities(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the update_entities(delta_time) method")

    def update_camera(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the update_camera() method")

    def update(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the update(delta_time) method")

    def draw(self, surface):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the draw(surface) method")


class SceneManager():
    def __init__(self, scene_type):
        self.create_scene(scene_type)
        self.scene.reset()

    def create_scene(self, scene_type):
        if scene_type == SceneType.EXAMPLE:
            self.scene = Example()

    def update(self, delta_time):
        self.scene.update(delta_time)

    def draw(self, surface):
        self.scene.draw(surface)


class Example(Scene):
    def __init__(self):
        super(Example, self).__init__()

    def reset(self):
        self.player = Player(
            Camera.BOUNDS.width / 2 + 16,
            Camera.BOUNDS.height / 2 - 8
        )
        self.entities = [
            self.player,
            Block(Camera.BOUNDS.width / 2 - 8, Camera.BOUNDS.height / 2)
        ]
        self.transition = Pinhole(PinholeType.OPEN)

    def update_camera(self):
        self.camera_location = Vector2(
            self.player.x + self.player.width / 2 - self.camera.BOUNDS.width / 2,
            self.player.y + self.player.height / 2 - self.camera.BOUNDS.height / 2
        )
        self.camera.update(self.camera_location)

    def update_entities(self, delta_time):
        for i in range(len(self.entities)-1, -1, -1):
            if isinstance(self.entities[i], Kinetic):
                self.entities[i].update(delta_time, self.entities)
            else:
                self.entities[i].update(delta_time)
        self.entities.sort(key=lambda e: e.y + e.height)

    def update(self, delta_time):
        self.update_transition(delta_time)
        self.update_input()
        self.update_entities(delta_time)
        self.update_camera()

    def draw(self, surface):
        for e in self.entities:
            e.draw(surface)
        self.transition.draw(surface)
