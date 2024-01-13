import pygame

from config.config import (HEIGHT, SCORE_COLORS, WIDTH, WIDTH_PIPES,
                           bird_image, pipe_image)


def collision(pipe_manager, bird, bird_hitbox, game_display, number):
    """
    Check for collision between the bird and pipes.

    Parameters:
    - pipe_manager (PipeManager): PipeManager object managing the pipes.
    - bird (Bird): Bird object.
    - bird_hitbox (pygame.Rect): Rect representing the hitbox of the bird.
    - game_display (pygame.Surface): The game display surface.
    - number (int): The number of existing bird objects.

    Returns:
    - n (int): The result of existing bird objects
                after applying collision logic.
    """
    display_upper_hitboxes = []
    display_lower_hitboxes = []
    n = number

    # Checks if the bird collides within the limits
    if bird_hitbox.y > HEIGHT or bird_hitbox.y <= 0:
        player_over(bird, pipe_manager)
        n = number - 1

    # Checks if bird hits the upper pipe
    for pipe in pipe_manager.upper_pipes:
        display_upper_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_upper_hitboxes[0].hitbox)
        pipe_display = game_display.blit(pygame.transform.rotate(
            pygame.transform.scale(pipe_image, (WIDTH_PIPES, pipe.height)),
            180), pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display):
                player_over(bird, pipe_manager)
                n = number - 1

    # Checks if bird hits the lower pipe
    for pipe in pipe_manager.lower_pipes:
        display_lower_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_lower_hitboxes[0].hitbox)
        pipe_display = game_display.blit((pygame.transform.scale(
            pipe_image, (WIDTH_PIPES, pipe.height))), pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display):
                player_over(bird, pipe_manager)
                n = number - 1
    return n


def game_player(bird, pipe_manager, game_display, number):
    """
    Player logic for the game.

    Parameters:
    - bird (Bird): Bird object.
    - pipe_manager (PipeManager): PipeManager object managing the pipes.
    - game_display (pygame.Surface): The game display surface.
    - number (int): The number of existing bird objects.

    Returns:
    - number (int): The result of existing bird objects
                    after applying player logic.
    """
    # Bird
    if bird.is_alive:
        bird.hitbox = game_display.blit(bird_image, (bird.x-20, bird.y-15))
        observations = interface_inputs(bird, pipe_manager)
        prediction_move = bird.dna.predict([observations])
        if prediction_move > 0:
            bird.jump()
        else:
            bird.move()

        # Checks for collisions
        n = collision(pipe_manager, bird, bird.hitbox, game_display, number)

        # Score
        scoreboard(pipe_manager, game_display)
        return n
    return number


def player_over(bird, pipe_manager):
    """
    Logic to handle game over for the player.

    Parameters:
    - bird (Bird): Bird object.
    - pipe_manager (PipeManager): PipeManager object managing the pipes.
    """
    bird.final_score = pipe_manager.score
    bird.is_alive = False


def scoreboard(pipe_manager, game_display):
    """
    Display the current score on the game display.

    Parameters:
    - pipe_manager (PipeManager): PipeManager object managing the pipes.
    - game_display (pygame.Surface): The game display surface.
    """
    font_score = pygame.font.Font(None, 72)
    text_score = font_score.render(str(pipe_manager.score), 2, SCORE_COLORS)
    game_display.blit(text_score, (WIDTH/2.2, 30))


def generation_text(generation_it, game_display):
    """
    Display the current generation information on the game display.

    Parameters:
    - generation_it (int): Current generation number.
    - game_display (pygame.Surface): The game display surface.
    """
    font_score = pygame.font.Font(None, 72)
    text = 'Generation ' + str(generation_it)
    text_generation = font_score.render(text, 2, SCORE_COLORS)
    game_display.blit(text_generation, (WIDTH - 350, HEIGHT - 150))


def interface_inputs(bird, pipe_manager):
    """
    Generate input values for the neural network based on game state.

    Parameters:
    - bird (Bird): Bird object.
    - pipe_manager (PipeManager): PipeManager object managing the pipes.

    Returns:
    - inputs (list): List of input values for the neural network.
    """
    upper_pipe_display = pygame.Rect(pipe_manager.upper_pipes[0].hitbox)
    lower_pipe_display = pygame.Rect(pipe_manager.lower_pipes[0].hitbox)
    inputs = [pipe_manager.upper_pipes[0].pos[0] - bird.hitbox.width,
              bird.hitbox.y, HEIGHT - bird.hitbox.y,
              lower_pipe_display.y - upper_pipe_display.height,
              upper_pipe_display.height, HEIGHT - lower_pipe_display.y]
    return inputs
