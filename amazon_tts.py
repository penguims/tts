class AmazonTTS:
    def __init__(self, app_id="", api_key="", secret_key=""):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key

    def say(self, text):
        audio = None
        err = True
        return (err, audio)
