#coding: utf-8
import numpy as np
import queue
from audio_utils.signal_processing import get_dB_audio_signal, get_dBFS_audio_signal
from audio_processing.limiting import max_limit_dB_audio_signal
from statistical_utils.amplitude_stats import get_mean_amplitudes

class AudioCallbacks(object):
    def __init__(self):
        self.AUDIO_SOURCE_AMPLITUDES = []
        self.AUDIO_SOURCE_TRANSMIT_STATUS = False
        self.AUDIO_SOURCE_TRANSMIT_COUNT = 0
        self.q__audio = queue.Queue()
        self.q__file = queue.Queue()

    def callback_audio_source(self, indata, frames, time, status):
        if status:
            print(status)

        indata_array = np.array(indata)
        amplitude = self.get_amplitude_audio_signal(indata_array=indata_array)
        print(f"Amplitude: {amplitude:.2f}")

        indata = self.increase_gain_audio_signal(indata_array, gain=12.0)
        self.q__audio.put(indata.copy())
        self.q__file.put(indata.copy())

    def callback_audio_destination(self, outdata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        if not self.q__audio.empty():
            outdata[:] = self.q__audio.get()

