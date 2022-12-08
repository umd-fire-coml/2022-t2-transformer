# Usage: model_trainer.py <number of epochs>
from model import compile_model
import os
import sys
import numpy as np
from tensorflow import TensorSpec, dtypes
from tensorflow.data import Dataset, AUTOTUNE
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

INPUT_SHAPE = (1025, 130)
TRAIN_SIZE = 900
VAL_SIZE = 100
CKPTS_PATH = 'ckpts'

num_epochs = sys.argv[1]

# load compiled model
model = compile_model()

# Show summary for compiled model
print(model.summary())

# Triplet Generator Class
class ClipTripletGenerator():
    def __init__(self, triplet_dir, batch_size=4, input_shape=INPUT_SHAPE):
        self.triplet_dir = triplet_dir
        self.batch_size = batch_size
        self.input_shape = input_shape

    def generate(self):
        for triplet in os.listdir(self.triplet_dir):
            try:
                a, p, n = np.load(os.path.join(self.triplet_dir, triplet), allow_pickle=True)
            except:
                print(f'Failed to load {triplet}')
                continue
            yield (a, p, n), None

    def get_generator(self):
        inp_ts = TensorSpec(self.input_shape, dtypes.float32)
        datagen = Dataset.from_generator(
                      self.generate, 
                      output_signature=((inp_ts, inp_ts, inp_ts), TensorSpec(None))
                  )
        return datagen.batch(self.batch_size).prefetch(AUTOTUNE)


# loading dataset with generator
gen = ClipTripletGenerator('triplets')
generator = gen.get_generator()
train_set = generator.take(TRAIN_SIZE)
test_set = generator.skip(TRAIN_SIZE)
val_set = test_set.take(VAL_SIZE)
test_set = test_set.skip(VAL_SIZE)

# train model
history = model.fit(train_set, 
    epochs=num_epochs,
    validation_data=val_set,
    callbacks=[
        ModelCheckpoint(
            filepath=os.path.join(CKPTS_PATH, 'epoch{epoch:03d}_loss{loss:.3f}.hdf5'),
            save_best_only=True,
            mode='auto',
            save_weights_only=True,
            verbose=True
        ),
        EarlyStopping(
            mode='auto',
            patience=15,
            verbose=True
        )
    ]
)
