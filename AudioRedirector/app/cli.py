#!/usr/bin/env python3
#coding: utf-8

from config.arguments import parse_arguments

import sounddevice as sd
import argparse
import queue
import numpy as np
#import socket

# Importer les modules définis ci-dessus
from stream.audio_file_saver import AudioFileSaver
from stream.audio_input_stream import AudioInputStream
from stream.audio_output_stream import AudioOutputStream

from audio_utils.signal_processing import get_dB_audio_signal, get_dBFS_audio_signal

from effects.audio_amplitude import get_amplitude_audio_signal, increase_gain_audio_signal, decrease_gain_audio_signal, normalize_audio_signal

from audio_processing.limiting import max_limit_dB_audio_signal
from statistical_utils.amplitude_stats import get_mean_amplitudes


AUDIO_SOURCE_AMPLITUDES = []
AUDIO_SOURCE_TRANSMIT_STATUS = False
# define a variable to store the counts of the number of times the amplitude is greater than 2.0
AUDIO_SOURCE_TRANSMIT_COUNT = 0

# audio_effect_adjust_pitch_and_speed(indata_array, pitch=1.0, speed=1.0):


def get_n_last_amplitudes(n):
    global AUDIO_SOURCE_AMPLITUDES
    return AUDIO_SOURCE_AMPLITUDES[-n:]


def keep_last_n_amplitudes(n):
    global AUDIO_SOURCE_AMPLITUDES
    return AUDIO_SOURCE_AMPLITUDES[-n:]



def is_audio_signal_transmit(n_last_amplitudes=100,
                             max_keep_last_amplitudes=200):
    global AUDIO_SOURCE_AMPLITUDES
    global AUDIO_SOURCE_TRANSMIT_STATUS
    global AUDIO_SOURCE_TRANSMIT_COUNT

    if ( len(AUDIO_SOURCE_AMPLITUDES) >= n_last_amplitudes ):
        # Calcule la moyenne des amplitudes des `n_last_amplitudes` dernières valeurs dans `AUDIO_SOURCE_AMPLITUDES`
        mean_last_amplitudes = get_mean_amplitudes(amplitudes=get_n_last_amplitudes(n=n_last_amplitudes))
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

        if ( len(AUDIO_SOURCE_AMPLITUDES) > max_keep_last_amplitudes ):
            # remove the first 5 values ( keep the last >=95 values. )
            AUDIO_SOURCE_AMPLITUDES = keep_last_n_amplitudes(n=max_keep_last_amplitudes)


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

    #udp_socket.sendto(indata.tobytes(), (udp_target_ip, udp_target_port))

    indata = increase_gain_audio_signal(indata_array, gain=12.0)


    # if ( AUDIO_SOURCE_TRANSMIT_STATUS == True ):
    #     q__audio.put(indata.copy())
    # else:
    #     q__audio.put(np.zeros_like(indata))


    q__audio.put(indata.copy())
    q__file.put(indata.copy())

def callback_audio_destination(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    if not q__audio.empty():
        outdata[:] = q__audio.get()


q__audio = queue.Queue()
q__file = queue.Queue()

# Initialisation du socket UDP
#udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#udp_target_ip = '192.168.1.2'  # Remplacer par l'adresse IP de la machine cible
#udp_target_port = 5005         # Choisir un port disponible sur la machine cible
if __name__ == '__main__':

    args = parse_arguments()

    if args.list_devices:
        print("devices:\n{0}".format(sd.query_devices()))
        parser.exit(0)

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

    exit(0)

