from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

import youtube_dl


class YoutubedlSkill(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.playing = False

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        pass

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
