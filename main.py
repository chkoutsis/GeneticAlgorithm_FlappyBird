import os
import sys

import pygame

from config.config import (background_image, bird_image, fps, height,
                           n_population_bird, width)
from core.pipe_manager import PipeManager
from genetic_algorithm.genetic_algorithm import bird_population, reproduction
from interface.interface import game_player, generation_text
from setup.setup import initialize_game

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def run(game_display_f, background_f, clock_f):
    population = bird_population(n_population_bird)
    generation_flag = True
    generation_it = 1
    while generation_flag:
        number = n_population_bird
        pipe_manager = PipeManager()
        run_game = True
        dt = 0
        pipe_manager.manage_pipes(dt)
        dt = clock_f.tick(fps)
        while run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            game_display_f.blit(background_f, (0, 0))
            for bird in population:
                number = game_player(bird, game_display_f,
                                     pipe_manager, number)
            pipe_manager.manage_pipes(dt)
            generation_text(generation_it, game_display_f)
            pygame.display.update()
            dt = clock_f.tick(fps)
            if number == 0:
                run_game = False
                generation_it += 1
        population = reproduction(population)


if __name__ == '__main__':
    game_display, background, clock = initialize_game(
        width, height, background_image, bird_image)
    run(game_display, background, clock)
