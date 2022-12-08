## Configuration

Before running the train, you must have `python3` and `kaggle` cli configured.

#### `kaggle` cli
- Download the cli with `pip3 install kaggle`.
- Download your API key from `https://www.kaggle.com/<your-account-username>/account`
  - Kaggle's cli expects your API key to be at `~/.kaggle/kaggle.json`.

## Training the Model
To train the model, run `bash scripts/model_trainer.sh [number of epochs]`. The default if not provided is 100. 

The paths to checkpoints should be printed as the model trains; they will be stored in the `ckpts` directory.

## Testing the Model
To test the model, run `bash scripts/model_tester.sh <path to weights> [path to embeddings]`. The path to the weights to test is required. If the embeddings for these weights have already been generated, a path to those can be provided as a second argument to save time. 

The script will run 10 tests on random augmented song snippets and display the model's best guess, as well as an indication of how high the correct guess was in the model's rankings.
