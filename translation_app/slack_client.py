import os
import requests
from slack import WebClient
from slack.errors import SlackApiError

flags_map = {
  "flag-vn": { "translateTo": "vie_Latn", "languageIcon": ":flag-vn:" },
  "flag-jp": { "translateTo": "jpn_Jpan", "languageIcon": ":jp:" },
  "jp": { "translateTo": "jpn_Jpan", "languageIcon": ":jp:" }
}

DEF_SRC_LNG = 'jpn_Jpan'
DEF_TGT_LNG = 'vie_Latn'

class SlackClient:

    def __init__(self, logger):
        slack_token = os.environ["SLACK_API_TOKEN"]
        self.client = WebClient(token=slack_token)
        self.logger = logger

    def postThreadMessage(self, channel, ts, text):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                thread_ts=ts,
                text=text
            )
        except SlackApiError as e:
            assert e.response["error"]

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

        if (reaction not in flags_map):
            self.logger.info("Not supported language!")
            return False

        target_lang = flags_map[reaction]['translateTo']
        if (target_lang is None or len(target_lang)==0):
            self.logger.info("target_lang not found! Skip translate")
            return False

        channel = json['event']['item']['channel']
        self.logger.info("channel:" + channel + ", ts:" + ts + ", reaction:" + reaction)
        message = self.getMessages(channel, ts)
        src_lang = DEF_SRC_LNG
        if (src_lang == target_lang):
            src_lang = DEF_TGT_LNG
        translated_message = self.call_translation_api(source_msg=message, src_lang=src_lang, tgt_lang=target_lang)
        self.logger.info("translated Message:")
        self.logger.info(translated_message)
        if (len(translated_message) > 0):
            self.postThreadMessage(channel, ts, flags_map[reaction]['languageIcon'] + " " + translated_message[0]);
        return True

    def getMessages(self, channel, ts):
        message_history = self.client.api_call(api_method='conversations.replies', data={'channel':channel, 'ts': ts})
        self.logger.info(message_history['messages'][0]['text'])
        return message_history['messages'][0]['text']

    def call_translation_api(self, source_msg, src_lang, tgt_lang):
        if isinstance(source_msg, str):
            source_msg = [source_msg]
        r = requests.post('http://nllb200-api:6060/translate', json={"source": source_msg, "src_lang": src_lang, "tgt_lang": tgt_lang})
        return r.json()['translation']
