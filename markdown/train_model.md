A list of step-by-step instructions to train the model to get the trained model weights.

1. Build and compile model (Described by model architecture diagram)
1. Load dataset
    - ClipTripletGenerator: generator yielding anchor, positive, negative triplets from the dataset we created
    - Create train, test, and validation sets