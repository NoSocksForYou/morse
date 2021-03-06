#!/usr/bin/python3
import pyaudio
import numpy as np
import time

speed = 20


class Morse(object):
    """
    Desc:
        A class of which instances contatain a string to be morsed.
    Methods:
        None
    Raises:
        True
    """
    morsechars = {
                      '0': '-----',
                      '1': '.----',
                      '2': '..---',
                      '3': '...--',
                      '4': '....-',
                      '5': '.....',
                      '6': '-....',
                      '7': '--...',
                      '8': '---..',
                      '9': '----.',
                      'a': '.-',
                      'b': '-...',
                      'c': '-.-.',
                      'd': '-..',
                      'e': '.',
                      'f': '..-.',
                      'g': '--.',
                      'h': '....',
                      'i': '..',
                      'j': '.---',
                      'k': '-.-',
                      'l': '.-..',
                      'm': '--',
                      'n': '-.',
                      'o': '---',
                      'p': '.--.',
                      'q': '--.-',
                      'r': '.-.',
                      's': '...',
                      't': '-',
                      'u': '..-',
                      'v': '...-',
                      'w': '.--',
                      'x': '-..-',
                      'y': '-.--',
                      'z': '--..',
                      '.': '.-.-.-',
                      ',': '--..--',
                      '?': '..--..',
                      '!': '-.-.--',
                      '-': '-....-',
                      '/': '-..-.',
                      '@': '.--.-.',
                      '(': '-.--.',
                      ')': '-.--.-',
                      ' ': ' '
                    }
    illegal_chars = {
                        'ä': list('ae'),
                        'ö': list('oe'),
                        'å': list('aa'),
                        ' ': list(' ')
    }

    def __init__(self, string):
        self.string = string  # the string initiation
        self.chars = list(self.string)  # a list version of the above
        self.morse_chars = Morse.MorseChar(self.chars)  # refer to the corresponding function

    def MorseChar(self):
        """
        Desc:
            converts a given string into a morse notation.
        Takes:
            Morse self
        Returns:
            list morse_chars: a list containg the corresponding morse alphabet.
        Raises:
            Exception: in case of a KeyError.
        """
        morse_chars = []
        for i in range(len(self)):
            try:
                morse_chars.append(Morse.morsechars[self[i]])
            except KeyError:
                if self[i] in Morse.illegal_chars:  # handling the illegal chars
                    for a in Morse.illegal_chars[self[i]]:
                        morse_chars.append(Morse.morsechars[a])
                else:
                    raise Exception('Error: an unspecified illegal character in stdin')
        return morse_chars

    def PlayMorse(self):
        pulse_length = None
        for i in self.morse_chars:
            if i == ' ':
                time.sleep(7 / speed)
                continue
            for a in i:
                if a == '.':
                    pulse_length = 1 / speed
                elif a == '-':
                    pulse_length = 3 / speed
                else:
                    raise Exception('Fatal: not a morse character')
                sound(pulse_length)
                time.sleep(1 / speed)
            time.sleep(2 / speed)
            # time.sleep(speed / 4)


p = pyaudio.PyAudio()  # initiate the PyAudio
stream = p.open(format=pyaudio.paFloat32,  # open the stream
                channels=1,
                rate=44100,
                output=True)


def sound(length, volume=1, frequency=700):  # sampling rate, Hz, must be integer
    global stream
    length *= 10
    fs = 44100
    samples = (np.sin(2 * np.pi * np.arange(fs * length) * frequency / fs)).astype(np.float32)
    stream.write(volume*samples)
    return None


user_input = input('string: ').lower()
chartest = Morse(user_input)
print(chartest.morse_chars)
chartest.PlayMorse()


stream.stop_stream()
stream.close()

p.terminate()  # terminate everything
