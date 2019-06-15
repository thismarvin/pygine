from utilities.transitions import Pinhole
from utilities.transitions import PinholeType
from utilities.camera import CameraType


class HUD():
    def __init__(self):
        self.pinhole = Pinhole(PinholeType.OPEN)

    def reset(self):
        self.pinhole = Pinhole(PinholeType.OPEN)

    def update(self, delta_time):
        self.pinhole.update(delta_time)

    def draw(self, surface):
        self.pinhole.draw(surface)