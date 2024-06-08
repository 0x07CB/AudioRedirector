#coding: utf-8
import numpy as np
import sys
import queue
from audio_utils.signal_processing import get_dB_audio_signal, get_dBFS_audio_signal
from audio_processing.limiting import max_limit_dB_audio_signal
from statistical_utils.amplitude_stats import get_mean_amplitudes
from effects.audio_amplitude import get_amplitude_audio_signal, increase_gain_audio_signal, decrease_gain_audio_signal, normalize_audio_signal




q__audio = queue.Queue()
q__file = queue.Queue()

AUDIO_SOURCE_AMPLITUDES = []
AUDIO_SOURCE_TRANSMIT_STATUS = False
AUDIO_SOURCE_TRANSMIT_COUNT = 0

def callback_audio_destination(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    if not q__audio.empty():
        outdata[:] = q__audio.get()


def callback_audio_source(indata, frames, time, status):
    global AUDIO_SOURCE_AMPLITUDES
    global AUDIO_SOURCE_TRANSMIT_STATUS
    global AUDIO_SOURCE_TRANSMIT_COUNT

    if status:
        print(status)

    # I want display the audio amplitude (0.0 to 200.0)
    # First: Get indata and create a numpy array.
    # Second: Get the amplitude of the audio signal.
    # Third: Display the amplitude.

    # First
    indata_array = np.array(indata)

    # Second
    amplitude = get_amplitude_audio_signal(indata_array=indata_array)
    #AUDIO_SOURCE_AMPLITUDES.append(amplitude)

    # Third
    print(f"Amplitude: {amplitude:.2f}")

    indata = increase_gain_audio_signal(indata_array, gain=12.0)

    q__audio.put(indata.copy())
    q__file.put(indata.copy())


