#!/usr/bin/env python
# coding: utf-8

# In[4]:



# In[5]:

# In[6]:


import gradio as gr
from pathlib import Path
import subprocess
from transformers import AutoTokenizer
from transformers import TFAutoModelForCausalLM
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import numpy as np


# In[7]:


#load poem generation model
model = TFAutoModelForCausalLM.from_pretrained('drive/MyDrive/FIRE_3rd Sem/peom_gn/')
base_model = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(base_model)


# In[8]:


#load sentiment analysis
model_v1 = TFAutoModelForSequenceClassification.from_pretrained('drive/MyDrive/FIRE_3rd Sem/sen_analysis/bert')
base_model = "distilbert-base-uncased"
tokenizer_v1 = AutoTokenizer.from_pretrained(base_model)


# In[9]:


#music generation
base_path = "/content/drive/MyDrive/FIRE_3rd Sem/music_gn/"
#path_mid_file -> Replace this with model generated file path
path_mid_file = base_path + "Comic_Relief.mid"
path_wav_file = base_path + "output_comic.wav"
subprocess.call(['timidity', path_mid_file, "-Ow", "-o", path_wav_file])


# ## Music Generation

# In[10]:


def inference_music_gen():
  return Path(path_wav_file)


# In[13]:


music_gen_interface = gr.Interface(
    inference_music_gen, 
    inputs = None, 
    outputs = gr.outputs.Audio(type="filepath", label="Output")
    )


# ## Sentiment Analysis

# In[14]:


def inference_sentiment_analysis(sen):
  tokenized_v1 = tokenizer_v1([sen], return_tensors="np", padding="longest")
  outputs_v1 = model_v1(tokenized_v1).logits
  classifications_v1 = np.argmax(outputs_v1, axis=1)
  if classifications_v1[0] == 1:
      res = "Positive :)"
  else:
      res = "Negative :("
  return res


# In[15]:


sentiment_analysis_interface = gr.Interface(
    fn=inference_sentiment_analysis,
    inputs=gr.Textbox(lines=2, placeholder="Enter a Sentence"),
    outputs="text",
)


# ## Peom Generation

# In[16]:


def inference_poem_gen(start):
  tokenized = tokenizer(start, return_tensors="np")
  outputs = model.generate(**tokenized, max_new_tokens=20)
  res = tokenizer.decode(outputs[0])
  return res.replace("<LINE>", "\n")


# In[17]:


poem_gen_interface = gr.Interface(
    fn=inference_poem_gen,
    inputs=gr.Textbox(lines=2, placeholder="Start Here..."),
    outputs="text",
)


# ## Combine All

# In[18]:


title = "Music Generation"
description = "Add Project description"
article = "<p style='text-align: center'><a href='https://github.com/' target='_blank'>Github Repo</a></p>"
#we can add other project related stuff as well

demo = gr.TabbedInterface([music_gen_interface, poem_gen_interface, sentiment_analysis_interface], 
                          ["Music Generation", "Poem Generation", "Sentiment Analysis"])
demo.launch(debug=True, share=True)


# In[ ]:




