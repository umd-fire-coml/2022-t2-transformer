import streamlit as st

from tensorflow import keras
from midi2audio import FluidSynth

from musicautobot.multitask_transformer import *

model = keras.models.load_model("sigmoidCheckpoints")
data = np.load("data.npy", allow_pickle = True)


def predict_music(model, input_vector, num):
    normalized = input_vector / 311
    for i in range(num):
        predict = model.predict(np.reshape(normalized[-100:], (1, 100)), verbose=0)
        normalized = np.append(normalized, predict)

    result = np.rint(normalized * 311)
    # edits to prediction
    for i in range(100, len(result)):
        if abs(result[i] - 8) < 10:
            print("change made to " + str(result[i]))
            result[i] = 8
    return result

def midi_predict(model, test):
    test_midi = idxenc2stream(test.astype("int"), MusicVocab.create())
    test_midi.write('midi',"input.mid")
    res = predict_music(model, test, 100)
    print(res[-40:])
    output = idxenc2stream(res.astype("int"), MusicVocab.create())
    output.write('midi',"output.mid")
    return res.astype("int")


st.title('MIDI generator!')

index= st.slider("Choose your MIDI baseline. each number is encoded to a different song snippet.", min_value=0, \
                 max_value=100)
st.write("You selected baseline number " + str(index))
selection = data[index][0:100]
test_midi = idxenc2stream(selection.astype("int"), MusicVocab.create())
test_midi.write('midi', "input.mid")
fs = FluidSynth()
fs.midi_to_audio('input.mid', 'input.wav')
st.audio("input.wav", format="audio/wav")

if st.button("Generate MIDI! (Please be patient)"):
    array = midi_predict(model, selection)
    fs.midi_to_audio('output.mid', 'output.wav')
    st.audio("output.wav", format="audio/wav")

#to do this i edited the path variable and also programdata file