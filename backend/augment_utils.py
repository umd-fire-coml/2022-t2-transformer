import librosa
import numpy as np


def augment_noise(sound, noise_value: float):
    y_noise = sound.copy()
    noise_amp = noise_value * np.random.uniform() * np.amax(y_noise)
    y_noise = y_noise.astype('float64') + noise_amp * \
        np.random.normal(size=y_noise.shape[0])
    return y_noise


def augment_pitch(sound, pitch_value: int, samplerate: int):
    return librosa.effects.pitch_shift(sound, samplerate, pitch_value)


def augment_speed(sound, speed_value: float):
    return librosa.effects.time_stretch(sound, speed_value)
