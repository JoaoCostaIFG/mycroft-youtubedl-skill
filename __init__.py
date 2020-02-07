#!/usr/bin/python3

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

from __future__ import unicode_literals
import youtube_dl


class YoutubedlSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.playing = False
        self.downloading = False

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get("my_setting")

    #  def youtubedl_hook(msg):
    #  if msg["status"] == "downloading":
    #  pass
    #  #  print("Downloading " + msg["filename"])
    #  elif msg["status"] == "finished":
    #  self.log.info("Finished downloading " + msg["filename"])
    #  elif msg["status"] == "error":
    #  self.log.error("Error downloading " + msg["filename"])

    def download_vid(self, vid_name):
        if self.downloading:
            self.log.warning("Already downloading a video, wait.")
            self.speak_dialog("Already downloading a video, wait.")
            return

        self.downloading = True
        # youtube_dl options
        ydl_opts = {
            "default_search": "auto",
            "quiet": True,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "128",
                }
            ],
        }

        # download and convert video
        failed = 0
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            failed = ydl.download([vid_name])

        # check and handle failures
        if failed:
            self.log.error("Error downloading " + vid_name)
            self.speak_dialog("Error downloading " + vid_name)
        else:
            self.log.info("Finished downloading " + vid_name)
            self.speak_dialog("Finished downloading " + vid_name)
        self.downloading = False

    @intent_handler("Youtubedl.intent")
    def handle_youtubedl_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        vid_name = message.data.get("vid")
        if vid_name is not None:
            self.speak_dialog("Looking for " + vid_name)
            self.download_vid(self, vid_name)
        else:
            self.speak_dialog("youtubedl")

    def stop(self):
        pass


def create_skill():
    return YoutubedlSkill()
