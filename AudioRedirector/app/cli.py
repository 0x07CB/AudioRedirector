#!/usr/bin/env python3
#coding: utf-8
import sounddevice as sd
import argparse
import queue
import numpy as np
#import socket

# Importer les modules définis ci-dessus
from audio_file_saver import AudioFileSaver
from audio_input_stream import AudioInputStream
from audio_output_stream import AudioOutputStream

AUDIO_SOURCE_AMPLITUDES = []
AUDIO_SOURCE_TRANSMIT_STATUS = False
# define a variable to store the counts of the number of times the amplitude is greater than 2.0
AUDIO_SOURCE_TRANSMIT_COUNT = 0

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
    amplitude = np.abs(indata_array).mean() * 200
    AUDIO_SOURCE_AMPLITUDES.append(amplitude)

    # Third
    print(f"Amplitude: {amplitude:.2f}")

    #udp_socket.sendto(indata.tobytes(), (udp_target_ip, udp_target_port))
    
    
    if ( len(AUDIO_SOURCE_AMPLITUDES) >= 100 ):
        # Calcule la moyenne des amplitudes des 10 dernières valeurs dans `AUDIO_SOURCE_AMPLITUDES`
        mean_last_amplitudes = np.mean(AUDIO_SOURCE_AMPLITUDES[-100:])
        if mean_last_amplitudes >= 2.0:
            AUDIO_SOURCE_TRANSMIT_COUNT += 1
            if ( AUDIO_SOURCE_TRANSMIT_COUNT > 100 ):
                AUDIO_SOURCE_TRANSMIT_COUNT = 100

            if ( AUDIO_SOURCE_TRANSMIT_STATUS == False ):
                if ( AUDIO_SOURCE_TRANSMIT_COUNT >= 5 ):
                    AUDIO_SOURCE_TRANSMIT_STATUS = True
                    AUDIO_SOURCE_TRANSMIT_COUNT = 20
        else:
            if ( AUDIO_SOURCE_TRANSMIT_STATUS == False ):
                AUDIO_SOURCE_TRANSMIT_COUNT = 0
            else:
                AUDIO_SOURCE_TRANSMIT_COUNT -= 1
                if ( AUDIO_SOURCE_TRANSMIT_COUNT < 0 ):
                    AUDIO_SOURCE_TRANSMIT_COUNT = 0

                if ( AUDIO_SOURCE_TRANSMIT_COUNT < 15 ):
                    AUDIO_SOURCE_TRANSMIT_STATUS = False
                    AUDIO_SOURCE_TRANSMIT_COUNT = 0

        if ( len(AUDIO_SOURCE_AMPLITUDES) >= 200 ):
            # remove the first 5 values ( keep the last >=95 values. )
            AUDIO_SOURCE_AMPLITUDES = AUDIO_SOURCE_AMPLITUDES[-195:]



    if ( AUDIO_SOURCE_TRANSMIT_STATUS == True ):
        q__audio.put(indata.copy())
    else:
        q__audio.put(np.zeros_like(indata))

    q__file.put(indata.copy())

def callback_audio_destination(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    if not q__audio.empty():
        outdata[:] = q__audio.get()

# Configuration des arguments et des variables
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
parser.add_argument('-i', '--input-device', type=int, help='Input device ID')
parser.add_argument('-o', '--output-device', type=int, help='Output device ID')
parser.add_argument('-c', '--channels', type=int, default=2, help='Number of channels')
parser.add_argument('--samplerate', type=int, default=48000, help='Sampling rate')
parser.add_argument('--blocksize', type=int, default=384, help='Block size')
args = parser.parse_args()

if args.list_devices:
    print("devices:\n{0}".format(sd.query_devices()))
    parser.exit(0)

q__audio = queue.Queue()
q__file = queue.Queue()

# Initialisation du socket UDP
#udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#udp_target_ip = '192.168.1.2'  # Remplacer par l'adresse IP de la machine cible
#udp_target_port = 5005         # Choisir un port disponible sur la machine cible

try:
    with AudioFileSaver(samplerate=args.samplerate, channels=args.channels) as file:
        with AudioInputStream(samplerate=args.samplerate, device=args.input_device,
                              channels=args.channels, blocksize=args.blocksize,
                              callback=callback_audio_source) as source:
            with AudioOutputStream(samplerate=args.samplerate, device=args.output_device,
                                   channels=args.channels, blocksize=args.blocksize,
                                   callback=callback_audio_destination) as destination:
                print('#' * 80)
                print('Press <Ctrl+C> to quit')
                print('#' * 80)
                while True:
                    file.write(q__file.get())
except KeyboardInterrupt:
    #udp_socket.close()
    print("Program interrupted by user.")
except Exception as e:
    #udp_socket.close()
    print(f"An error occurred: {type(e).__name__} - {e}")

