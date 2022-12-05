# Augemented Song Recognition Project
 by Keshav Pradeep, Spencer Lutz, and Saatvik Vadlapatla

Our project is a song recognition model which has the ability to take in augmented snippets of songs and predict what the actual song is. The dataset used to train the model were songs pulled from the ITunes library. The user interacts with a UI built using React. The UI allows the user to pick from a list of songs and apply augmentations to it such as pitch, speed, and noise. Using the librosa library, a random triplet of STFTs(Short-Term Fourier Transform) are generated for the chosen audio. The STFT data is then split into patches which is then fed into the transformer sequentially. This data is passed through a MLP layer which generates an embedding. This embedding is compared to the other songs in the dataset to find the one which is most similar.


# Directory Guide

## Backend

### itunes_utils.py

This file is used to pull data from the ITunes API, and get song data simply using the song ID.

### main.py

### model.py

This file is used to split the audio snippets into patches and then feed it into the transformer sequentially. Then a MLP layer is used to generate an embedding and compare it to the embeddings of other sonfs ro make a prediction on what the user requested song is. 


## Frontend

### App.css

The App.css file sets the parameters for the UI and style it according to our preferences. It sets the height,color, font, etc of the app using CSS.

### App.js

The App.js utilizes Javascript to build the UI for the frontend of our project. The UI displays 10 songs which the user can choose from. The user can then choose the pitch, speed, and noise augmentations they wish to apply to their song which the file keeps track of and sends to the backend to apply the augmentations to the actual song. The pitch, speed and noise are displayed in terms of sliders which the user can set. The app then displays the augmented sound for the user to listen to. Finally, there is a Predict button which when pressed, utilizes the backend to get a prediction for the requested song, and then displays the artist name, artwork, track name, and url on the UI for the user to see.

### SongCard.js

The SongCard.js file displays the details about the predicted song. It creates the tempelate to display the artist name, song name, and the artwork for the song which the backend predicts.

