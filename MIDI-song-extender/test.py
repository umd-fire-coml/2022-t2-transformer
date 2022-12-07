from enum import Enum
import os
import numpy as np
import fastai
from musicautobot.numpy_encode import *
from musicautobot.config import *
from musicautobot.music_transformer import *
from musicautobot.multitask_transformer import *
from musicautobot.utils import midifile

item = MusicItem.from_file("C:\\Users\\drago\\OneDrive\\Documents\\MOVE TO NEW PC\\College\\fall 2022\FIRE\\adl-piano-midi\\42.mid", MusicVocab.create())
index = 0
for i in item.to_text().split(" "):
    if (i[0] != "x" and i[0] != "n") and index % 2 == 0:
        print(i)
    elif i[0] != "d" and index % 2 == 1:
        print(i)
    index += 1
embedding = midi2idxenc('Comic Relief.mid', MusicVocab.create())

print(list(MusicVocab.create().stoi.items()))
print(embedding)
x = np.load("data/x_0.npy")
print(x[0] * 311)
output = idxenc2stream((x[0] * 311).astype("int"), MusicVocab.create())
output.write('midi',"output.mid")


# test: it merges all the streams into one and makes the tempo 120, which is suboptimal