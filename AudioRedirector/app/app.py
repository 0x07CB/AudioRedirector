#!/usr/bin/env python3
import socket
import numpy as np
from copy import deepcopy
import io
import tempfile
import argparse
import queue
import sys
import os
import time as t
import subprocess
import soundfile as sf
import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

def in_memory_audio_file(data: bytes):
    buffer_ = io.BytesIO(data)
    buffer_.name = 'in_memory_audio_file.wav'
    buffer_.seek(0)
    data, samplerate = sf.read(buffer_)
    return data, samplerate

def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

def get_list_of_devices():
    return sd.query_devices()

def show_list_of_devices():
    subprocess.call(["clear"],shell=True)
    print("LIST OF AVAILABLE AUDIO DEVICES:\n{0}\n\n".format(get_list_of_devices()))

def get_device_id(device_name):
    devices = list(get_list_of_devices())
    for device in devices:
        if device_name in device['name']:
            return device['index']
    return None

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def raise_kb_interrupt():
    raise KeyboardInterrupt



# #############################################################################

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print("devices:\n{0}".format(sd.query_devices()))
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-c', '--channels', type=int, default=2,
    help='number of channels')
parser.add_argument('--dtype', default='int16',
                    help='audio data type')
parser.add_argument('--samplerate', type=int, default=48000,
                    help='sampling rate')
parser.add_argument('--blocksize', type=int, default=384,
                    help='block size')
parser.add_argument('--latency', type=float, default=None,
                    help='latency in seconds')
args = parser.parse_args(remaining)

# #############################################################################

filename_ = None 
if filename_ is None: 
    filename_ = tempfile.mktemp(prefix='sounddevice-', suffix='.wav', dir='')

q__audio = queue.Queue()
q__file = queue.Queue()

# create a empty ndarray
PCM_AUDIO_DATA = []



def callback_audio_source(indata, frames, time, status):
    global PCM_AUDIO_DATA
    global filename_i
    if status:
        print(status)
    #
    #
    def vumetre__no_color(audio_data):
    #   #
    #   #
        def audio_norm(audio_data):
    #       #
            return numpy.linalg.norm(audio_data) * 10
    #   
        volume_norm = audio_norm(audio_data)
        ## now I want volume_norm to be a value between 0.0 and 100.0
        volume_norm = float( (volume_norm * 100) / 10 )
        

        print("\r\r{0}".format("|" * int(volume_norm)), end=' ')

    q__audio.put(indata.copy())
    q__file.put(indata.copy())

    # Convert the data to a NumPy array
    #audio_data = numpy.frombuffer(indata, dtype=numpy.float32)
    
    new_audio_data = indata.copy().astype(numpy.int16)
    new_audio_data_bytes = new_audio_data.tobytes()

    # Calculate energy (RMS) for each frame
    energy_values  = numpy.sqrt(numpy.mean(new_audio_data**2, axis=1))
    
def callback_audio_destination(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    
    if not q__audio.empty():
        # read the data from the queue without remove it
        first_outdata = q__audio.queue[0]
        first_outdata_shape = first_outdata.shape
        
        if first_outdata_shape == outdata.shape:
            in_array = q__audio.get()
            outdata[:] = in_array

try:
    with sf.SoundFile(filename_, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype='PCM_16') as file:
        with sd.InputStream(samplerate=args.samplerate,
                        device=args.input_device, 
                        channels=args.channels,
                        blocksize=args.blocksize,
                        callback=callback_audio_source) as source:
            with sd.OutputStream(samplerate=args.samplerate, 
                             device=args.output_device, 
                             channels=args.channels,
                             blocksize=args.blocksize,
                             callback=callback_audio_destination) as destination:

                print('#' * 80)
                print('Press <Ctrl+C> to quit')
                print('#' * 80)
                while True:
                    file.write(q__file.get())


except KeyboardInterrupt:
    parser.exit('')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
