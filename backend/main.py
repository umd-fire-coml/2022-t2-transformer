from models import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import soundfile as sf
from song import song


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
    data = song
    samplerate = 22050
    sf.write('song.ogg', data, samplerate,
             format='ogg', subtype='vorbis')

    return {'song': data}


@app.get('/file/{filename}')
def serve_file(filename: str):
    return FileResponse(filename, filename=filename)


@app.post('/predict-song')
def predict_song(song):
    return
