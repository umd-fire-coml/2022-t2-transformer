import requests
import urllib.parse
import os
import random
import librosa
import librosa.effects
import numpy as np

# Librosa gets angry for some reason
import warnings
warnings.filterwarnings("ignore")

# Sample Rate
SR = 22050

# Gets initial artist ids to seed the spidering
def get_initial_artist_ids(seeds, num_songs_per_query):
    ids = []

    with requests.Session() as s:
        for seed in seeds:
            search = urllib.parse.quote_plus(seed)
            url = 'https://itunes.apple.com/search?term='+search+'&entity=song&limit='+str(num_songs_per_query)
            response = s.get(url)
            try:
                results = response.json()["results"]
                for r in results:
                    id = r['artistId']
                    if id not in ids:
                        ids.append(id)
            except:
                pass
            
    return ids


# Spiders the itunes store and saves each song in a npy file, returns list of song ids
def spider_itunes(num_songs, artist_ids, songs_per_artist=2, songs_queried_per_artist=5):
    s = requests.Session()
    song_ids = set()
    filenames = []
    n_songs = 0

    for id in artist_ids:
        url = f'https://itunes.apple.com/lookup?id={id}&entity=song&limit={songs_queried_per_artist}'
        response = s.get(url)

        try:
            results = response.json()["results"]
        except BaseException as err:
            print("Response Not JSON:", url, ":", response.content)
            continue

        results = [r for r in results 
                    if r['wrapperType'] == 'track' 
                    and r['trackId'] not in song_ids
                  ]

        for r in results[:songs_per_artist]:
            if r['artistId'] not in artist_ids:
                artist_ids.append(r['artistId'])

            sound = s.get(r["previewUrl"]).content
            filename = "temptrack.m4a"
            with open(filename, "wb") as f:
                f.write(sound)
            data, _ = librosa.load(filename)
            id = r['trackId']

            arr = [data, r['artistName'], r['trackName'], id]
            filename = f'songs/{id}.npy'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            np.save(filename, arr)
            filenames.append(filename)
            n_songs += 1
            song_ids.add(id)

            if n_songs == num_songs:
                s.close()
                return filenames

    if n_songs < num_songs:
        print("Not enough songs")

    s.close()
    return filenames


# Takes in sound data and runs augmentations on it
def augment_data(sound, augmentations):
    ret = sound.copy()
    for a in augmentations:
        ret = a(ret)
    return ret


# Add noise to signal
def augment_noise(sound):
    y_noise = sound.copy()
    noise_amp = 0.005 * np.random.uniform() * np.amax(y_noise)
    y_noise = y_noise.astype('float64') + noise_amp * np.random.normal(size=y_noise.shape[0])
    return y_noise


# Change the pitch and speed together (i.e. high pitch => high speed)
def augment_pitch_speed(sound):
    y_pitch_speed = sound.copy()
    speed_fac = np.random.uniform(low=0.8, high=1.5)
    tmp = np.interp(np.arange(0, len(y_pitch_speed), speed_fac), np.arange(0, len(y_pitch_speed)), y_pitch_speed)
    return tmp


# Change the pitch independently
def augment_pitch(sound):
    pitch_diff = np.random.uniform(low=-12, high=12)
    return librosa.effects.pitch_shift(sound, SR, pitch_diff)


# Change the speed independently
def augment_speed(sound):
    rate_diff = np.random.uniform(low=0.8, high=1.5)
    return librosa.effects.time_stretch(sound, rate_diff)


# Generates a random triplet of STFTs when given a list of filenames
def get_random_triplet(files):
    augmentations = [
        augment_noise,
        augment_pitch, 
        augment_speed
    ]
    
    pos_file, neg_file = random.sample(files, 2)
    pos_data = np.load(pos_file, allow_pickle=True)
    neg_data = np.load(neg_file, allow_pickle=True)
    pos, neg = pos_data[0], neg_data[0]

    anchor = augment_data(pos, augmentations)
    positive = augment_data(pos, augmentations)
    negative = augment_data(neg, augmentations)

    clip_secs = 3
    clip_samples = clip_secs * SR
    min_len = min(len(anchor), len(positive), len(negative))
    start_pc = random.uniform(0, (min_len - clip_samples) / min_len)
            
    a_start = int(start_pc * len(anchor))
    p_start = int(start_pc * len(positive))
    n_start = int(start_pc * len(negative))

    return (
        librosa.stft(anchor[a_start : a_start + clip_samples]),
        librosa.stft(positive[p_start : p_start + clip_samples]),
        librosa.stft(negative[n_start : n_start + clip_samples]),
    )


# Saves a certain amount of triplets to files in /triplets directory
def generate_triplets_to_file(num_triplets, filenames):
    digits = len(str(num_triplets-1))

    for i in range(num_triplets):
        triplet = get_random_triplet(filenames)
        filename = f'triplets/{str(i).zfill(digits)}.npy'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        np.save(filename, triplet)


# Use the above methods to generate triplets to file
seeds = list(map(chr, range(97, 123)))

artist_ids = get_initial_artist_ids(seeds, 10)
filenames = spider_itunes(10, artist_ids)
generate_triplets_to_file(20, filenames)