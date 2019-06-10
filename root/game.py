import pygame
from enum import Enum
from level.playfield import Playfield
from ui.menu import Menu
from utilities.color import Color
from utilities.camera import Camera
from utilities.static_camera import StaticCamera
from utilities.input import Input
from utilities.input import InputType


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

        self.setup_window(320, 240, 60, False, Orientaion.LANDSCAPE, "Pygine")
        self.setup_pixel_scene(320, 180)
        self.setup_cameras()

        self.delta_time = 0
        self.ticks = 0
        self.state = GameState.PLAYFIELD
        self.menu = Menu()
        self.playfield = Playfield()
        self.input = Input()

    def initialize_pygame(self):
        pygame.init()

    def setup_window(self, window_width=1280, window_height=720, target_fps=60, fullscreen=False, orientation=Orientaion.LANDSCAPE, title="Game"):
        self.display_width = pygame.display.Info().current_w
        self.display_height = pygame.display.Info().current_h
        self.window_width = window_width
        self.window_height = window_height
        self.target_fps = target_fps
        self.orientation = orientation
        self.fullscreen = fullscreen

        if self.fullscreen:
            self.window = pygame.display.set_mode(
                (self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))

        pygame.display.set_caption(title)

    def setup_pixel_scene(self, game_width=320, game_height=180):
        self.game_width = game_width
        self.game_height = game_height

    def setup_cameras(self):
        if self.orientation == Orientaion.LANDSCAPE:
            if self.fullscreen:
                self.scale = self.display_height / self.game_height
                if self.game_width * self.scale > self.display_width:
                    self.scale = self.display_width / self.game_width
            else:
                self.scale = self.window_height / self.game_height
                if self.game_width * self.scale > self.window_width:
                    self.scale = self.window_width / self.game_width

        elif self.orientation == Orientaion.PORTRAIT:
            if self.fullscreen:
                self.scale = self.display_width / self.game_width
                if self.game_height * self.scale > self.display_height:
                    self.scale = self.display_height / self.game_height
            else:
                self.scale = self.window_width / self.game_width
                if self.game_height * self.scale > self.window_height:
                    self.scale = self.window_height / self.game_height

        StaticCamera.initialize(
            (self.game_width, self.game_height), self.scale)
        Camera.initialize((self.game_width, self.game_height), self.scale)

        if self.fullscreen:
            if self.game_width * self.scale < self.display_width:
                StaticCamera.apply_horizontal_letterbox(
                    (self.display_width - self.game_width * self.scale) / 2)
            if self.game_height * self.scale < self.display_height:
                StaticCamera.apply_vertical_letterbox(
                    (self.display_height - self.game_height * self.scale) / 2)
        else:
            if self.game_width * self.scale < self.window_width:
                StaticCamera.apply_horizontal_letterbox(
                    (self.window_width - self.game_width * self.scale) / 2)
            if self.game_height * self.scale < self.window_height:
                StaticCamera.apply_vertical_letterbox(
                    (self.window_height - self.game_height * self.scale) / 2)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window = pygame.display.set_mode(
                (self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))

        self.setup_cameras()

    def calculate_delta_time(self):
        pygame.time.Clock().tick(self.target_fps)
        self.delta_time = (pygame.time.get_ticks() - self.ticks) / 1000.0
        self.ticks = pygame.time.get_ticks()

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.QUIT):
            self.state = GameState.NONE
        if self.input.pressing(InputType.TOGGLE_FULLSCREEN):
            self.toggle_fullscreen()

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.NONE

    def clear_screen(self, window, color=Color.BLACK):
        "Clear the screen in preparation for the next draw call."
        window.fill(color)

    def update(self):
        self.calculate_delta_time()
        self.update_input()

        if self.state == GameState.MENU:
            self.menu.update(self.delta_time)

        elif self.state == GameState.PLAYFIELD:
            self.playfield.update(self.delta_time)

        self.update_events()

    def draw(self):
        self.clear_screen(self.window, Color.BLUE)

        if self.state == GameState.MENU:
            self.menu.draw(self.window)

        elif self.state == GameState.PLAYFIELD:
            self.playfield.draw(self.window)

        StaticCamera.draw(self.window)

        pygame.display.update()

    def run(self):
        while self.state != GameState.NONE:
            self.update()
            self.draw()