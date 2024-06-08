#coding: utf-8

import soundfile as sf
import tempfile

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