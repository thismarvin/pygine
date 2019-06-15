import pygame


class Timer:
    def __init__(self, length=0, started=False):
        self.length = length
        self.reset()
        self.started = started

    def start(self):
        self.started = True
        self.starting_ticks = pygame.time.get_ticks()

    def reset(self):
        self.started = False
        self.done = False
        self.starting_ticks = 0
        self.ticks = 0

    def update(self):
        if self.started and not self.done:
            self.ticks = pygame.time.get_ticks()
            if self.ticks - self.starting_ticks >= self.length:
                self.done = True
