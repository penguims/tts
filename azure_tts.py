'''
After you've set your subscription key, run this application from your working
directory with this command: python TTSSample.py
'''
import os, requests, time
from xml.etree import ElementTree

# This code is required for Python 2.7
try: input = raw_input
except NameError: pass

'''
If you prefer, you can hardcode your subscription key as a string and remove
the provided conditional statement. However, we do recommend using environment
variables to secure your subscription keys. The environment variable is
set to SPEECH_SERVICE_KEY in our sample.

For example:
subscription_key = "Your-Key-Goes-Here"
'''

TTS_URL = ''
OUT_FMTS = {
    'default': 'mp3-16k-32k',
    'raw-16k': 'raw-16khz-16bit-mono-pcm',
    'raw-8k': 'raw-8khz-8bit-mono-mulaw',
    'riff-8k': 'riff-8khz-8bit-mono-alaw',
    'riff-8k-m': 'riff-8khz-8bit-mono-mulaw',
    'riff-16k': 'riff-16khz-16bit-mono-pcm',
    'mp3-16k-128k': 'audio-16khz-128kbitrate-mono-mp3',
    'mp3-16k-64k': 'audio-16khz-64kbitrate-mono-mp3',
    'mp3-16k-32k': 'audio-16khz-32kbitrate-mono-mp3',
    'raw-24k': 'raw-24khz-16bit-mono-pcm',
    'riff-24k': 'riff-24khz-16bit-mono-pcm',
    'mp3-24k-160k': 'audio-24khz-160kbitrate-mono-mp3',
    'mp3-24k-96k': 'audio-24khz-96kbitrate-mono-mp3',
    'mp3-24k-48k': 'audio-24khz-48kbitrate-mono-mp3',
}

LANGS = {
    "default": "en",
    "zh": "zh-CN",
    "en": "en-US",
    "uk": "en-UK",
}

VOICES = {
        "default": "zh-HuhuiRUS",
#        "ar-Hoda": "ar-EG-Hoda",
#        "ar-Naayf": "ar-SA-Naayf",
#	"": "bg-BG-Ivan"
#	"": "ca-ES-HerenaRUS"
#	"": "cs-CZ-Jakub"
#	"": "da-DK-HelleRUS"
#	"": "de-AT-Michael"
#	"": "de-CH-Karsten"
#	"": "de-DE-Hedda"
#	"": "de-DE-HeddaRUS"
#	"": "de-DE-Stefan-Apollo"
#	"": "el-GR-Stefanos"
#	"": "en-AU-Catherine"
#	"": "en-AU-HayleyRUS"
#	"": "en-CA-Linda"
#	"": "en-CA-HeatherRUS"
#	"": "en-GB-Susan-Apollo"
#	"": "en-GB-HazelRUS"
#	"": "en-GB-George-Apollo"
#	"": "en-IE-Sean"
#	"": "en-IN-Heera-Apollo"
#	"": "en-IN-PriyaRUS"
#	"": "en-IN-Ravi-Apollo"
#	"": "en-US-ZiraRUS"
#	"": "en-US-AriaRUS"
#	"": "en-US-BenjaminRUS"
#	"": "en-US-Guy24kRUS"
#	"": "es-ES-Laura-Apollo"
#	"": "es-ES-HelenaRUS"
#	"": "es-ES-Pablo-Apollo"
#	"": "es-MX-HildaRUS"
#	"": "es-MX-Raul-Apollo"
#	"": "fi-FI-HeidiRUS"
#	"": "fr-CA-Caroline"
#	"": "fr-CA-HarmonieRUS"
#	"": "fr-CH-Guillaume"
#	"": "fr-FR-Julie-Apollo"
#	"": "fr-FR-HortenseRUS"
#	"": "fr-FR-Paul-Apollo"
#	"": "he-IL-Asaf"
#	"": "hi-IN-Kalpana-Apollo"
#	"": "hi-IN-Kalpana"
#	"": "hi-IN-Hemant"
#	"": "hr-HR-Matej"
#	"": "hu-HU-Szabolcs"
#	"": "id-ID-Andika"
#	"": "it-IT-Cosimo-Apollo"
#	"": "it-IT-LuciaRUS"
#	"": "ja-JP-Ayumi-Apollo"
#	"": "ja-JP-Ichiro-Apollo"
#	"": "ja-JP-HarukaRUS"
#	"": "ko-KR-HeamiRUS"
#	"": "ms-MY-Rizwan"
#	"": "nb-NO-HuldaRUS"
#	"": "nl-NL-HannaRUS"
#	"": "pl-PL-PaulinaRUS"
#	"": "pt-BR-HeloisaRUS"
#	"": "pt-BR-Daniel-Apollo"
#	"": "pt-PT-HeliaRUS"
#	"": "ro-RO-Andrei"
#	"": "ru-RU-Irina-Apollo"
#	"": "ru-RU-Pavel-Apollo"
#	"": "ru-RU-EkaterinaRUS"
#	"": "sk-SK-Filip"
#	"": "sl-SI-Lado"
#	"": "sv-SE-HedvigRUS"
#	"": "ta-IN-Valluvar"
#	"": "te-IN-Chitra"
#	"": "th-TH-Pattara"
#	"": "tr-TR-SedaRUS"
#	"": "vi-VN-An"
	"zh-HuhuiRUS": "zh-CN-HuihuiRUS",
	"zh-Yaoyao": "zh-CN-Yaoyao-Apollo",
	"zh-Kangkang": "zh-CN-Kangkang-Apollo",
#	"": "zh-HK-Tracy-Apollo"
#	"": "zh-HK-TracyRUS"
#	"": "zh-HK-Danny-Apollo"
#	"": "zh-TW-Yating-Apollo"
#	"": "zh-TW-HanHanRUS"
#        "": "zh-TW-Zhiwei-Apollo"
}


class AzureTTS(object):
    def __init__(self, app_id="", api_key="", secret_key=""):
        self.api_key = api_key
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

        '''
        The TTS endpoint requires an access token. This method exchanges your
        subscription key for an access token that is valid for ten minutes.
        '''
        fetch_token_url = "https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
            #'Authorization': 'Bearer '+self.api_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def say(self, text, **kvargs):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': OUT_FMTS[OUT_FMTS['default']],
            'User-Agent': 'magicAzureTTS'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', VOICES[VOICES['default']]) # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = text
        body = ElementTree.tostring(xml_body)
        constructed_url += '?language=en-US'
        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        err_msg = response.status_code
        audio = response.content
        if response.status_code == 200:
            return (err_msg, audio)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")
            return (err_msg, None)

    def get_voices_list(self):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

if __name__ == "__main__":
    app = AzureTTS(api_key='f1f1d4329cc340169cc6074062c18675')
    (err, audio) = app.say(text="Hello, Azure")
    print(audio)
    # Get a list of voices https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices
    #app.get_voices_list()
