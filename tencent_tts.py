# -*- coding:utf-8 -*-
import configparser
import urllib
import base64
import hmac
import hashlib
import requests
import json

TTS_URL = "tts.cloud.tencent.com/stream"
#请求参数设置,固定值
ACTION = "TextToStreamAudio"
#一次请求对应一个 SessionId，会原样返回，建议传入类似于 uuid 的字符串防止重复。
SESSION_ID=123
#模型类型，1：默认模型
MODEL=1
#音量大小，范围：[0，10]，分别对应11个等级的音量，默认值为0，代表正常音量。没有静音选项。
#输入除以上整数之外的其他参数不生效，按默认值处理
VOLUME = 5
#语速，范围：[-2，2]，分别对应不同语速：
#-2代表0.6倍
#-1代表0.8倍
#0代表1.0倍（默认）
#1代表1.2倍
#2代表1.5倍
#输入除以上整数之外的其他参数不生效，按默认值处理。
SPEED = 0
#项目 ID，用户自定义，默认为0。
PROJECT_ID = 0
#音色：
#0：亲和女声（默认）
#1：亲和男声
#2：成熟男声
#3：活力男声
#4：温暖女声
#5：情感女声
#6：情感男声
VOICE = 0
#主语言类型：
#1：中文（默认）
#2：英文
LANG = 1
#音频采样率：
#16000：16k（默认）
#8000：8k
RATE = 16000
#返回音频格式：Python SDK只支持pcm格式
#pcm：返回二进制 pcm 音频，使用简单，但数据量大。
CODEC = "pcm"
#鉴权有效时间 单位 s
#不设置默认为一小时
EXPIRED = 3600


class TencentTTS():
    def __init__(self, app_id, api_key, secret_key):
        self.app_id = int(app_id)
        self.api_key = api_key
        self.secret_key = secret_key

    def say(self, 
            text, 
            action=ACTION, 
            codec=CODEC, 
            expired=EXPIRED, 
            model=MODEL, 
            lang=LANG, 
            project_id=PROJECT_ID, 
            rate=RATE, 
            session_id=SESSION_ID, 
            speed=SPEED, 
            voice=VOICE, 
            volume=VOLUME, **kvargs):
        conf = {
        	"Action": action,
        	"Text": text,
        	"Codec": codec,
        	"Expired": expired,
        	"ModelType": model,
        	"PrimaryLanguage": lang,
        	"ProjectId": project_id,
        	"SampleRate": rate,
        	"SessionId": session_id,
        	"Speed": speed,
        	"VoiceType": voice,
        	"Volume": volume,
        }
        sign_str = "POST" + TTS_URL + "?"
        for key in conf:
            sign_str = sign_str + key + "=" + urllib.parse.unquote(str(conf[key])) + '&'
        sign_str = sign_str[:-1]
        sign_bytes = sign_str.encode('utf-8')
        key_bytes = self.secret_key.encode('utf-8')
        auth = base64.b64encode(hmac.new(key_bytes, sign_bytes, hashlib.sha1).digest()).decode('utf-8')
	    #request_data = collections.OrderedDict()
        conf['AppId'] = self.app_id
	
        header = {
            "Content-Type": "application/json",
            "Authorization": auth 
        }
	
        r = requests.post("https://"+TTS_URL, headers=header, data=json.dumps(conf), stream = True)
        print(r)
        return (True, r.content)

if __name__ == "__main__":
    tts = TencentTTS(
            app_id="1301839692", 
            api_key="AKID90e05sNO4SkohI4LVyA6qKYWKrCGRexz", 
            secret_key="SecretKey:zh8JDqHQIwJVHm04rMdcx1oKSJTN1Ip5"
    )
    (err, audio) = tts.say("tencent tts");
