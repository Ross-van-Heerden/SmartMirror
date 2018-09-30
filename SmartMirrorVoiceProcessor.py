#!/usr/bin/env python3

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

# My Google Assistant class
import GoogleAssistant

# Multi processing library to start Google Assistant and my voice recognizer at the same time in main
from multiprocessing import Process


def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('hello')
    recognizer.expect_phrase('use Google Assistant to')

    aiy.audio.get_recorder().start()

    while True:
        print('waiting for activation trigger')
        wait_for_activation_trigger(recognizer)
        print('Listening...')
        text = recognizer.recognize()
        if not text:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            if 'goodbye' in text:
                break


# Custom activation trigger
def wait_for_activation_trigger(recognizer):
    while True:
        text = recognizer.recognize()
        if 'hello' in text:
            break


if __name__ == '__main__':
    main()
    # p1 = Process(target=main)
    # p1.start()
    # p2 = Process(target=GoogleAssistant.main)
    # p2.start()
    # p1.join()
    # p2.join()
