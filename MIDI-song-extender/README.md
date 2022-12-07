# Further Info

## Training Instructions
Training uses data located in the[google drive folder](https://drive.google.com/drive/folders/1u26zC-kGG6o9xCCJDkk5Pd8euF4CjiVD?usp=sharing). Training can be done either locally or through Google Colab. You don't need data.npy for training.

If using Google Colab:
Create a copy of the Colab notebook ["transformer training"](https://colab.research.google.com/drive/16mGM6uQ-kkLZ_vXgStZWtfSTnu0coDr-?usp=sharing).
Download the data folder and upload it to a folder in your personal google drive. 
Mount the Google drive and change the path to your folder path. Take note that this folder will also store model checkpoints.
Run the cells. If you are using a previous model, uncomment the keras.model.load_model command and change the path accordingly.
The last cell will load data in batches of 10 and call model.fit on them, then save the model. run the last cell as long as you want. You can also tune hyperparameters in the second to last cell.

If training locally:
You will need to download the data folder to a local directory. Change all filepaths as needed.
Use the generator.ipynb file in this directory. You only need to run the cells in this notebook that correspond with the cells in the Colab notebook.

## Testing Instructions
Testing also uses data located in the [google drive folder](https://drive.google.com/drive/folders/1u26zC-kGG6o9xCCJDkk5Pd8euF4CjiVD?usp=sharing). Testing can also be done either locally or through Google Colab. You don't need the data folder for training.

If using Google Colab:
Create a copy of the Colab notebook ["transformer testing"](https://colab.research.google.com/drive/1yJQdfcS7pSXwxYV0oiD0-6jvkowuLVqO?usp=sharing).
Download data.npy and upload it to a folder in your personal google drive. Make sure a suitable model is also in the folder.
Mount the Google drive and change the path to your folder path.
Run the cells and load your model, changing the path as necessary.
The midi_predict function takes 100 integers of the beginning of an encoded song as input, writes the input to input.mid, and writes the predicted output to output.mid while also returning the full integer array that got converted to output.mid. It also has some postprocessing features that ensure the predicted song is a valid MIDI encoding. We group a range of note type encodings to the number 8 because 8 encodes to a pause, which is extremely important in how the final product sounds, and previous models weren't able to predict 8 with high accuracy. The provided model should be good enough so that the features are not necessary.
We took encoded song samples from data.npy as an example. The last cell calls midi_predict on the sample. You will see the midi prediction in your drive folder.

If training locally:
You will need to download data.npy to a local directory. Change all filepaths as needed.
Use the generator.ipynb file in this directory. You only need to run the cells in this notebook that correspond with the cells in the Colab notebook.
