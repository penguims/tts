#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020,  Magic Fang, magicfang@gmail.com
#
# Distributed under terms of the GPL-3 license.

'''
程序思想：
有两个本地语音库，美音库Speech_US，英音库Speech_US
调用有道api，获取语音MP3，存入对应的语音库中
'''

import os
from urllib.request import urlopen
from urllib.parse import urlencode

AUE={
    '美音': 0,
    '英音': 1,
}

TTS_URL = "http://dict.youdao.com/dictvoice"

class YoudaoTTS():
    def __init__(self, app_id="", api_key="", secret_key=""):
        '''
        调用youdao API
        type = 0：美音
        type = 1：英音

        判断当前目录下是否存在两个语音库的目录
        如果不存在，创建
        '''
        pass

    def say(self, text="", aue="美音", **kargs):
        '''
        下载单词的MP3
        判断语音库中是否有对应的MP3
        如果没有就下载
        '''
        url = "{}?{}".format(TTS_URL, urlencode({'type': AUE[aue], 'audio': text}))
        audio = None
        with urlopen(url) as fh:
            audio = fh.read()
        return (True, audio)

if __name__ == "__main__":

    tts = YoudaoTTS()
    audio = tts.say(text="hello, 你好")
    with open("hello.mp3", "wb") as fh:
        fh.write(audio)
