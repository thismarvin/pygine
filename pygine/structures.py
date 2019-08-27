from pygame import Rect
from pygine.draw import draw_rectangle
from pygine.utilities import CameraType, Color


class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity

        self.divided = False
        self.insertion_index = 0
        self.objects = [None] * self.capacity

        self.topLeft = None
        self.topRight = None
        self.bottomRight = None
        self.bottomLeft = None

    def insert(self, pygine_object):
        if not pygine_object.bounds.colliderect(self.boundary):
            return False

        if self.insertion_index < self.capacity:
            self.objects[self.insertion_index] = pygine_object
            self.insertion_index += 1
            return True
        else:
            if not self.divided:
                self.__subdivide()

            if (
                self.topLeft.insert(pygine_object) or
                self.topRight.insert(pygine_object) or
                self.bottomRight.insert(pygine_object) or
                self.bottomLeft.insert(pygine_object)
            ):
                return True

        return False

    def query(self, area):
        result = []

        if not area.colliderect(self.boundary):
            return result

        for i in range(len(self.objects)):
            if self.objects[i] == None:
                continue

            if area.colliderect(self.objects[i].bounds):
                result.append(self.objects[i])

        if not self.divided:
            return result

        result.extend(self.topLeft.query(area))
        result.extend(self.topRight.query(area))
        result.extend(self.bottomRight.query(area))
        result.extend(self.bottomLeft.query(area))

        return result

    def clear(self):
        if self.divided:
            self.topLeft.clear()
            self.topRight.clear()
            self.bottomRight.clear()
            self.bottomLeft.clear()

            self.topLeft = None
            self.topRight = None
            self.bottomRight = None
            self.bottomLeft = None

        self.divided = False
        self.insertion_index = 0
        self.objects = [None] * self.capacity

    def __subdivide(self):
        self.divided = True
        self.topLeft = QuadTree(
            Rect(
                self.boundary.x,
                self.boundary.y,
                self.boundary.width / 2,
                self.boundary.height / 2
            ),
            self.capacity
        )
        self.topRight = QuadTree(
            Rect(
                self.boundary.x + self.boundary.width / 2,
                self.boundary.y,
                self.boundary.width / 2,
                self.boundary.height / 2
            ),
            self.capacity
        )
        self.bottomRight = QuadTree(
            Rect(
                self.boundary.x + self.boundary.width / 2,
                self.boundary.y + self.boundary.height / 2,
                self.boundary.width / 2,
                self.boundary.height / 2
            ),
            self.capacity
        )
        self.bottomLeft = QuadTree(
            Rect(
                self.boundary.x,
                self.boundary.y + self.boundary.height / 2,
                self.boundary.width / 2,
                self.boundary.height / 2
            ),
            self.capacity
        )

    def draw(self, surface):
        draw_rectangle(
            surface,
            self.boundary,
            CameraType.DYNAMIC,
            Color.BLACK,
            1
        )

        if self.divided:
            self.topLeft.draw(surface)
            self.topRight.draw(surface)
            self.bottomRight.draw(surface)
            self.bottomLeft.draw(surface)
