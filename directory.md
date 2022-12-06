## Root

`README.md`: root level README for the project

`requirements.txt`: List of python dependencies.

`.gitignore`: Root level .gitignore file for directories and files ignored by git.

## Backend

`backend/itunes_utils.py`: Utility functions to interact with the iTunes API.

`backend/main.py`: Contains all server endpoints for frontend to make requests to.

`backend/model.py`: Contains the main model of the backend of the project. It provides utility for compiling the model, and making predictions by passing the trained model in.

`backend/augment_utils.py`: Utility functions to augment songs passed in form of a numpy array.

`backend/models.py`: Custom pydantic BaseModel types used to represent a Song, or a SongAugmentation.

`backend/emb1.npy`: A numpy array of the embeddings of all songs in our database.

`backend/model-checkpoints/*`: Model weights at the checkpoint we want to train.

`backend/.gitignore`: List of files (in the backend directory) that are ignored by git.

`backend/README.md`: README for backend. Includes usage and development process.

`backend/requirements.txt`: List of python dependencies for the backend to run.

## Frontend

`frontend/src/App.css`: Contains global styling for our application.

`frontend/src/App.js`: The root endpoint for our React app. This is the main page for our Single Page Application. We utilize the material-ui library for a majority of our components.

`frontend/src/*` (Everything else): Default template React app files.

`frontend/src/components/SongCard.js`: A React component that displays info about a song in a compact card, given a song_id prop.

`frontend/package.json`: Describes this node package, with package identifying information, dependencies, and npm scripts definitions.

`frontend/.gitignore`: List of files (in the frontend directory) that are ignored by git.

`frontend/public/*`: Default static files in React template

## markdown

`markdown/*`: Various markdown files describing different processes that help to build our root level README.

## Src

`src/model.ipynb`: The jupyter notebook we created on colab as we were building our dataset, creating and training our model

`src/triplet_gen.py`: Generates triplet files through scriping the iTunes API. This is the script used to build our dataset.

## Scripts

`scripts/download_dataset.sh`: bash script for downloading the dataset. Refer [here](markdown/download_dataset.md) for usage info.

`scripts/model_trainer.sh`: bash script that runs through the entire process of installing pip requirements and node_modules, downloading and extracting dataset, loading dataset, and training our model. Refer [here](markdown/scripts.md#training-the-model) for usage.

`scripts/model_tester.sh`: bash script that runs through the entire process of installing pip requirements and node_modules, downloading and extracting dataset, loading dataset, and using pre-trained model to test. Refer [here](markdown/scripts.md#testing-the-model) for usage.

`scripts/setup_env.sh`: bash script that creates a virtual env, and installs pip requirements and node_modules. Refer [here](markdown/setup_env.md) for usage.
