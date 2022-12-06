# Augemented Song Recognition Project

by Spencer Lutz, Rishi Keshav Pradeep, and Saatvik Vadlapatla

Our project is a song recognition model which has the ability to take in augmented snippets of songs and predict what the actual song is. We built the dataset used to train the model by creating web crawler to pull songs from the iTunes library. The end user interacts with a React app. This UI allows the user to pick from a list of songs and apply augmentations to it such as pitch, speed, and noise. Using the librosa library, a random triplet of STFTs(Short-Term Fourier Transform) are generated for the chosen audio. The STFT data is then split into patches and then fed into the transformer sequentially. This data is passed through a MLP layer which generates an embedding. This embedding is compared to the other songs in the dataset to find the one which is most similar.

# Directory Guide

The directory guide can be accessed [here](./directory.md).
