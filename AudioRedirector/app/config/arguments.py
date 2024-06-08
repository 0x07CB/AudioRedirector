#coding:utf-8
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
    parser.add_argument('-i', '--input-device', type=int, help='Input device ID')
    parser.add_argument('-o', '--output-device', type=int, help='Output device ID')
    parser.add_argument('-c', '--channels', type=int, default=2, help='Number of channels')
    parser.add_argument('--samplerate', type=int, default=48000, help='Sampling rate')
    parser.add_argument('--blocksize', type=int, default=384, help='Block size')
    return parser.parse_args()
