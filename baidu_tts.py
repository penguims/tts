# coding=utf-8
import sys
import json
import argparse

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
PER = {
    "度小美": 0,
    "度小宇": 1,
    "度逍遥": 3,
    "度丫丫": 4,
    "度小娇": 5,
    "度小朵": 103,
    "度博文": 106,
    "度小童": 110,
    "度小萌": 111,
}
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = {
    'mp3': 3,
    'pcm-16k': 4,
    'pcm-8k': 5,
    'wav': 6,
}

TTS_URL = 'http://tsn.baidu.com/text2audio'

class DemoError(Exception):
    pass

"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  

class BaiduTTS:
    def __init__(self, app_id=None, api_key=None, secret_key=None):
        self.app_id = app_id
        params = {'grant_type': 'client_credentials',
              'client_id': api_key,
              'client_secret': secret_key}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print('token http response http code : ' + str(err.code))
            result_str = err.read()
        if (IS_PY3):
            result_str = result_str.decode()

        result = json.loads(result_str)
        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not SCOPE in result['scope'].split(' '):
                raise DemoError('scope is not correct')
            self.token = result['access_token']
        else:
            raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

    def say(self, text="", lan="zh", per=PER['度逍遥'], speed=SPD, pit=PIT, vol=VOL, aue=AUE['mp3'], **kargs):
        tex = quote_plus(text)
        params = {
            'tok': self.token, 
            'tex': tex, 
            'per': per, 
            'spd': speed, 
            'pit': pit, 
            'vol': vol, 
            'aue': aue, 
            'cuid': self.app_id,
            'lan': 'zh', 
            'ctp': 1
        }
        data = urlencode(params)
        req = Request(TTS_URL, data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
            headers = dict((name.lower(), value) for name, value in f.headers.items())
            has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
        except  URLError as err:
            print('asr http response http code : ' + str(err.code))
            result_str = err.read()
            has_error = True
        if has_error:
            if (IS_PY3):
                result_str = str(result_str, 'utf-8')
        return (has_error, result_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", required="yes")
    parser.add_argument("-o", "--output")
    parser.add_argument("-a", "--api_key", required="yes")
    parser.add_argument("-s", "--secret_key", required="yes")
    parser.add_argument("-c", "--app_id", default="baidu_tts_demo")
    args = parser.parse_args()

    tts = BaiduTTS(args.api_key, args.secret_key, args.app_id)
    (error_code, content) = tts.say(args.text)

    if args.output:
        with open(args.output, "wb") as fh:
            fh.write(content)
