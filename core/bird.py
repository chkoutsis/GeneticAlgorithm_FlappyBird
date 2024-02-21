from config.config import (BIRD_MAX_VELOCOCITY_Y, BIRD_VELOCOCITY_Y, GRAVITY,
                           HEIGHT, WIDTH_BIRD)
from genetic_algorithms.model import dna

import random


class Bird:
    """
    Bird class for representing the player-controlled bird.

    Methods:
    - jump(): Make the bird jump by adjusting its vertical velocity.
    - move(): Update the bird's position based on its current velocity.
    """

    def __init__(self):
        """
        Initialize a new Bird object.

        Default attributes:
        - x (float): Initial x-coordinate of the bird, set to the width of the bird sprite.
        - y (float): Initial y-coordinate of the bird, set to the height of the bird sprite.
        - move_x (int): Initial horizontal movement of the bird.
        - move_y (int): Initial vertical movement of the bird.
        - dna (DNA): DNA object representing the genetic code of the bird.
        - final_score (int): The final score achieved by the bird in the game.
        - is_alive (bool): Flag indicating whether the bird is alive or not.
        """
        self.x = WIDTH_BIRD
        self.y = random.uniform(0, HEIGHT)  # HEIGHT_BIRD
        self.move_x = 0
        self.move_y = 0
        self.dna = dna()
        self.final_score = 0
        self.is_alive = True

    def jump(self):
        """
        Make the bird jump by adjusting its vertical velocity.
        """
        self.move_y = BIRD_VELOCOCITY_Y
        self.x += self.move_x * GRAVITY
        self.y += BIRD_VELOCOCITY_Y

    def move(self):
        """
        Update the bird's position based on its current velocity.
        """
        self.move_y = BIRD_MAX_VELOCOCITY_Y
        self.x += self.move_x * GRAVITY
        self.y += self.move_y
