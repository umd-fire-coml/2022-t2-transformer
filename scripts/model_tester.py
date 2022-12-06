# Usage: model_tester.py <path to weights> [path to embeddings]
# If path to embeddings not specified, will be generated (takes longer)
from model import compile_model
import sys
import os
import librosa
import random
import numpy as np
import tensorflow as tf
from tqdm import tqdm

SR = 22050
WEIGHTS_PATH = os.path.join('ckpts', sys.argv[1])

# load compiled model
model = compile_model()

# Show summary for compiled model
print(model.summary())

# Load weights and predictor
model.load_weights(WEIGHTS_PATH)
base_model = model.get_layer('Embedding')

if sys.argv[2]:
    print(f"Loading embeddings from {sys.argv[2]}")
    embeddings = np.load(sys.argv[2], allow_pickle=True)
else:
    # Generate embeddings
    print(f"Generating embeddings...")
    embeddings = []
    for filename in tqdm(os.listdir('songs')):
        song, _, _, id = np.load(os.path.join('songs', filename), allow_pickle=True)
        clip_secs = 3
        clip_samples = clip_secs * SR
        for start in range(0, len(song), clip_samples):
            inputs = []
            if start + clip_samples < len(song):
                inp = librosa.stft(song[start : start + clip_samples])
                inputs.append(inp)
                emb = base_model.predict(tf.reshape(inp, [-1, inp.shape[0], inp.shape[1]]), verbose=0)
                # With Batch Normalization, maybe predict over larger batches if the predictions are still close
                embeddings.append((emb, id))

    # Save embeddings for future use
    name = os.path.basename(WEIGHTS_PATH)[:-5]
    path = os.path.join('embeddings', name)
    print(f"Saving embeddings to {path}.npy")
    np.save(path, np.array(embeddings))

def embedding_distance(embedding1, embedding2):
    return np.sum(np.square(embedding1 - embedding2))

# Function to make a guess based on a 3 second numpy snippet
def guess(snippet, top=1):
    inp = librosa.stft(snippet)
    emb = base_model.predict(tf.reshape(inp, [-1, inp.shape[0], inp.shape[1]]), verbose=0)
    emb_distances = [(embedding_distance(emb, e), id) for e, id in embeddings]
    shortest_distances = sorted(emb_distances)
    return shortest_distances[:top]

# Functions to augment test songs
def augment_noise(sound):
    y_noise = sound.copy()
    noise_amp = 0.005 * np.random.uniform() * np.amax(y_noise)
    y_noise = y_noise.astype('float64') + noise_amp * np.random.normal(size=y_noise.shape[0])
    return y_noise

def augment_pitch_speed(sound):
    y_pitch_speed = sound.copy()
    speed_fac = np.random.uniform(low=0.8, high=1.5)
    tmp = np.interp(np.arange(0, len(y_pitch_speed), speed_fac), np.arange(0, len(y_pitch_speed)), y_pitch_speed)
    return tmp

def augment_pitch(sound):
    pitch_diff = np.random.uniform(low=-12, high=12)
    return librosa.effects.pitch_shift(sound, SR, pitch_diff)

def augment_speed(sound):
    rate_diff = np.random.uniform(low=0.8, high=1.5)
    return librosa.effects.time_stretch(sound, rate_diff)

def augment_data(sound, augmentations):
    ret = sound.copy()
    for a in augmentations:
        ret = a(ret)
    return ret



iterations = 10

for index, ts_filename in tqdm(enumerate(os.listdir('songs'))):
    test_song, name, artist, id = np.load(os.path.join('songs', ts_filename), allow_pickle=True)

    augmentations = [
        augment_noise,
        augment_pitch, 
        augment_speed
    ]
    aug_song = augment_data(test_song, augmentations)

    clip_secs = 3
    clip_samples = clip_secs * SR
    max_start = len(aug_song) - clip_samples
    start = int(random.uniform(0, max_start))
    test_snippet = aug_song[start : start + clip_samples]
    
    output = guess(test_snippet, top=len(embeddings))
    print(f'Top guess: {output[0][0]}, distance: {output[0][1]}')
    print(f'Actual: {id}')

    for i, o in enumerate(output):
        if o[1] == id:
            print(f'Guess {i+1} out of {len(embeddings)}')
            break
        
    if index == iterations - 1:
        break