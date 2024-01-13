from config.config import *
from genetic_algorithm.model import DNA


class Bird:
    def __init__(self):
        self.x = width_bird
        self.y = height_bird
        self.dna = DNA()
        self.final_score = 0
        self.is_alive = True

    def jump(self):
        self.move_x = 0
        self.move_y = bird_velocity_y
        self.x += self.move_x * gravity
        self.y += bird_velocity_y

    def move(self):
        self.move_x = 0
        self.move_y = bird_max_velocity_y
        self.x += self.move_x * gravity
        self.y += self.move_y
