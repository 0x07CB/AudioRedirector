#!/usr/bin/env python3
#coding: utf-8

import asyncio
import sys

from time import sleep
from config.arguments import parse_arguments


import sounddevice as sd


import numpy as np
#import socket

# Importer les modules définis ci-dessus
from stream.audio_file_saver import AudioFileSaver
from stream.audio_input_stream import AudioInputStream
from stream.audio_output_stream import AudioOutputStream

from callbacks.audio_callbacks import AudioCallbacks


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


async def create_audio_file_saver(samplerate, channels):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    stream = AudioFileSaver(samplerate=samplerate, channels=channels)

    with stream:
        await event.wait()

async def create_audio_input_stream(samplerate, channels, device, blocksize, callback):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    stream = AudioInputStream(samplerate=samplerate, device=device, channels=channels, blocksize=blocksize, callback=callback)

    with stream:
        await event.wait()

async def create_audio_output_stream(samplerate, channels, device, blocksize, callback):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    stream = AudioOutputStream(samplerate=samplerate, device=device, channels=channels, blocksize=blocksize, callback=callback)

    with stream:
        await event.wait()

async def main():
    Parser = parse_arguments()
    args = Parser.parse_args()

    if args.list_devices:
        print("devices:\n{0}".format(sd.query_devices()))
        Parser.exit(0)

    audio_callbacks = AudioCallbacks()



    # Utilisation des fonctions dans le code principal
    try:
        #create_audio_file_saver(args.samplerate, args.channels)
        await create_audio_input_stream(args.samplerate, args.channels, args.input_device, args.blocksize, audio_callbacks.callback_audio_source)
        await create_audio_output_stream(args.samplerate, args.channels, args.output_device, args.blocksize, audio_callbacks.callback_audio_destination)
        
        #with  source, destination:
        print('#' * 80)
        print('Press <Ctrl+C> to quit')
        print('#' * 80)
        while True:
            #file.write(audio_callbacks.q__file.get())
            sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {type(e).__name__} - {e}")

    exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')