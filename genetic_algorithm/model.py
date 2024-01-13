import tensorflow as tf


def DNA():
    input_layer = tf.keras.Input((6), name='Input')
    dense_layer = tf.keras.layers.Dense(
        10, activation="relu", name='Hidden')(input_layer)
    output_layer = tf.keras.layers.Dense(
        1, activation="linear", name='Output')(dense_layer)
    model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
    return model
