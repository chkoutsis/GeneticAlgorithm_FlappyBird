'''
Contains configuration variables and assets.

Variables:
- path (str): The current working directory.
- bird_image (pygame.Surface): Image of the bird for the game.
- pipe_image (pygame.Surface): Image of the pipes for the game.
- background_image (pygame.Surface): Image of the background for the game.
- SCORE_COLORS (str): Color code for displaying the score in the game.
- WIDTH (int): Width of the game window.
- HEIGHT (int): Height of the game window.
- WIDTH_BIRD (float): Width of the bird sprite.
- WIDTH_PIPES (int): Width of the pipes in the game.
- PIPE_VELOCITY (float): Velocity of the pipes in the game.
- PIPE_TO_PIPE (int): Distance between consecutive pipes.
- GRAVITY (float): Gravity affecting the bird's vertical motion.
- BIRD_VELOCITY_Y (float): Vertical velocity of the bird.
- BIRD_MAX_VELOCITY_Y (float): Maximum vertical velocity of the bird.
- MUTATION_THRESHOLD (float): Threshold for mutation during genetic algorithm.
- N_POPULATION_BIRD (int): Number of birds in each population.
- FPS (int): Frames per second for the game.
'''
import os

import pygame

path = os.getcwd()
bird_image = pygame.image.load(path + '\\assets\\bird.png')
pipe_image = pygame.image.load(path + '\\assets\\red_pipe.png')
background_image = pygame.image.load(path + '\\assets\\background.png')

SCORE_COLORS = '#1C3C7B'
WIDTH = 800
HEIGHT = 600
WIDTH_BIRD = WIDTH / 10
WIDTH_PIPES = 50
PIPE_VELOCITY = .3
PIPE_TO_PIPE = 1600
GRAVITY = .9
BIRD_VELOCOCITY_Y = -10
BIRD_MAX_VELOCOCITY_Y = 5
MUTATION_THRESHOLD = 0.3
N_POPULATION_BIRD = 10
FPS = 60
