import tensorflow


def DNA():
    input_layer = tensorflow.keras.Input((6), name='Input')
    dense_layer = tensorflow.keras.layers.Dense(
        10, activation="relu", name='Hidden')(input_layer)
    output_layer = tensorflow.keras.layers.Dense(
        1, activation="linear", name='Output')(dense_layer)
    model = tensorflow.keras.Model(inputs=input_layer, outputs=output_layer)
    return model
