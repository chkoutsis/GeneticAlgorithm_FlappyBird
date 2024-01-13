import os

import pygame

path = os.getcwd()
bird_image = pygame.image.load(path + '\\assets\\bird.png')
pipe_image = pygame.image.load(path + '\\assets\\red_pipe.png')
background_image = pygame.image.load(path + '\\assets\\background.png')

score_colors = '#1C3C7B'
width = 800
height = 600
width_bird = width / 10
height_bird = height / 2
width_pipes = 50
pipe_velocity = .3
pipe_to_pipe = 1300
gravity = .2
bird_velocity_y = -10
bird_max_velocity_y = 5
mutation_threshold = 0.3
n_population_bird = 8
fps = 60