# Augemented Song Recognition Project

by Spencer Lutz, Rishi Keshav Pradeep, and Saatvik Vadlapatla

Our project is a song recognition model which has the ability to take in augmented snippets of songs and predict what the actual song is. We built the dataset used to train the model by creating web crawler to pull songs from the iTunes library. The end user interacts with a React app. This UI allows the user to pick from a list of songs and apply augmentations to it such as pitch, speed, and noise. Using the librosa library, a random triplet of STFTs(Short-Term Fourier Transform) are generated for the chosen audio. The STFT data is then split into patches and then fed into the transformer sequentially. This data is passed through a MLP layer which generates an embedding. This embedding is compared to the other songs in the dataset to find the one which is most similar.

Go to our project [here](./song-recognition/).

# MIDI Song Extender

by Steven Zhang, Rahul Dagar, and Kofi Boateng

Our project is a MIDI generation model that takes in the beginning of a MIDI file as a sample and generates original music based off of the given sample. We use an encoder package to compress MIDIs into integer arrays to feed into the model. One note is encoded by 2 integers representing note type and duration. The model takes an input of 50 encoded notes and predicts the next note. To generate more, we loop this process by appending the generated note to the array and feeding the most recent 50 notes back into the model. To train the model, we used the [adl-piano-midi dataset](https://github.com/lucasnfe/adl-piano-midi).

Check out our HuggingFace demo here! (will implement later)

You can also take a look by watching this demo video. (will implement later)

See our project [here](MIDI-song-extender).
