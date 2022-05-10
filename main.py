import pygame 
import random
import sys
import os

PATH = os.getcwd()
BIRD_IMAGE = pygame.image.load(PATH + '\\assets\\bird.png')
PIPE_IMAGE = pygame.image.load(PATH + '\\assets\\red_pipe.png')
BACKGROUND_IMAGE = pygame.image.load(PATH + '\\assets\\background.png')

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCORE_COLORS = '#1C3C7B'
WIDTH = 800
HEIGHT = 600
WIDTH_BIRD = WIDTH / 10
HEIGHT_BIRD = HEIGHT / 2
WIDTH_PIPES = 50
PIPE_VELOCITY = .3
PIPE2PIPE = 1300
GRAVITY = .2
FPS = 60
BIRD_VELOCITY_Y = -10  
BIRD_MAX_VELOCITY_Y = 5   

pygame.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
pygame.display.set_icon(BIRD_IMAGE)
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird: 
    def __init__(self):
        self.x = WIDTH_BIRD
        self.y =  HEIGHT_BIRD

    def move(self):
        self.move_x = 0 
        self.move_y = BIRD_MAX_VELOCITY_Y
        self.x += self.move_x * GRAVITY
        self.y += self.move_y 

class Pipe:
    def __init__(self, pos, height, hitbox):
        self.pos = pos
        self.hitbox_pos = pos
        self.height = height
        self.hitbox = hitbox
        

class Pipe_Manager():
    def __init__(self):
        self.pipe_width = WIDTH_PIPES 
        self.upper_pipes = []
        self.lower_pipes = []
        self.pipe_speed = PIPE_VELOCITY
        self.max_tick = PIPE2PIPE
        self.spawn_tick = self.max_tick
        self.score = 0

    def manage_pipes(self, dt):
        self.spawner(dt)
        self.manage(dt)

    def make_pipe(self):
        height = random.randint(HEIGHT/5, HEIGHT/1.5)
        gap = random.randint(100, 150)
        height_2 = HEIGHT - (height + gap)
        hitbox_1 = (self.pipe_width, 0, self.pipe_width, height) 
        hitbox_2 = (self.pipe_width,  height + gap, self.pipe_width, HEIGHT) 
        pipe = Pipe(pygame.Vector2(WIDTH, 0), height, hitbox_1)
        pipe2 = Pipe(pygame.Vector2(WIDTH, height + gap), height_2, hitbox_2)
        self.upper_pipes.append(pipe)
        self.lower_pipes.append(pipe2)

    def spawner(self, dt):
        if self.spawn_tick >= self.max_tick:
            self.make_pipe()
            self.spawn_tick = 0
        self.spawn_tick += dt

    def manage(self, dt):
        for pipe in self.upper_pipes[:]: 
            pipe.score_counted = True
            pipe.pos.x -= self.pipe_speed * dt
            if pipe.pos.x + self.pipe_width < 0: 
                removed_upper = self.upper_pipes.remove(pipe)    
                del removed_upper 
                self.score +=1
        for pipe in self.lower_pipes[:]: 
            pipe.pos.x -= self.pipe_speed * dt      
            if pipe.pos.x + self.pipe_width < 0: 
                removed_lower = self.lower_pipes.remove(pipe) 
                del removed_lower 

def collision(pipe_manager, bird_hitbox):
    display_upper_hitboxes = []
    display_lower_hitboxes = []
    #Check if bird is into the limits
    if bird_hitbox.y > HEIGHT or bird_hitbox.y < 0: game_over()
    #Check if bird hits the upper pipe
    for pipe in pipe_manager.upper_pipes:
        display_upper_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_upper_hitboxes[0].hitbox)
        pipe_display = game_display.blit(pygame.transform.rotate(pygame.transform.scale(PIPE_IMAGE, (WIDTH_PIPES, pipe.height)), 180), pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display): game_over()
    #Check if bird hits the lower pipe
    for pipe in pipe_manager.lower_pipes:
        display_lower_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_lower_hitboxes[0].hitbox)
        pipe_display = game_display.blit((pygame.transform.scale(PIPE_IMAGE, (WIDTH_PIPES, pipe.height))), pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display): game_over()


def scoreboard(pipe_manager):
    font_score = pygame.font.Font(None, 72)
    text_score = font_score.render(str(pipe_manager.score), 2, SCORE_COLORS)
    game_display.blit(text_score, (WIDTH/2.2, 30))
         
        
def player(bird, pipe_manager):
    #Bird
    bird.hitbox = game_display.blit(BIRD_IMAGE, (bird.x-20, bird.y-15))
    bird.move()    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  bird.y += BIRD_VELOCITY_Y
    #Check for collisions
    collision(pipe_manager, bird.hitbox)
    #Score
    scoreboard(pipe_manager)


def game_over():
    game_display.blit(BACKGROUND, (0, 0))
    font = pygame.font.Font(None, 90)
    text = font.render(("GAME OVER"), 3, SCORE_COLORS)
    game_display.blit(text, (WIDTH/4, HEIGHT/2.2))
    pygame.display.update() 
    pygame.time.wait(1500)
    main()
        

def main(): 
    bird = Bird()
    pipe_manager = Pipe_Manager()
    run_game = True
    dt = 0
    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                run_game = False
        game_display.blit(BACKGROUND, (0, 0))
        pipe_manager.manage_pipes(dt)
        player(bird, pipe_manager)
        pygame.display.update()
        dt=clock.tick(FPS)

if __name__ == '__main__':
    main()
