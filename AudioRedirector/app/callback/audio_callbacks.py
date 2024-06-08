#coding: utf-8
import numpy as np
from audio_utils.signal_processing import get_dB_audio_signal, get_dBFS_audio_signal
from audio_processing.limiting import max_limit_dB_audio_signal
from statistical_utils.amplitude_stats import get_mean_amplitudes

def callback_audio_source(indata, outdata, frames, time, status):
    if status:
        print(status)
    # Process the input audio signal
    dB_audio_signal = get_dB_audio_signal(indata)
    mean_amplitude = get_mean_amplitudes(dB_audio_signal)
    print(f"Mean amplitude: {mean_amplitude:.2f} dB")
    
    # Limit the audio signal
    limited_signal = max_limit_dB_audio_signal(indata)
    outdata[:] = limited_signal

def callback_audio_destination(indata, outdata, frames, time, status):
    if status:
        print(status)
    # Process the input audio signal
    dB_audio_signal = get_dB_audio_signal(indata)
    mean_amplitude = get_mean_amplitudes(dB_audio_signal)
    print(f"Mean amplitude: {mean_amplitude:.2f} dB")
    
    # Limit the audio signal
    limited_signal = max_limit_dB_audio_signal(indata)
    outdata[:] = limited_signal
