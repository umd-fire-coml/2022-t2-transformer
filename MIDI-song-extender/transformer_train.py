import numpy as np
import keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import datetime
from packaging import version


from enum import Enum

import os
import gc

n_classes = 2
def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
    # Normalization and Attention
    x = layers.LayerNormalization(epsilon=1e-6)(inputs)
    x = layers.MultiHeadAttention(
        key_dim=head_size, num_heads=num_heads, dropout=dropout
    )(x, x)
    x = layers.Dropout(dropout)(x)
    res = x + inputs

    # Feed Forward Part
    x = layers.LayerNormalization(epsilon=1e-6)(res)
    x = layers.Conv1D(filters=ff_dim, kernel_size=1, activation="relu")(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    return x + res

def build_model(
    input_shape,
    head_size,
    num_heads,
    ff_dim,
    num_transformer_blocks,
    mlp_units,
    dropout=0,
    mlp_dropout=0,
):
    inputs = keras.Input(shape=input_shape)
    x = inputs
    for _ in range(num_transformer_blocks):
        x = transformer_encoder(x, head_size, num_heads, ff_dim, dropout)

    x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    for dim in mlp_units:
        x = layers.Dense(dim, activation="relu")(x)
        x = layers.Dropout(mlp_dropout)(x)
    outputs = layers.Dense(n_classes, activation="softmax")(x)
    return keras.Model(inputs, outputs)

model = build_model((100,1),
    head_size=25,
    num_heads=4,
    ff_dim=4,
    num_transformer_blocks=4,
    mlp_units=[50],
    mlp_dropout=0.4,
    dropout=0.25)
model.compile(
    loss="mse",
    optimizer=keras.optimizers.Adam(learning_rate=1e-4),
    metrics=["mse"],
)
try:
    a = keras.models.load_model("/home/ubuntu/projectpathing/transformer1")
    model = a
except:
    print("except")

model.summary()

# this trains 1 epoch

x_val = np.load("/home/ubuntu/data 3/x_200.npy")
y_val = np.load("/home/ubuntu/data 3/y_200.npy")
for g in range(211,221):
    a = np.load("/home/ubuntu/data 3/x_" + str(g) + ".npy")
    b = np.load("/home/ubuntu/data 3/y_" + str(g) + ".npy")
    x_val = np.concatenate((x_val, a))
    y_val = np.concatenate((y_val, b))
for i in range(20):  # let's make the last batch the validation (#200-220 inclusive)
    x = None
    y = None
    gc.collect()
    for j in range(10):
        print(10 * i + j)
        new_x = np.load("/home/ubuntu/data 3/x_" + str(10 * i + j) + ".npy")
        new_y = np.load("/home/ubuntu/data 3/y_" + str(10 * i + j) + ".npy")
        if x is None and y is None:
            x = new_x
            y = new_y
        else:
            x = np.concatenate((x, new_x))
            y = np.concatenate((y, new_y))
    # this will need to be optimized
    x = x.reshape((x.shape[0], x.shape[1], 1))
    y = y.reshape((y.shape[0], y.shape[1], 1))
    x_val = x_val.reshape((x_val.shape[0], x_val.shape[1], 1))
    y_val = y_val.reshape((y_val.shape[0], y_val.shape[1], 1))
    print(x.shape)
    model.fit(x, y, validation_data=(x_val, y_val), epochs=1)
    model.save("/home/ubuntu/projectpathing/transformer1")