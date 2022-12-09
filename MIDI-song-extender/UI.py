

"""## Imports"""
import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
import gradio as gr
from pathlib import Path
import subprocess
from transformers import AutoTokenizer
from transformers import TFAutoModelForCausalLM
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from musicautobot.music_transformer.transform import idxenc2stream, midi2idxenc
from musicautobot.vocab import MusicVocab
import keras

"""## Model Loads"""

#load poem generation model
model_poem_gn = TFAutoModelForCausalLM.from_pretrained('../merged-ui/models-misc/peom_gn')
base_model_poem_gn = "distilgpt2"
tokenizer_poem_gn = AutoTokenizer.from_pretrained(base_model_poem_gn)

#load sentiment analysis
model_sa = TFAutoModelForSequenceClassification.from_pretrained('../merged-ui/models-misc/sen_analysis/bert')
base_model_sa = "distilbert-base-uncased"
tokenizer_sa = AutoTokenizer.from_pretrained(base_model_sa)

#music generation
"""
base_path = "/content/drive/MyDrive/FIRE_3rd Sem/music_gn/"
#path_mid_file -> Replace this with model generated file path
path_mid_file = base_path + "Comic_Relief.mid"
path_wav_file = base_path + "output_comic.wav"
subprocess.call(['timidity', path_mid_file, "-Ow", "-o", path_wav_file])"""
music_gen_base_path = "../merged-ui/music_gen/"
model_music_gen = keras.models.load_model("transformer-final")

"""## Music Generation"""

def predict_music(model, input_vector, num):
    normalized = input_vector / 311
    for i in range(num):
        predict = model.predict(np.reshape(normalized[-100:], (1,100)), verbose = 0)
        normalized = np.append(normalized, predict)
    
    result = np.rint(normalized * 311)
    # edits to prediction
    for i in range(100, len(result)):
        if i % 2 == 0:
            if abs(result[i] - 8) < 5 and result[i] != 8:
                result[i] = 8
        else:
            if result[i] < 137:
                result[i] = 137
    return result

# this function takes a 100 length encoded song beginning as an input and 
def midi_predict(model, test, num_notes):
    test_midi = idxenc2stream(test.astype("int"), MusicVocab.create())
    test_midi.write('midi',music_gen_base_path+"input_demo.mid")
    
    res = predict_music(model, test, num_notes)
    output = idxenc2stream(res.astype("int"), MusicVocab.create())
    output.write('midi',music_gen_base_path+"output_demo.mid")

    return

def inference_music_gen(audio, num_notes):
  data_e = midi2idxenc(audio.name, MusicVocab.create())
  midi_predict(model_music_gen, data_e[:100], int(num_notes))
  return

music_gen_interface = gr.Interface(
    inference_music_gen, 
    inputs = [gr.inputs.File(type="file", label="Input"), gr.Textbox(lines = 1, placeholder = "Enter number of notes here")],
    examples=[[music_gen_base_path + "mid_file/Comic_Relief.mid", 300]],
    outputs = gr.outputs.Audio(type="filepath", label="Output")
    )

"""## Sentiment Analysis"""

def inference_sentiment_analysis(sen):
  tokenized_v1 = tokenizer_sa([sen], return_tensors="np", padding="longest")
  outputs_v1 = model_sa(tokenized_v1).logits
  classifications_v1 = np.argmax(outputs_v1, axis=1)
  if classifications_v1[0] == 1:
      res = "Positive :)"
  else:
      res = "Negative :("
  return res

sentiment_analysis_interface = gr.Interface(
    fn=inference_sentiment_analysis,
    inputs=gr.Textbox(lines=2, placeholder="Enter a Sentence"),
    outputs="text",
)

"""## Peom Generation"""

def inference_poem_gen(start):
  tokenized = tokenizer_poem_gn(start, return_tensors="np")
  outputs = model_poem_gn.generate(**tokenized, max_new_tokens=20)
  res = tokenizer_poem_gn.decode(outputs[0])
  return res.replace("<LINE>", "\n")

poem_gen_interface = gr.Interface(
    fn=inference_poem_gen,
    inputs=gr.Textbox(lines=2, placeholder="Start Here..."),
    outputs="text",
)

"""## Combine All"""

demo = gr.TabbedInterface([music_gen_interface, poem_gen_interface, sentiment_analysis_interface], 
                          ["Music Generation", "Poem Generation", "Sentiment Analysis"]) 
demo.launch(debug=True, share=True)

