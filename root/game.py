import pygame
from enum import Enum
from level.playfield import Playfield
from ui.menu import Menu
from utilities.color import Color
from utilities.camera import Camera


class GameState(Enum):
    NONE = 0
    MENU = 1
    PLAYFIELD = 2


class Orientaion(Enum):
    LANDSCAPE = 0
    PORTRAIT = 1


class Game:
    "A modest game engine used to streamline the development of a game made using pygame"

    def __init__(self):
        self.initialize_pygame()
        self.setup_window(1280, 720, Orientaion.LANDSCAPE, "Pygine")
        self.setup_pixel_scene(320, 180)
        self.camera = Camera(
            (0, 0), (self.game_width, self.game_height), self.scale)
        self.static_camera = Camera(
            (0, 0), (self.game_width, self.game_height), self.scale)

        self.state = GameState.PLAYFIELD
        self.target_fps = 60
        self.ticks = 0
        self.delta_time = 0
        self.menu = Menu(self.static_camera)
        self.playfield = Playfield(self.camera)

    def initialize_pygame(self):
        pygame.init()

    def setup_window(self, display_width=1280, display_height=720, orientation=Orientaion.LANDSCAPE, title="Game"):
        self.display_width = display_width
        self.display_height = display_height
        self.window = pygame.display.set_mode(
            (self.display_width, self.display_height))
        self.orientation = orientation
        pygame.display.set_caption(title)

    def setup_pixel_scene(self, game_width=320, game_height=180):
        self.game_width = game_width
        self.game_height = game_height

        if self.orientation == Orientaion.LANDSCAPE:
            self.scale = self.display_height / self.game_height
        elif self.orientation == Orientaion.PORTRAIT:
            self.scale = self.display_width / self.game_width

    def calculate_delta_time(self):
        pygame.time.Clock().tick(self.target_fps)
        self.delta_time = (pygame.time.get_ticks() - self.ticks) / 1000.0
        self.ticks = pygame.time.get_ticks()

    def check_for_end_condition(self):
        "Used to end the game loop and consequently exit the program."
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.NONE

    def clear_screen(self, window, color=Color.BLACK):
        "Clear the screen in preparation for the next draw call."
        window.fill(color)

    def update(self):
        self.calculate_delta_time()

        if self.state == GameState.MENU:
            self.menu.update(self.delta_time)

        elif self.state == GameState.PLAYFIELD:
            self.playfield.update(self.delta_time)

        self.check_for_end_condition()

    def draw(self):
        self.clear_screen(self.window, Color.BLACK)

        if self.state == GameState.MENU:
            self.menu.draw(self.window)

        elif self.state == GameState.PLAYFIELD:
            self.playfield.draw(self.window)

        pygame.display.update()

    def run(self):
        while self.state != GameState.NONE:
            self.update()
            self.draw()
