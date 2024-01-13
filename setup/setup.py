import pygame


def initialize_game(width, height, background_image, bird_image):
    pygame.init()
    game_display = pygame.display.set_mode((width, height))
    background = pygame.transform.scale(background_image, (width, height))
    pygame.display.set_icon(bird_image)
    pygame.display.set_caption('Flappy Bird')
    clock = pygame.time.Clock()

    return game_display, background, clock
