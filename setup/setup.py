import pygame


def initialize_game(width, height, background_image, bird_image):
    """
    Initialize the game environment.

    Parameters:
    - width (int): Width of the game display.
    - height (int): Height of the game display.
    - background_image (pygame.Surface): Background image for the game.
    - bird_image (pygame.Surface): Icon for the bird.

    Returns:
    - game_display (pygame.Surface): The game display surface.
    - background (pygame.Surface): Scaled background image.
    - clock (pygame.time.Clock): Clock object for controlling the frame rate.
    """
    pygame.init()
    game_display = pygame.display.set_mode((width, height))
    background = pygame.transform.scale(background_image, (width, height))
    pygame.display.set_icon(bird_image)
    pygame.display.set_caption('Flappy Bird')
    clock = pygame.time.Clock()

    return game_display, background, clock
