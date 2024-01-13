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
    kid = [
        hidden_layer(parent_bird_1, parent_bird_2)[0],
        hidden_layer(parent_bird_1, parent_bird_2)[1],
        output_layer(parent_bird_1, parent_bird_2)[0],
        output_layer(parent_bird_1, parent_bird_2)[1],
    ]
    child.dna.set_weights(kid)
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
    if random.random() < mutation_threshold_var:
        return np.random.uniform(-1, 1)
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


def generate_layer(parent_bird_1, parent_bird_2, weight_index):
    """
    Generate weights and bias for a neural network layer.

    Parameters:
    - parent_bird_1 (Bird): First parent bird.
    - parent_bird_2 (Bird): Second parent bird.
    - weight_index (int): Index indicating the type of weights and bias.
                        0 for hidden layer, 2 for output layer.

    Returns:
    - mutation_child_weights (numpy.ndarray): Mutated weights for the layer.
    - child_bias (numpy.ndarray): Bias for the layer.
    """
    parent_1_weights = parent_bird_1.dna.get_weights()[weight_index]
    parent_2_weights = parent_bird_2.dna.get_weights()[weight_index]
    child_weights = []

    for parent_1_weights_i in parent_1_weights:
        new_weights_i = [(w1 + w2) / 2 for w1, w2 in zip(parent_1_weights_i,
                                                         parent_2_weights[len(child_weights)])]
        child_weights.append(new_weights_i)

    mutation_child_weights = [
        [mutation(w, MUTATION_THRESHOLD) for w in weight_i] for weight_i in child_weights
    ]

    parent_1_bias = parent_bird_1.dna.get_weights()[weight_index + 1]
    parent_2_bias = parent_bird_2.dna.get_weights()[weight_index + 1]
    child_bias = [(b1 + b2) / 2 for b1,
                  b2 in zip(parent_1_bias, parent_2_bias)]

    return np.array(mutation_child_weights, dtype="float32"), \
        np.array(child_bias, dtype="float32")


def hidden_layer(parent_bird_1, parent_bird_2):
    """
    Generate weights and bias for a hidden layer in a neural network.

    Parameters:
    - parent_bird_1 (Bird): First parent bird.
    - parent_bird_2 (Bird): Second parent bird.

    Returns:
    - mutation_child_weights (numpy.ndarray): Mutated weights for the hidden layer.
    - child_bias (numpy.ndarray): Bias for the hidden layer.
    """
    return generate_layer(parent_bird_1, parent_bird_2, weight_index=0)


def output_layer(parent_bird_1, parent_bird_2):
    """
    Generate weights and bias for an output layer in a neural network.

    Parameters:
    - parent_bird_1 (Bird): First parent bird.
    - parent_bird_2 (Bird): Second parent bird.

    Returns:
    - mutation_child_weights (numpy.ndarray): Mutated weights for the output layer.
    - child_bias (numpy.ndarray): Bias for the output layer.
    """
    return generate_layer(parent_bird_1, parent_bird_2, weight_index=2)
