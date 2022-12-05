# Augemented Song Recognition Project

by Rishi Keshav Pradeep, Spencer Lutz, and Saatvik Vadlapatla

Our project is a song recognition model which has the ability to take in augmented snippets of songs and predict what the actual song is. We built the dataset used to train the model by creating web crawler to pull songs from the iTunes library. The end user interacts with a React app. This UI allows the user to pick from a list of songs and apply augmentations to it such as pitch, speed, and noise. Using the librosa library, a random triplet of STFTs(Short-Term Fourier Transform) are generated for the chosen audio. The STFT data is then split into patches and then fed into the transformer sequentially. This data is passed through a MLP layer which generates an embedding. This embedding is compared to the other songs in the dataset to find the one which is most similar.

# Directory Guide

## Backend

### itunes_utils.py

This file is used to pull data from the ITunes API, and get song data simply using the song ID.

### main.py

### model.py

This file is used to split the audio snippets into patches and then feed it into the transformer sequentially. Then a MLP layer is used to generate an embedding and compare it to the embeddings of other sonfs ro make a prediction on what the user requested song is.

## Frontend

`frontend/src/App.css`: Contains global styling for our application.

`frontend/src/App.js`: The root endpoint for our React app. This is the main page for our Single Page Application. We utilize the material-ui library for a majority of our components.

`frontend/src/components/SongCard.js`: A component that displays info about a song in a compact card, given a song_id prop.
