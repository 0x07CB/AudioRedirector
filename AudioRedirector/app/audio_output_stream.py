#coding: utf-8

import sounddevice as sd

class AudioOutputStream:
    def __init__(self, samplerate=48000, device=None, channels=2, blocksize=384, callback=None):
        self.samplerate = samplerate
        self.device = device
        self.channels = channels
        self.blocksize = blocksize
        self.callback = callback
        self.stream = None

    def __enter__(self):
        self.stream = sd.OutputStream(samplerate=self.samplerate,
                                      device=self.device,
                                      channels=self.channels,
                                      blocksize=self.blocksize,
                                      callback=self.callback)
        self.stream.start()
        return self.stream

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.stop()
        self.stream.close()
