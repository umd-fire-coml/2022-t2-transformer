import os
import librosa
import librosa.effects
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import backend as K
import warnings
warnings.filterwarnings("ignore")

SR = 22050
INPUT_SHAPE = (1025, 130)

# Hyperparameters
learning_rate = 0.001
weight_decay = 0.0001
batch_size = 4
num_epochs = 10
patch_width = 1
num_patches = INPUT_SHAPE[1] // patch_width
projection_dim = 16  # 256
num_heads = 4
transformer_units = [
    projection_dim * 2,
    projection_dim,
]
transformer_layers = 1  # 8
mlp_head_units = [16, 8]  # [512, 256] #[2048, 1024]
embedding_length = 16  # 128


def mlp(x, hidden_units, dropout_rate):
    for units in hidden_units:
        x = layers.Dense(units, activation=tf.nn.gelu)(x)
        x = layers.Dropout(dropout_rate)(x)
    return x


class Patches(layers.Layer):
    def __init__(self, num_patches):
        super(Patches, self).__init__(name='Patches')
        self.num_patches = num_patches
        self.patch_width = INPUT_SHAPE[1] // num_patches

    # def build(self, input_shape):
    #     self.batch_size = input_shape[0]
    #     super(Patches, self).build(input_shape)

    def call(self, inputs):
        batch_size = tf.shape(inputs)[0]
        inp = tf.reshape(
            inputs, [batch_size, INPUT_SHAPE[0], INPUT_SHAPE[1], 1])
        patches = tf.image.extract_patches(
            images=inp,
            sizes=[1, INPUT_SHAPE[0], self.patch_width, 1],
            strides=[1, INPUT_SHAPE[0], self.patch_width, 1],
            rates=[1, 1, 1, 1],
            padding="VALID"
        )
        patch_dims = patches.shape[-1]
        patches = tf.reshape(patches, [batch_size, -1, patch_dims])
        return patches


class PatchEncoder(layers.Layer):
    def __init__(self, num_patches, projection_dim):
        super(PatchEncoder, self).__init__(name='PatchEncoder')
        self.num_patches = num_patches
        self.projection = layers.Dense(units=projection_dim)
        self.position_embedding = layers.Embedding(
            input_dim=num_patches, output_dim=projection_dim
        )

    def call(self, patch):
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        proj = self.projection(patch)
        pose = self.position_embedding(positions)
        # should be 'encoded = proj + pose'
        encoded = tf.reshape(proj, [-1, num_patches, projection_dim])
        return encoded


class TripletLossLayer(layers.Layer):
    def __init__(self, alpha, **kwargs):
        self.alpha = alpha
        super(TripletLossLayer, self).__init__(**kwargs)

    def get_config(self):
        config = super().get_config().copy()
        config.update({'alpha': self.alpha})
        return config

    def triplet_loss(self, inputs):
        a, p, n = inputs
        p_dist = K.sum(K.square(a-p), axis=-1)
        n_dist = K.sum(K.square(a-n), axis=-1)
        # return K.sum(K.maximum(p_dist - n_dist + self.alpha, 0), axis=0)
        return K.sum(p_dist - n_dist + self.alpha, axis=0)

    def call(self, inputs):
        loss = self.triplet_loss(inputs)
        self.add_loss(loss)
        return loss


def compile_model():
    in_a = layers.Input(shape=INPUT_SHAPE, name='anchor_input')
    in_p = layers.Input(shape=INPUT_SHAPE, name='positive_input')
    in_n = layers.Input(shape=INPUT_SHAPE, name='negative_input')

    input = layers.Input(shape=INPUT_SHAPE, name='Input')
    # norm = layers.Normalization()(input) # Do we need / want this?
    patches = Patches(num_patches)(input)
    encoded = PatchEncoder(num_patches, projection_dim)(patches)

    # for _ in range(transformer_layers):
    #     x1 = layers.LayerNormalization(epsilon=1e-6)(encoded)
    #     attention_output = layers.MultiHeadAttention(
    #         num_heads=num_heads, key_dim=projection_dim, dropout=0.1
    #     )(x1, x1)
    #     x2 = layers.Add()([attention_output, encoded])
    #     x3 = layers.LayerNormalization(epsilon=1e-6)(x2)
    #     x3 = mlp(x3, hidden_units=transformer_units, dropout_rate=0.1)
    #     encoded = layers.Add()([x3, x2])

    representation = layers.LayerNormalization(epsilon=1e-6)(encoded)
    representation = layers.Flatten()(representation)
    representation = layers.Dropout(0.5)(representation)
    features = mlp(representation, hidden_units=mlp_head_units,
                   dropout_rate=0.5)
    output = layers.Dense(embedding_length)(features)

    embedding = keras.Model(input, output, name="Embedding")

    emb_a = embedding(in_a)
    emb_p = embedding(in_p)
    emb_n = embedding(in_n)

    triplet_loss_layer = TripletLossLayer(
        alpha=0.4, name='triplet_loss_layer')([emb_a, emb_p, emb_n])

    model = keras.Model([in_a, in_p, in_n], triplet_loss_layer)
    # optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss=None)
    model.compile(loss=None, optimizer='adam')
    return model


def embedding_distance(embedding1, embedding2):
    return np.sum(np.square(embedding1 - embedding2))


# Function to make a guess based on a 3 second numpy snippet
def guess(model, embeddings, snippet):
    inp = librosa.stft(snippet)
    emb = model.predict(tf.reshape(
        inp, [-1, inp.shape[0], inp.shape[1]]), verbose=0)
    emb_distances = [(embedding_distance(emb, e), id) for e, id in embeddings]
    shortest_distances = sorted(emb_distances)
    dist, id = shortest_distances[0]
    return id, dist
