import random

import numpy as np

from config.config import n_population_bird, mutation_threshold
from core.bird import Bird


def bird_population(n_population_bird_var):
    bird_population_list = []
    for _ in range(n_population_bird_var):
        bird_population_list.append(Bird())
    return bird_population_list


def crossover(parent_bird_1, parent_bird_2):
    child = Bird()
    kid = [
        hidden_layer(parent_bird_1, parent_bird_2)[0],
        hidden_layer(parent_bird_1, parent_bird_2)[1],
        output_layer(parent_bird_1, parent_bird_2)[0],
        output_layer(parent_bird_1, parent_bird_2)[1],
    ]
    child.dna.set_weights(kid)
    return child


def mutation(weight, mutation_threshold_var):
    if random.random() < mutation_threshold_var:
        return np.random.uniform(-1, 1)
    return weight


def reproduction(population):
    new_population = []
    for _ in range(len(population)):
        sum_score = 0
        start_score = 0
        for bird in population:
            sum_score += bird.final_score
        random_1 = random.randint(0, sum_score)
        random_2 = random.randint(0, sum_score)
        parent_bird_1 = None
        parent_bird_2 = None
        for bird in population:
            if random_1 in range(start_score, start_score + bird.final_score):
                parent_bird_1 = bird
            if random_2 in range(start_score, start_score + bird.final_score):
                parent_bird_2 = bird
            start_score = start_score + bird.final_score
        if parent_bird_1 is None:
            parent_bird_1 = population[random.randint(
                0, n_population_bird - 1)]
        if parent_bird_2 is None:
            parent_bird_2 = population[random.randint(
                0, n_population_bird - 1)]
        child = crossover(parent_bird_1, parent_bird_2)
        new_population.append(child)
    return new_population


def hidden_layer(parent_bird_1, parent_bird_2):
    parent_1_weights = parent_bird_1.dna.get_weights()[0]
    parent_2_weights = parent_bird_2.dna.get_weights()[0]
    parent_1_bias = parent_bird_1.dna.get_weights()[1]
    parent_2_bias = parent_bird_2.dna.get_weights()[1]
    child_weights = []
    new_weights_i = []
    new_weights_j = []
    new_weight_i = []
    mutation_child_weights = []
    child_bias = []
    for i, parent_1_weights_i in enumerate(parent_1_weights):
        for j, par_1_wei_j in enumerate(parent_1_weights_i):
            new_weights_j = (
                par_1_wei_j + parent_2_weights[i][j]) / 2
            new_weights_i.append(new_weights_j)
        child_weights.append(new_weights_i)
        new_weights_i = []
    for weight_i in child_weights:
        for weight_j in weight_i:
            new_weight_j = mutation(weight_j, mutation_threshold)
            new_weight_i.append(new_weight_j)
        mutation_child_weights.append(new_weight_i)
        new_weight_i = []
    for i, parent_1_bias_i in enumerate(parent_1_bias):
        new_child_bias = (parent_1_bias_i + parent_2_bias[i]) / 2
        child_bias.append(new_child_bias)
    return np.array(mutation_child_weights, dtype="float32"), np.array(
        child_bias, dtype="float32"
    )


def output_layer(parent_bird_1, parent_bird_2):
    parent_1_weights = parent_bird_1.dna.get_weights()[2]
    parent_2_weights = parent_bird_2.dna.get_weights()[2]
    parent_1_bias = parent_bird_1.dna.get_weights()[3]
    parent_2_bias = parent_bird_2.dna.get_weights()[3]
    child_weights = []
    new_weights_i = []
    new_weights_j = []
    new_weight_i = []
    mutation_child_weights = []
    child_bias = []
    for i, parent_1_weights_i in enumerate(parent_1_weights):
        for j, par_1_wei_j in enumerate(parent_1_weights_i):
            new_weights_j = (
                par_1_wei_j + parent_2_weights[i][j]) / 2
            new_weights_i.append(new_weights_j)
        child_weights.append(new_weights_i)
        new_weights_i = []
    for weight_i in child_weights:
        for weight_j in weight_i:
            new_weight_j = mutation(weight_j, mutation_threshold)
            new_weight_i.append(new_weight_j)
        mutation_child_weights.append(new_weight_i)
        new_weight_i = []
    for i, parent_1_bias_i in enumerate(parent_1_bias):
        new_child_bias = (parent_1_bias_i + parent_2_bias[i]) / 2
        child_bias.append(new_child_bias)
    return np.array(mutation_child_weights, dtype="float32"), np.array(
        child_bias, dtype="float32"
    )
