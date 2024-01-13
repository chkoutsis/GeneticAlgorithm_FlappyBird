import random

import pygame

from config.config import (HEIGHT, PIPE_TO_PIPE, PIPE_VELOCITY, WIDTH,
                           WIDTH_PIPES)
from core.pipe import Pipe


class PipeManager():
    """
    PipeManager class for managing pipes in the Flappy Bird game.

    Methods:
    - manage_pipes(dt): Update the positions of existing pipes based on time.
    - make_pipe(): Create a new pair of pipes.
    - spawner(dt): Control the spawning of new pipes based on time.
    - manage(dt): Overall pipe management function, updating positions
                  and spawning new pipes.
    """

    def __init__(self):
        """
        Initialize a new PipeManager object.

        Default attributes:
        - pipe_width: Width of the pipes.
        - upper_pipes: List to store the upper pipes.
        - lower_pipes: List to store the lower pipes.
        - pipe_speed: Velocity of the pipes.
        - max_tick: Maximum time between pipe spawns.
        - spawn_tick: Current time between pipe spawns.
        - score: Current score in the game.
        """
        self.pipe_width = WIDTH_PIPES
        self.upper_pipes = []
        self.lower_pipes = []
        self.pipe_speed = PIPE_VELOCITY
        self.max_tick = PIPE_TO_PIPE
        self.spawn_tick = self.max_tick
        self.score = 0

    def manage_pipes(self, dt):
        """
        Manage the pipes by controlling pipe spawning
        and overall pipe management.

        Parameters:
        - dt (float): Time elapsed since the last update.
        """
        self.spawner(dt)
        self.manage(dt)

    def make_pipe(self):
        """
        Create a new pair of pipes.
        """
        height_1 = random.randint(HEIGHT/5, HEIGHT/1.5)
        gap = random.randint(100, 150)
        height_2 = HEIGHT - (height_1 + gap)

        hitbox_1 = (self.pipe_width, 0, self.pipe_width, height_1)
        hitbox_2 = (self.pipe_width,  height_1 + gap, self.pipe_width, HEIGHT)

        pipe = Pipe(pygame.Vector2(WIDTH, 0), height_1, hitbox_1)
        pipe2 = Pipe(pygame.Vector2(WIDTH, height_1 + gap), height_2, hitbox_2)
        self.upper_pipes.append(pipe)
        self.lower_pipes.append(pipe2)

    def spawner(self, dt):
        """
        Control the spawning of new pipes based on time.

        Parameters:
        - dt (float): Time elapsed since the last update.
        """
        if self.spawn_tick >= self.max_tick:
            self.make_pipe()
            self.spawn_tick = 0
        self.spawn_tick += dt

    def manage(self, dt):
        """
        Update the positions of existing pipes and remove pipes that are out of the screen.

        Parameters:
        - dt (float): Time elapsed since the last update.
        """
        for pipe in self.upper_pipes[:]:
            pipe.pos.x -= self.pipe_speed * dt
            if pipe.pos.x + self.pipe_width < -100:
                self.upper_pipes.remove(pipe)
                self.score += 1
        for pipe in self.lower_pipes[:]:
            pipe.pos.x -= self.pipe_speed * dt
            if pipe.pos.x + self.pipe_width < -100:
                self.lower_pipes.remove(pipe)
