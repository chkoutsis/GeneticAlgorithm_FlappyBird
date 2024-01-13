import random

from config.config import *
from core.pipe import Pipe


class PipeManager():
    def __init__(self):
        self.pipe_width = width_pipes
        self.upper_pipes = []
        self.lower_pipes = []
        self.pipe_speed = pipe_velocity
        self.max_tick = pipe_to_pipe
        self.spawn_tick = self.max_tick
        self.score = 0

    def manage_pipes(self, dt):
        self.spawner(dt)
        self.manage(dt)

    def make_pipe(self):
        height_1 = random.randint(height/5, height/1.5)
        gap = random.randint(100, 150)
        height_2 = height - (height_1 + gap)

        hitbox_1 = (self.pipe_width, 0, self.pipe_width, height_1)
        hitbox_2 = (self.pipe_width,  height_1 + gap, self.pipe_width, height)

        pipe = Pipe(pygame.Vector2(width, 0), height_1, hitbox_1)
        pipe2 = Pipe(pygame.Vector2(width, height_1 + gap), height_2, hitbox_2)
        self.upper_pipes.append(pipe)
        self.lower_pipes.append(pipe2)

    def spawner(self, dt):
        if self.spawn_tick >= self.max_tick:
            self.make_pipe()
            self.spawn_tick = 0
        self.spawn_tick += dt

    def manage(self, dt):
        for pipe in self.upper_pipes[:]:
            pipe.pos.x -= self.pipe_speed * dt
            if pipe.pos.x + self.pipe_width < -100:
                removed_upper = self.upper_pipes.remove(pipe)
                del removed_upper
                self.score += 1
        for pipe in self.lower_pipes[:]:
            pipe.pos.x -= self.pipe_speed * dt
            if pipe.pos.x + self.pipe_width < -100:
                removed_lower = self.lower_pipes.remove(pipe)
                del removed_lower
