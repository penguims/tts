# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、ent=mtts、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from websocket import WebSocketApp
import _thread as thread
import os
import argparse


STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

TTS_URL = 'wss://tts-api.xfyun.cn/v2/tts'

AUE = {
    'pcm': 'raw',
    'mp3': 'lame',
    'speex-org-wb;7': 'speex16k',
    'speex-org-nb;7': 'speex8k',
    'speex;7': 'speex8k',
    'speex-wb;7': 'speex16k',
}

VCN = {
    '讯飞小燕': 'xiaoyan',
    '讯飞徐久': 'aisjiuxu',
    '讯飞小萍': 'aisxping',
    '讯飞小婧': 'aisjinger',
    '讯飞许小宝': 'aisbabyxu'
}

SFL = 1

SPD = 5
PIT = 5
VOL = 5


class XunfeiTTS(WebSocketApp):
    def __init__(self, app_id, api_key, secret_key):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key

        # 公共参数(common)
        self.args = {"app_id": self.app_id}
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.secret_key.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        self.url = TTS_URL + '?' + urlencode(v)
        super().__init__(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close)
        self.audio = None

    def on_message(self, message):
#        print("---on message---")
        try:
            message =json.loads(message)
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
#            print(message)
            if message['data']['status'] == 2:
#                print("ws is closed")
                self.close()
            if message['code'] != 0:
                print("sid:%s call error:%s code is:%s" % (message['sid'], message["message"], message['code']))
            else:
#                print("get audio stream")
                self.audio = audio
        except Exception as e:
            print("receive msg,but parse exception:", e)

    def on_error(self, error):
        print("### error:", error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        def run(*args):
            d = {
                "common": self.args,
                "business": self.business,
                "data": self.data,
            }
            d = json.dumps(d)
#            print("send data")
            self.send(d)
            if self.audio:
                self.audio = None
        thread.start_new_thread(run, ())
    

    def say(self, text, aue='mp3', vcn='讯飞小燕', auf="audio/L16;rate=16000", tte="utf8", ent="aisound", **kargs):
        # 业务参数(business)，更多个性化参数可在官网查看
        self.business = {"aue": AUE[aue], "auf": auf, "vcn": VCN[vcn], "tte": tte, "ent":ent}
        if aue == 'lame':
            self.business["sfl"] = SFL
        self.data = {"status": 2, "text": str(base64.b64encode(text.encode('utf-8')), "UTF8")}
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}
        websocket.enableTrace(False)
        self.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return (True, self.audio)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", default="hello world!")
    parser.add_argument("-o", "--output", default="xunfei.mp3")
    parser.add_argument("-a", "--app_id")
    parser.add_argument("-k", "--api_key")
    parser.add_argument("-s", "--secret_key")
    args = parser.parse_args()
    tts = XunfeiTTS(
            app_id=args.app_id, 
            api_key=args.api_key,
            secret_key=args.secret_key,
        )
    (err_msg, audio) = tts.say(args.text, vcn='讯飞许小宝')
    if audio:
        with open(args.output, "wb") as fh:
            fh.write(audio)
    else:
        print("not tts audio!")
