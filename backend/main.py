from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import soundfile as sf
import os

# modules
from models import Song, UnidentifiedSong, SongAugment
from itunes_utils import get_song_by_id
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
# Sample rate
samplerate = 22050


@app.on_event('startup')
def startup():
    print("starting up")
    # would load model here
    return


@app.get('/')
def root():
    return 200


@app.post('/generate-song')
def generate_song(song_augment: SongAugment):
    song_augment = song_augment.dict()
    aug_fname = f"files/{song_augment['song']['id']}-{song_augment['pitch']}-{song_augment['speed']}-{song_augment['noise']:.{3}f}.ogg"

    if not os.path.exists(aug_fname):
        data = get_song_by_id(song_augment, aug_fname)
        data = augment_noise(data, song_augment['noise'])
        data = augment_pitch(data, song_augment['pitch'], samplerate)
        data = augment_speed(data, song_augment['speed'])

        sf.write(aug_fname, data, samplerate,
                 format='ogg', subtype='vorbis')

    return 200


@app.get('/files/{filename}')
def serve_file(filename: str):
    return FileResponse(f'files/{filename}', filename=filename)


@app.post('/predict-song')
def predict_song(song):
    return
