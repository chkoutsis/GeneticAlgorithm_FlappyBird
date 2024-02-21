import sys

import pygame

from config.config import (FPS, HEIGHT, N_POPULATION_BIRD, WIDTH,
                           background_image, bird_image)
from core.pipe_manager import PipeManager
from genetic_algorithms.genetic_algorithm import bird_population, reproduction
from interface.interface import game_player, generation_text
from setup.setup import initialize_game


def run(game_display_f, background_f, clock_f):
    """
    Run the main game loop.

    Parameters:
    - game_display_f (pygame.Surface): The game display surface.
    - background_f (pygame.Surface): Scaled background image.
    - clock_f (pygame.time.Clock): Clock object for controlling the frame rate.
    """
    population = bird_population(N_POPULATION_BIRD)
    generation_flag = True
    generation_it = 1
    while generation_flag:
        number = N_POPULATION_BIRD
        pipe_manager = PipeManager()
        run_game = True
        dt = 0
        pipe_manager.manage_pipes(dt)
        dt = clock_f.tick(FPS)
        while run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            game_display_f.blit(background_f, (0, 0))
            for bird in population:
                number = game_player(bird, pipe_manager,
                                     game_display_f, number)
            pipe_manager.manage_pipes(dt)
            generation_text(generation_it, game_display_f)
            pygame.display.update()
            dt = clock_f.tick(FPS)
            if number == 0:
                run_game = False
                generation_it += 1
        population = reproduction(population)


if __name__ == '__main__':
    game_display, background, clock = initialize_game(
        WIDTH, HEIGHT, background_image, bird_image)
    run(game_display, background, clock)
