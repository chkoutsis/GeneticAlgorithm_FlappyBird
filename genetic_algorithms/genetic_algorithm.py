import random

import numpy as np

from config.config import MUTATION_THRESHOLD, N_POPULATION_BIRD
from core.bird import Bird


def bird_population(n_population_bird_var):
    """
    Generate a population of bird objects.

    Parameters:
    - n_population_bird_var (int): Number of bird objects to generate.

    Returns:
    - bird_population_list (list): List containing the generated bird objects.
    """
    bird_population_list = []
    for _ in range(n_population_bird_var):
        bird_population_list.append(Bird())
    return bird_population_list


def crossover(parent_bird_1, parent_bird_2):
    """
    Perform crossover between two parent birds to create a child bird.

    Parameters:
    - parent_bird_1 (Bird): First parent bird.
    - parent_bird_2 (Bird): Second parent bird.

    Returns:
    - child (Bird): The resulting child bird from the crossover.
    """
    child = Bird()
    child_model = child.dna
    for child_layer, parent_layer_1, parent_layer_2 in zip(
            child_model.layers,
            parent_bird_1.dna.layers,
            parent_bird_2.dna.layers):
        if child_layer.get_weights():
            weights_parent_1 = parent_layer_1.get_weights()
            weights_parent_2 = parent_layer_2.get_weights()
            weights_to_use = []
            for w1, w2 in zip(weights_parent_1, weights_parent_2):
                if w1.shape != w2.shape:
                    weights_to_use.append(
                        np.random.uniform(-1, 1, size=w1.shape) * 0.5)
                else:
                    weights_to_use.append(0.5 * (w1 + w2))
            weights_mutated = [mutation(w, MUTATION_THRESHOLD)
                               for w in weights_to_use]
            for w, w_mutated in zip(weights_to_use, weights_mutated):
                if isinstance(w, np.ndarray) and w.shape != w_mutated.shape:
                    weights_mutated = [np.random.uniform(-1, 1, size=w.shape)
                                       for _ in range(len(weights_to_use))]
                    break

            child_layer.set_weights(weights_mutated)
    child.dna = child_model
    return child


def mutation(weight, mutation_threshold_var):
    """
    Apply mutation to a weight based on a mutation threshold.

    Parameters:
    - weight (float): The weight to be mutated.
    - mutation_threshold_var (float): Threshold for mutation probability.

    Returns:
    - float: Mutated weight if mutation occurs, otherwise the original weight.
    """
    if isinstance(weight, np.ndarray):
        if random.random() < mutation_threshold_var:
            return np.random.uniform(-1, 1, size=weight.shape)
    return weight


def reproduction(population):
    """
    Create a new population of birds through reproduction.

    Parameters:
    - population (list): List of bird objects in the current population.

    Returns:
    - new_population (list): List containing the newly generated bird objects.
    """
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
                0, N_POPULATION_BIRD - 1)]
        if parent_bird_2 is None:
            parent_bird_2 = population[random.randint(
                0, N_POPULATION_BIRD - 1)]
        child = crossover(parent_bird_1, parent_bird_2)
        new_population.append(child)
    return new_population
