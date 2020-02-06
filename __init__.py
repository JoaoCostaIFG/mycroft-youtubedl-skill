from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

import youtube_dl


class YoutubedlSkill(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.playing = False

    @intent_handler(IntentBuilder("youtubedl.intent").require("YoutubedlKeyword.voc"))
    def handle_playintent(self, message):
        vid_name = message.data.get("vid")
        if vid_name is not None:
            self.speak_dialog(vid_name)
        else:
            self.speak_dialog("dunno vid name")

    def stop(self):
        # what to do if told to stop
        pass

    def shutdown(self):
        self.stop(self)
        pass


def create_skill():
    return YoutubedlSkill()
