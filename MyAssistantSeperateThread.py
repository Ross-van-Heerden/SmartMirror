#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library with button support.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import sys
import threading

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.voicehat
from google.assistant.library.event import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


class GoogleAssistant(object):
    """An assistant that runs in the background.

    The Google Assistant Library event loop blocks the running thread entirely.
    To support the button trigger, we need to run the event loop in a separate
    thread. Otherwise, the on_button_pressed() method will never get a chance to
    be invoked.
    """

    def __init__(self):
        self._task = threading.Thread(target=self._run_task)
        self._can_start_conversation = False
        self._assistant = None

    def start(self):
        """Starts the assistant.

        Starts the assistant event loop and begin processing events.
        """
        self._task.start()

    def _run_task(self):
        recognizer = aiy.cloudspeech.get_recognizer()
        recognizer.expect_phrase('turn off the light')
        recognizer.expect_phrase('turn on the light')
        recognizer.expect_phrase('blink')

        button = aiy.voicehat.get_button()
        led = aiy.voicehat.get_led()
        aiy.audio.get_recorder().start()

        while True:
            print('Press the button and speak')
            button.wait_for_press()
            print('Listening...')
            text = recognizer.recognize()
            if not text:
                print('Sorry, I did not hear you.')
            else:
                print('You said "', text, '"')
                if 'turn on the light' in text:
                    led.set_state(aiy.voicehat.LED.ON)
                elif 'turn off the light' in text:
                    led.set_state(aiy.voicehat.LED.OFF)
                elif 'blink' in text:
                    led.set_state(aiy.voicehat.LED.BLINK)
                elif 'goodbye' in text:
                    break


def main():
    GoogleAssistant().start()


if __name__ == '__main__':
    main()

