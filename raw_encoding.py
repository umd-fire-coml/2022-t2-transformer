import mido
import numpy as np

f = open("wii.mid", "r")
a = np.fromfile(f, dtype=np.uint8)
print(a)
print(len(a))
# counts number of note on instrs, should be pretty high
print(np.count_nonzero(a == 144))
# this proves that this is possible, which is good