from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import soundfile as sf
import numpy as np
import os

# modules
from models import SongAugment
from model import compile_model
from itunes_utils import get_song_data_by_id, get_song_meta_by_id
from augment_utils import augment_noise, augment_pitch, augment_speed


# Set up FastAPI app
app = FastAPI(title="Autoscriber",
              description="Automatic online meeting notes with voice recognition and NLP.",
              version="0.0.1")
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def aug_fname(song_augment):
    return f"files/{song_augment['song']['id']}-{song_augment['pitch']}-{song_augment['speed']}-{song_augment['noise']:.{3}f}.ogg"


# Sample rate
samplerate = 22050


@app.on_event('startup')
def startup():
    global base_model, embeddings
    print("starting up")
    # would load model here
    model = compile_model()
    model.load_weights('./model-checkpoints/epoch007_loss-97146000.000.hdf5')
    base_model = model.get_layer('Embedding')
    embeddings = np.load('./embeddings/emb1.npy')
    print("done")


@app.get('/')
def root():
    return 200


@app.post('/generate-song')
def generate_song(song_augment: SongAugment):
    song_augment = song_augment.dict()

    fname = aug_fname(song_augment)

    if not os.path.exists(fname):
        data = get_song_data_by_id(song_augment['song']['id'], fname)
        data = augment_noise(data, song_augment['noise'])
        data = augment_pitch(data, song_augment['pitch'], samplerate)
        data = augment_speed(data, song_augment['speed'])

        sf.write(fname, data, samplerate,
                 format='ogg', subtype='vorbis')
    return 200


@app.get('/files/{filename}')
def serve_file(filename: str):
    return FileResponse(f'files/{filename}', filename=filename)


@app.post('/predict-song')
def predict_song(song_augment: SongAugment):
    song_augment = song_augment.dict()
    fname = aug_fname(song_augment)

    # do model predict the id
    id = song_augment['song']['id']

    return {'song_id': id}


@app.get('/song-meta')
def serve_file(song_id: int):
    print(song_id)
    return get_song_meta_by_id(song_id).json()
