from typing import List
from pydantic import BaseModel


class Song(BaseModel):
    title: str = ''
    artist: str = ''
    id: int


class UnidentifiedSong(BaseModel):
    data: List[float] = []


class SongAugment(BaseModel):
    song: Song
    pitch: int
    speed: float
    noise: float

# -12-12
# 0.8-1.5
# 0-0.1
