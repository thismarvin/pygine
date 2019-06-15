from utilities.vector import Vector2
from utilities.camera import Camera
from utilities.camera import StaticCamera
from utilities.camera import CameraType


class PyObject(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = Vector2(self.x, self.y)

    def scaled_location(self, camera_type=CameraType.DYNAMIC):
        if camera_type == CameraType.DYNAMIC:
            return Vector2(self.x * Camera.SCALE - Camera.TOP_LEFT.x, self.y * Camera.SCALE - Camera.TOP_LEFT.y)
        if camera_type == CameraType.STATIC:
            return Vector2(self.x * StaticCamera.SCALE - StaticCamera.TOP_LEFT.x, self.y * StaticCamera.SCALE - StaticCamera.TOP_LEFT.y)

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.location = Vector2(self.x, self.y)
