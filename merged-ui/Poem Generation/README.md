# Poem Generation

## System Architecture
![High Level System Architecture](system_arch_pg.png)
## Model Architecture
![High Level System Architecture](model_arch2.png)

## Directory Guide
UI_poem_gen.ipynb: Colab notebook to create gradio UI just for poem generation application.  

poem generation.ipynb: Colab notebook for end-to-end. From procession to model training. 

system_arch_pg.png, model_arch2.png: files for system and model architecture visualization

## Pretrained Models
Please find pretrained models here: https://drive.google.com/drive/folders/1-KgkDgnv6qY5G6_Y4lZ2dkNcXEub-V39?usp=sharing

## Training Instructions
##### For Google Colab:

Create a copy of the Colab notebook poem generation.ipynb.

The notebook is self sufficient. We are insatlling all the required packages and dowloading required datasets in the notebook.

Mount the Google drive and change the path to your folder to save checkpoints and the model after training.

Run the cells. 

## Testing Instructions
##### For Google Colab:

Create a copy of the Colab notebook poem generation.ipynb.

Mount the Google drive and change the path to your folder path.

Make sure your folder path contains pre-trained model.

Run model performance and inference cells, changing the path as necessary.

## Works Cited
##### Research Work
[1] A Gutenberg Poetry Corpus https://github.com/aparrish/gutenberg-poetry-corpus

[2] Hugging Face, "DistilGPT2" [https://huggingface.co/distilroberta-base](https://huggingface.co/distilgpt2)


##### Article from the Internet
[4] Hugging face transformers package https://huggingface.co/docs/transformers/index

[5] Gradio https://gradio.app/