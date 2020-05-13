import sys, os

class LocalTTS:
    def __init__(self, app_id="", api_key="", secret_key=""):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key

    def say(self, text):
        audio = None
        err = True
        pin, pout = os.pipe()
        pid = os.fork()
        if pid:
            os.close(pout)
            pin = os.fdopen(pin)
            audio = fin.read()
        pin.close()
        else:
            os.close(pin)
            pout = os.fdopen(pout, "w")
            os.system('espeak --stdout "{}"'.format(text))
            pout.close()
            system.exit(0)
        return (err, audio)
