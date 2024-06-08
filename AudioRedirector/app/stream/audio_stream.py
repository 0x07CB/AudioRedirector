#coding: utf-8

import sounddevice as sd
import soundfile as sf
import tempfile

from callbacks.audio_callbacks import *

class AudioFileSaver:
    def __init__(self, filename=None, samplerate=48000, channels=2):
        self.filename = filename or tempfile.mktemp(prefix='sounddevice-', suffix='.wav', dir='')
        self.samplerate = samplerate
        self.channels = channels
        self.file = None

    def __enter__(self):
        self.file = sf.SoundFile(self.filename, mode='x', samplerate=self.samplerate,
                                 channels=self.channels, subtype='PCM_16')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file is not None:
            self.file.close()
            self.file = None

class AudioOutputStream:
    def __init__(self, samplerate=48000, device=None, channels=2, blocksize=384):
        self.samplerate = samplerate
        self.device = device
        self.channels = channels
        self.blocksize = blocksize
        self.stream = None

    def __enter__(self):
        self.stream = sd.OutputStream(samplerate=self.samplerate,
                                      device=self.device,
                                      channels=self.channels,
                                      blocksize=self.blocksize,
                                      callback=callback_audio_destination)
        self.stream.__enter__()
        return self.stream

    def __exit__(self, exc_type, exc_value, traceback):
        if self.stream is not None:
            self.stream.__exit__(exc_type, exc_value, traceback)

class AudioInputStream:
    def __init__(self, samplerate=48000, device=None, channels=2, blocksize=384):
        self.samplerate = samplerate
        self.device = device
        self.channels = channels
        self.blocksize = blocksize
        self.stream = None

    def __enter__(self):
        self.stream = sd.InputStream(samplerate=self.samplerate,
                                     device=self.device,
                                     channels=self.channels,
                                     blocksize=self.blocksize,
                                     callback=callback_audio_source)
        self.stream.__enter__()
        return self.stream

    def __exit__(self, exc_type, exc_value, traceback):
        if self.stream is not None:
            self.stream.__exit__(exc_type, exc_value, traceback)
