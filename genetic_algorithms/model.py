import tensorflow as tf


def dna():
    """
    Create and return a neural network model representing DNA.

    Returns:
    - model (tf.keras.Model): A TensorFlow Keras model.
    """
    input_layer = tf.keras.Input((6), name='Input')
    hidden_1_layer = tf.keras.layers.Dense(
        32, activation="relu", name='Hidden_1')(input_layer)
    hidden_2_layer = tf.keras.layers.Dense(
        64, activation="relu", name='Hidden_2')(hidden_1_layer)
    output_layer = tf.keras.layers.Dense(
        1, activation="linear", name='Output')(hidden_2_layer)
    model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
    return model
