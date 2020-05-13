#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020,  Magic Fang, magicfang@gmail.com
#
# Distributed under terms of the GPL-3 license.


from gtts import gTTS
from io import BytesIO

class GoogleTTS:
    def __init__(self, app_id="", api_key="", secret_key=""):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key

    def say(self, text, **kvargs):
        tts = gTTS(text)
        bfh = BytesIO()
        tts.write_to_fp(bfh)
        return (True, bfh.getvalue())


if __name__ == "__main__":
    tts = GoogleTTS()
    (err, audio) = tts.say("hello google")
    print(audio)
