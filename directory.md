## Backend

`backend/itunes_utils.py`: Utility functions to interact with the iTunes API.

`backend/main.py`: Contains all server endpoints for frontend to make requests to.

`backend/model.py`: Contains the main model of the backend of the project. It provides utility for compiling the model, and making predictions by passing the trained model in.

`backend/augment_utils.py`: Utility functions to augment songs passed in form of a numpy array.

`backend/models.py`: Custom pydantic BaseModel types used to represent a Song, or a SongAugmentation.

`backend/emb1.npy`: A numpy array of the embeddings of all songs in our database.

`backend/model-checkpoints/*`: Model weights at the checkpoint we want to train.

`backend/.gitignore`: List of files (in the backend directory) not be included when pushing to GitHub.

`backend/README.md`: README for backend. Includes usage and development process.

`backend/requirements.txt`: List of python dependencies for the backend to run.

## Frontend

`frontend/src/App.css`: Contains global styling for our application.

`frontend/src/App.js`: The root endpoint for our React app. This is the main page for our Single Page Application. We utilize the material-ui library for a majority of our components.

`frontend/src/*` (Everything else): Default template React app files.

`frontend/src/components/SongCard.js`: A React component that displays info about a song in a compact card, given a song_id prop.

`frontend/package.json`: Describes this node package, with package identifying information, dependencies, and npm scripts definitions.

`frontend/public/*`: Default static files in React template

## Src

## Scripts
