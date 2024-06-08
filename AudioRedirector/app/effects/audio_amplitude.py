#coding: utf-8

import numpy as np


def get_amplitude_audio_signal(indata_array):
    return np.abs(indata_array).mean() * 200



###########################
# Audio Amplitude Effects #
###########################

##########################
#   AUDIO GAIN EFFECTS   #
##########################

# Increase the gain of the audio signal
def increase_gain_audio_signal(indata_array, gain=1.0):
    return indata_array * gain

# Decrease the gain of the audio signal
def decrease_gain_audio_signal(indata_array, gain=1.0):
    return indata_array / gain

# Normalize the audio signal
def normalize_audio_signal(indata_array):
    return indata_array / np.max(np.abs(indata_array))


##########################