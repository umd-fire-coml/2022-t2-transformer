## Backend

`emb1.npy`: The embeddings of the song.

`backend/model-checkpoints`: This contains the epoch used to train the model.

`backend/itunes_utils.py`: Pulls data from the ITunes API, and gets the song data simply using the song ID.

`backend/main.py`: Main file used to load the model, generate the augmented sound which the user requests on the frontend, and then finally call the backend to generate a prediction for the requested song.

`backend/model.py`: Contains the main model of the backend of the project. It builds the model and guesses what the user request is.

`backend/augment_utils.py`: Contains the functions to perform the user chosen augmentations on the song chosen on the frontend.

`backend/models.py`: Dependencies for the model

## Frontend

`frontend/src/App.css`: Contains global styling for our application.

`frontend/src/App.js`: The root endpoint for our React app. This is the main page for our Single Page Application. We utilize the material-ui library for a majority of our components.

`frontend/src/components/SongCard.js`: A component that displays info about a song in a compact card, given a song_id prop.

`frontend/public`: Default json and png files
