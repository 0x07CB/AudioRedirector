#coding: utf-8
import numpy as np
from audio_utils.signal_processing import get_dB_audio_signal

def max_limit_dB_audio_signal(indata_array, max_dB=0.0):
    # Get the dB of the audio signal
    dB_audio_signal = get_dB_audio_signal(indata_array=indata_array)
    # If `dB_audio_signal` is greater than `max_dB`, then adjust all values in `indata_array`.
    return np.where(dB_audio_signal > max_dB, max_dB, indata_array)
