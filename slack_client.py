import os
from slack import WebClient
from slack.errors import SlackApiError
from nllb_model import Translator
import requests

flags_map = {
  "flag-us": { "translateTo": "eng_Latn", "languageIcon": ":us:" },
  "flag-vn": { "translateTo": "vie_Latn", "languageIcon": ":vn:" },
  "flag-jp": { "translateTo": "jpn_Jpan", "languageIcon": ":jp:" }
}

class SlackClient:
    def __init__(self, logger):
        slack_token = os.environ["SLACK_API_TOKEN"]
        self.client = WebClient(token=slack_token)
        self.looger = logger
        MODEL_ID = "facebook/nllb-200-distilled-600M"
        self.translator = Translator(model_id=MODEL_ID, logger=logger)

    def postThreadMessage(self, channel, ts, text):
        try:
            response = client.chat_postMessage(
                channel=channel,
                text=text
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

    def onReactionAdded(self, json):

        event_type = json['event']['type']
        self.logger.info("Start!!" + event_type)
        if (event_type != "reaction_added"):
            self.logger.info("Event type is not reaction_added. Ignored.")
            return False

        ts = json['event']['item']['ts']
        if (len(ts)==0) :
            self.logger.info("thread not found!")
            return False

        reaction = json['event']['reaction']
        if (len(reaction)==0):
            self.logger.info("reaction not found!")
            return False

        target_lang = flags_map[reaction]
        if (target_lang is None or len(target_lang)==0):
            self.logger.info("target_lang not found! Skip translate")
            return False

        channel = json['event']['item']['channel']
        message = self.getMessages(channel, ts, logger)

        #translatedMessage = flag_map[reaction]['languageIcon'] + " "
            #+ LanguageApp.translate(message, "", flag_map[reaction].translateTo);
        #translated_message = self.translator.translate(message, 'jpn_Jpan', target_lang)
        translated_message = self.call_translation_api()
        self.logger.info("translated Message:" + translated_message)
        #    postThreadMessage(channel, ts, translatedMessage);
        return True

    def getMessages(self, channel, ts):
        message_history = self.client.api_call(api_method='conversations.replies', data={'channel':channel, 'ts': ts})
        self.logger.info(message_history['messages'][0]['text'])
        return message_history['messages'][0]['text']

    def call_translation_api(self):
        r = requests.post('localhost:5000/translate', json={"source": ["Comment allez-vous?"], "src_lang": "fra_Latn", "tgt_lang": "vie_Latn"})
        return r.json
