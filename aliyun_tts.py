#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020,  Magic Fang, magicfang@gmail.com
#
# Distributed under terms of the GPL-3 license.

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import requests
import hmac
import base64
import datetime
import tempfile
import shutil,os


class aliyun:
    def __init__(self, app_id = "", api_key="", secret_key=""):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
    def __time(self):
        time = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
        return time 

    def __md5_base64(self, body):
        hash = hashlib.md5()
        hash.update(body)
        str_hex = hash.digest()
        return base64.b64encode(str_hex)

    def __sha1_base64(self, str_to_sign, secret):
        hmacsha1 = hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest()).decode('utf-8')

    def say(self, text, **kvargs):
        options = {
            'method': 'POST',
            'url': 'http://nlsapi.aliyun.com/speak?encode_type=mp3&voice_name=xiaoyun&volume=50',
            'body': text.encode('utf-8')
        }
        headers = {
            'Authorization': '',
            'Content-type': 'text/plain',
            'Accept': 'audio/mp3,application/json',
            'Date': self.__time()
        }
        MD5 = self.__md5_base64(options['body']).decode('utf-8')
        feature = options['method'] + '\n' + headers['Accept'] + '\n' + MD5 + '\n' \
            + headers['Content-type'] + '\n' + headers['Date']
        signa = self.__sha1_base64(feature, self.secret_key)
        headers['Authorization'] = "Dataplus " + self.app_id + ":" + signa
        request = requests.post(options['url'], data=options['body'], headers=headers)
        print(request)

if __name__ == '__main__':
    a = aliyun()
    text="统一这一任务对欧洲来说显然要艰巨得多。"
    a.send_request(text)
