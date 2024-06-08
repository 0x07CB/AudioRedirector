#coding: utf-8
import numpy as np

def get_dB_audio_signal(indata_array):
    return 20 * np.log10(np.abs(indata_array))

def get_dBFS_audio_signal(indata_array):
    return 20 * np.log10(np.abs(indata_array) / np.max(np.abs(indata_array)))
