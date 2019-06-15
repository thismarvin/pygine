from entities.kinetic import Kinetic
from entities.kinetic import Direction
from entities.geometry.rectangle import Rectangle
from resources.sprite import Sprite
from resources.sprite import Type
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera
from utilities.color import Color


class Player(Kinetic):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height, 50)
        self.rectangle = Rectangle(self.x, self.y, self.width, self.height)
        self.input = Input()

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.rectangle.set_location(self.x, self.y)

    def move(self, direction=Direction.NONE):
        self.facing = direction
        if self.facing == Direction.UP:
            self.set_location(self.x, self.y - self.move_speed)
            self.velocity.y = -1
        if self.facing == Direction.DOWN:
            self.set_location(self.x, self.y + self.move_speed)
            self.velocity.y = 1
        if self.facing == Direction.LEFT:
            self.set_location(self.x - self.move_speed, self.y)
            self.velocity.x = -1
        if self.facing == Direction.RIGHT:
            self.set_location(self.x + self.move_speed, self.y)
            self.velocity.x = 1

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.UP):
            self.move(Direction.UP)
        if self.input.pressing(InputType.DOWN):
            self.move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT):
            self.move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self.move(Direction.RIGHT)

    def rectanlge_collision_logic(self, entity):
        # Bottom
        if self.collision_rectangles[0].bounds.colliderect(entity.bounds) and self.velocity.y < 0:
            self.set_location(self.x, entity.bounds.bottom)
        # Top
        if self.collision_rectangles[1].bounds.colliderect(entity.bounds) and self.velocity.y > 0:
            self.set_location(self.x, entity.bounds.top - self.bounds.height)
        # Right
        if self.collision_rectangles[2].bounds.colliderect(entity.bounds) and self.velocity.x < 0:
            self.set_location(entity.bounds.right, self.y)
        # Left
        if self.collision_rectangles[3].bounds.colliderect(entity.bounds) and self.velocity.x > 0:
            self.set_location(entity.bounds.left - self.bounds.width, self.y)

    def collision(self):
        from level.playfield import Playfield
        for e in Playfield.ENTITIES:
            if isinstance(e, Rectangle):
                self.rectanlge_collision_logic(e)

    def update(self, delta_time):
        self.calculate_scaled_speed(delta_time)
        self.update_input()
        self.update_collision_rectangles()
        self.collision()

    def draw(self, surface):
        self.rectangle.draw(surface)

        from root.game import Game
        if Game.DEBUG_MODE:
            for r in self.collision_rectangles:
                r.draw(surface)
