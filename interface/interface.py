import pygame

from config.config import (bird_image, height, pipe_image, score_colors, width,
                           width_pipes)


def collision(pipe_manager, game_display, bird_hitbox, bird, number):
    display_upper_hitboxes = []
    display_lower_hitboxes = []
    n = number

    # Checks if bird is into the limits
    if bird_hitbox.y > height or bird_hitbox.y <= 0:
        player_over(bird, pipe_manager)
        n = number - 1

    # Checks if bird hits the upper pipe
    for pipe in pipe_manager.upper_pipes:
        display_upper_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_upper_hitboxes[0].hitbox)
        pipe_display = game_display.blit(pygame.transform.rotate(
            pygame.transform.scale(pipe_image, (width_pipes, pipe.height)),
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
            pipe_image, (width_pipes, pipe.height))), pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display):
                player_over(bird, pipe_manager)
                n = number - 1
    return n


def game_player(bird, game_display, pipe_manager, number):
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
        n = collision(pipe_manager, game_display, bird.hitbox, bird, number)

        # Score
        scoreboard(pipe_manager, game_display)
        return n
    return number


def player_over(bird, pipe_manager):
    bird.final_score = pipe_manager.score
    bird.is_alive = False


def scoreboard(pipe_manager, game_display):
    font_score = pygame.font.Font(None, 72)
    text_score = font_score.render(str(pipe_manager.score), 2, score_colors)
    game_display.blit(text_score, (width/2.2, 30))


def generation_text(generation_it, game_display):
    font_score = pygame.font.Font(None, 72)
    text = 'Generation ' + str(generation_it)
    text_generation = font_score.render(text, 2, score_colors)
    game_display.blit(text_generation, (width - 350, height - 150))


def interface_inputs(bird, pipe_manager):
    upper_pipe_display = pygame.Rect(pipe_manager.upper_pipes[0].hitbox)
    lower_pipe_display = pygame.Rect(pipe_manager.lower_pipes[0].hitbox)
    inputs = [pipe_manager.upper_pipes[0].pos[0] - bird.hitbox.width,
              bird.hitbox.y, height - bird.hitbox.y,
              lower_pipe_display.y - upper_pipe_display.height,
              upper_pipe_display.height, height - lower_pipe_display.y]
    return inputs
