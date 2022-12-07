from typing import List
from pydantic import BaseModel


class Song(BaseModel):
    title: str = ''
    artist: str = ''
    id: int

class SongAugment(BaseModel):
    song: Song
    pitch: int
    speed: float
    noise: float
