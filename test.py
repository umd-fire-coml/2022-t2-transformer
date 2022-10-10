from enum import Enum
import os
import fastai
from musicautobot.numpy_encode import *
from musicautobot.config import *
from musicautobot.music_transformer import *
from musicautobot.multitask_transformer import *
from musicautobot.utils import midifile


embedding = midi2idxenc('Comic Relief.mid', MusicVocab.create())
print(list(MusicVocab.create().stoi.items()))
print(type(embedding))
output = idxenc2stream(embedding, MusicVocab.create())
output.write('midi',"output.mid")

# test: it merges all the streams into one and makes the tempo 120, which is suboptimal