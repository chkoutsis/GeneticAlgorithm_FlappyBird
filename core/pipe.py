class Pipe:
    """
    Pipe class for representing pipes in the Flappy Bird game.
    """

    def __init__(self, pos, height, hitbox):
        """
        Initialize a new Pipe object.

        Parameters:
        - pos (Vector2): The position of the pipe.
        - hitbox_pos: The x-coordinate of the pipe's hitbox position.
        - height (float): The height of the pipe.
        - hitbox (Rect): The hitbox of the pipe.
        """
        self.pos = pos
        self.hitbox_pos = pos.x
        self.height = height
        self.hitbox = hitbox
