from mido import MidiFile

mid = MidiFile('test1.midi')
array = []
for msg in mid:
    if str(msg)[0:14] != "control_change":
        array.append(str(msg))
for i in array:
    print(i)
print(len(array))
