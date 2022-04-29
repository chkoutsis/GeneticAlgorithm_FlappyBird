from pydoc import render_doc
import pygame 
import random
import sys
import os
import tensorflow
import numpy as np 
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


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
N_POPULATION_BIRD = 15
MUTATION_THRESHOLD = 0.08

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
        self.dna = DNA()
        self.final_score = 0
        self.is_alive = True

    def jump(self):
        self.move_x = 0 
        self.move_y = BIRD_MAX_VELOCITY_Y
        self.x += self.move_x * GRAVITY
        self.y += BIRD_VELOCITY_Y

    def move(self):
        self.move_x = 0 
        self.move_y = BIRD_MAX_VELOCITY_Y
        self.x += self.move_x * GRAVITY
        self.y += self.move_y 


class Pipe:
    def __init__(self, img, pos, height, hitbox):
        self.img = img
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
        height = random.randint(HEIGHT/4, HEIGHT/1.5)
        gap = random.randint(150, 180)
        height_2 = HEIGHT - (height + gap)

        surf1 = pygame.Surface((self.pipe_width, height)).convert_alpha()
        surf1.fill((0, 0, 0, 0))
        hitbox_1 = (self.pipe_width, 0, self.pipe_width, height) 

        surf2 = pygame.Surface((self.pipe_width, height_2)).convert_alpha()
        surf2.fill((0, 0, 0, 0))
        hitbox_2 = (self.pipe_width,  height + gap, self.pipe_width, height_2) 

        pipe = Pipe(surf1, pygame.Vector2(WIDTH, random.randint(-50,-10)), height, hitbox_1)
        pipe2 = Pipe(surf2, pygame.Vector2(WIDTH, height + gap), height_2, hitbox_2)
        self.upper_pipes.append(pipe)
        self.lower_pipes.append(pipe2)

    def spawner(self, dt):
        if self.spawn_tick >= self.max_tick:
            self.make_pipe()
            self.spawn_tick = 0
        self.spawn_tick += dt

    def manage(self, dt):
        for pipe in self.upper_pipes[:]: 
            pipe.pos.x -= self.pipe_speed * dt
            if pipe.pos.x + self.pipe_width < -100: 
                removed_upper = self.upper_pipes.remove(pipe)    
                del removed_upper 
                self.score +=1
        for pipe in self.lower_pipes[:]: 
            pipe.pos.x -= self.pipe_speed * dt      
            if pipe.pos.x + self.pipe_width < -100: 
                removed_lower = self.lower_pipes.remove(pipe) 
                del removed_lower 

def collision(pipe_manager, bird_hitbox, bird, number):
    display_upper_hitboxes = []
    display_lower_hitboxes = []
    n = number
    #Check if bird is into the limits
    if bird_hitbox.y > HEIGHT or bird_hitbox.y < 0:
        bird_over(bird, pipe_manager)
        n = number -1
    #Check if bird hits the upper pipe
    for pipe in pipe_manager.upper_pipes:
        display_upper_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_upper_hitboxes[0].hitbox)
        pipe_display = game_display.blit(pygame.transform.rotate(PIPE_IMAGE, 180), pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display):
                bird_over(bird, pipe_manager)
                n = number -1
    #Check if bird hits the lower pipe
    for pipe in pipe_manager.lower_pipes:
        display_lower_hitboxes.append(pipe)
        pipe_hitbox = pygame.Rect(display_lower_hitboxes[0].hitbox)
        pipe_display = game_display.blit(PIPE_IMAGE, pipe.pos)
        if pipe_hitbox.colliderect(pipe_display):
            if bird_hitbox.colliderect(pipe_display):
                bird_over(bird, pipe_manager)
                n = number -1
    return n


def scoreboard(pipe_manager):
    font_score = pygame.font.Font(None, 72)
    text_score = font_score.render(str(pipe_manager.score), 2, SCORE_COLORS)
    game_display.blit(text_score, (WIDTH/2.2, 30))
         
        
def player(bird, pipe_manager, number):
    #Bird
    if bird.is_alive is True:
        bird.hitbox = game_display.blit(BIRD_IMAGE, (bird.x-20, bird.y-15))
        observations = data(bird, pipe_manager)
    # print(observations ,observations.shape)
        prediction_move = bird.dna.predict([observations])
        if prediction_move > 0 :
            bird.jump()
        else: 
            bird.move()    
        #Check for collisions
        n = collision(pipe_manager, bird.hitbox, bird, number)
        #Score
        scoreboard(pipe_manager)
        return n
    else: return number

def bird_over(bird, pipe_manager):
    bird.final_score = pipe_manager.score
    bird.is_alive = False

def DNA():    
    input_layer  = tensorflow.keras.Input((6), name='Input')
   # dense_layer = tensorflow.keras.layers.Dense(10, activation="relu", name='Hidden')(input_layer)
    output_layer = tensorflow.keras.layers.Dense(1, activation="linear", name='Output')(input_layer)
    model = tensorflow.keras.Model(inputs=input_layer, outputs=output_layer)
    return model

def data(bird, pipe_manager):
    upper_pipe_display = pygame.Rect(pipe_manager.upper_pipes[0].hitbox)
    lower_pipe_display = pygame.Rect(pipe_manager.lower_pipes[0].hitbox)
    inputs=[upper_pipe_display.x-bird.hitbox.width, bird.hitbox.y, HEIGHT-bird.hitbox.y,
            lower_pipe_display.y-upper_pipe_display.height, upper_pipe_display.height, HEIGHT-lower_pipe_display.y]
    return inputs

def bird_population():
    bird_population = []
    for _ in range(N_POPULATION_BIRD):
        bird_population.append(Bird())
    return bird_population

def last_bird(bird, pipe_manager):
    if bird.final_score == pipe_manager.score:
        last_bird = bird
    print(last_bird)
    return last_bird

def mutation(weight, MUTATION_THRESHOLD):
    print('baros einai', weight.dtype)
    if random.random() < MUTATION_THRESHOLD:
        return np.array([np.random.uniform(-1,1)])
    return weight

def crossover(parent_bird_1, parent_bird_2):
    child = Bird()
    parent_1_weights = parent_bird_1.dna.get_weights()[0]
    parent_2_weights = parent_bird_2.dna.get_weights()[0]
    parent_1_bias = parent_bird_1.dna.get_weights()[1]
    parent_2_bias = parent_bird_2.dna.get_weights()[1]
    print(parent_1_weights, parent_2_weights)
    print('*********************************************')
    print(parent_1_bias, parent_2_bias)
    print('*********************************************')
    child_weights = []
    new_weight = []
    mutation_child_weights = []
    for i in range(len(parent_1_weights)):
        new_weights = (parent_1_weights[i] + parent_2_weights[i]) / 2
        child_weights.append(new_weights)
    print('child weights ', child_weights)
    for weight in child_weights:
       new_weight = mutation(weight, MUTATION_THRESHOLD)
       mutation_child_weights.append(new_weight)
    print('mutation_child_weights ', mutation_child_weights)
    print('////////////////////////////////////////////////////////////')
    print(np.array(mutation_child_weights), 'baroi se lista')
    print(np.array(mutation_child_weights).shape, 'shape baroi se lista')
    print(np.array(parent_1_bias + parent_2_bias/2), 'bias')
    kid = np.array([np.array(mutation_child_weights), np.array((parent_1_bias + parent_2_bias)/2)])
    print('gios ', kid.shape)
    child.dna.set_weights(kid)
    return child
  
def reproduction(population):
    new_population = []
    for i in range(len(population)):
        sum_score = 0
        start_score = 0
        for bird in population: 
            sum_score += bird.final_score 
        random_1 = random.randint(0,sum_score)
        random_2 = random.randint(0,sum_score)
        parent_bird_1 = None
        parent_bird_2 = None
        for bird in population: 
            if random_1 in range(start_score, start_score + bird.final_score): parent_bird_1 = bird
            if random_2 in range(start_score, start_score + bird.final_score): parent_bird_2 = bird
            start_score = start_score + bird.final_score 
        if  parent_bird_1 == None: parent_bird_1 = population[random.randint(0,N_POPULATION_BIRD-1)] 
        if  parent_bird_2 == None: parent_bird_2 = population[random.randint(0,N_POPULATION_BIRD-1)] 
        child = crossover(parent_bird_1, parent_bird_2)
        new_population.append(child)   
    return new_population

def generation_text(generation_it):
    font_score = pygame.font.Font(None, 72)
    text = 'Generation ' + str(generation_it) 
    text_generation = font_score.render(text, 2, SCORE_COLORS)
    game_display.blit(text_generation, (WIDTH - 350, HEIGHT - 150))

def main(): 
    population = bird_population()
    generation_flag = True
    generation_it = 1 
    while generation_flag:
        n = N_POPULATION_BIRD
        pipe_manager = Pipe_Manager()
        run_game = True
        dt = 0
        pipe_manager.manage_pipes(dt)
        dt=clock.tick(FPS)
        while run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    run_game = False
            game_display.blit(BACKGROUND, (0, 0))
            for bird in population:
                n = player(bird, pipe_manager, n)
            pipe_manager.manage_pipes(dt)
            generation_text(generation_it)
            pygame.display.update()
            dt=clock.tick(FPS)
            if n ==0:
                run_game = False
                generation_it += 1
        population = reproduction(population)
        print('population = ', len(population))

if __name__ == '__main__':
    main()
