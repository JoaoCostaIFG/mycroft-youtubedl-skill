#!/usr/bin/python3
from __future__ import unicode_literals
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import youtube_dl
from subprocess import check_call, DEVNULL, STDOUT
from os import remove


class YoutubedlSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.is_downloading = False
        self.proc = None
        self.vid = None
        self.cnt = 0

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get("my_setting")

    def play_vid(self):
        if self.proc is not None:
            self.stop()
        self.proc = check_call(
            ["mpv", "--vid=no", self.vid], stdout=DEVNULL, stderr=STDOUT
        )
        self.log.info("Finished playing video youtubedl.")
        self.stop()

    def download_vid(self, vid_name):
        # hook to check and handle failures
        def youtubedl_hook(msg):
            if msg["status"] == "finished":
                self.vid = msg["filename"]
                self.is_downloading = False
                self.log.info("Finished downloading " + vid_name)
            elif msg["status"] == "error":
                self.vid = None
                self.is_downloading = False
                self.log.error("Error downloading " + vid_name + ".")
                self.speak_dialog("Error downloading " + vid_name + ".")

        # check if a download is currently in progress
        if self.is_downloading:
            self.log.warning("Already downloading a video, wait.")
            self.speak_dialog("Already downloading a video, wait.")
            return

        self.log.info("Downloading " + vid_name + ".")
        self.speak_dialog("Downloading " + vid_name + ".")
        self.is_downloading = True
        # youtube_dl options
        ydl_opts = {
            "default_search": "auto",
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "progress_hooks": [youtubedl_hook],
        }

        # download and convert video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([vid_name])

    @intent_handler("Youtubedl.intent")
    def handle_youtubedl_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        vid_name = message.data.get("vid")
        if vid_name is not None:
            self.download_vid(vid_name)
            self.log.info("Done downloading video youtubedl.")
            if self.vid is not None:
                self.log.info("Start playing video youtubedl.")
                self.play_vid()
        else:
            self.speak_dialog("youtubedl")
        self.log.debug("Done youtubedl.")

    @intent_handler(IntentBuilder("YoutubedlStop").require("YoutubedlStopKeyword"))
    def handle_youtubedl_stop_intent(self, message):
        """ This is an Adapt intent handler, it is triggered by a keyword."""
        self.cnt += 1
        self.log.error("it is: " + str(self.cnt))
        self.stop()
        self.speak_dialog("youtubedl_stop")

    def stop(self):
        self.log.info("Stop playing video youtubedl.")
        if self.proc:
            self.proc.terminate()
        if self.vid:
            remove(self.vid)


def create_skill():
    return YoutubedlSkill()
