from models import *
import requests
import librosa

API_URI = "https://itunes.apple.com/lookup"


def get_song_meta_by_id(song_id):
    return requests.get(f"{API_URI}?id={song_id}&entity=song")


def get_song_data_by_id(song_id: int, aug_fname: str):
    res = get_song_meta_by_id(song_id)
    if res.status_code != 200:
        return

    preview_url = res.json()['results'][0]['previewUrl']
    res = requests.get(preview_url)
    if res.status_code != 200:
        return

    filename = "files/temptrack.m4a"
    with open(filename, "wb") as f:
        f.write(res.content)
    data, _ = librosa.load(filename)
    return data
