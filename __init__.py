#!/usr/bin/python3
from __future__ import unicode_literals
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import youtube_dl
from subprocess import Popen, DEVNULL, STDOUT, CalledProcessError
from os import remove


class YoutubedlSkill(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.proc = None
        self.vid = None
        self.queue = []

    def initialize(self):
        my_setting = self.settings.get("my_setting")

    def play_vid(self):
        if self.proc is not None:
            self.stop()
        try:
            self.proc = Popen(
                ["mpv", "--vid=no", "--keep-open=no", self.vid],
                stdin=DEVNULL,
                stdout=DEVNULL,
                stderr=STDOUT,
            )
        except OSError:
            self.log.error("Error playing video youtubedl: non-existent file.")
        except CalledProcessError:
            self.log.error("Error playing video youtubedl: non-existent file.")
        #  self.log.info("Finished playing video youtubedl.")
        #  self.stop()

    def download_vid(self, vid_name):
        # hook to check and handle failures
        def youtubedl_hook(msg):
            if msg["status"] == "finished":
                self.vid = msg["filename"]
                self.log.info("Finished downloading " + vid_name + ".")
                # play the stuff
                self.log.info("Start playing video youtubedl.")
                self.play_vid()
                self.proc.wait()  # wait for end
                self.skip()
            elif msg["status"] == "error":
                self.log.error("Error playing " + vid_name + ".")
                self.speak_dialog("Error playing " + vid_name + ".")
                self.skip()

        # queue songs
        self.queue.append(vid_name)
        if len(self.queue) > 1:
            self.log.info("Queued " + vid_name + ".")
            self.speak_dialog("Queued " + vid_name + ".")
            return
        else:
            self.log.info("Playing " + vid_name + ".")
            self.speak_dialog("Playing " + vid_name + ".")

        # youtube_dl options
        self.ydl_opts = {
            "default_search": "auto",
            "format": "bestaudio/best",
            "logtostderr": True,
            "progress_hooks": [youtubedl_hook]
            #  "quiet": True,
        }

        while len(self.queue):
            # set video name
            vid_name = self.queue[0]
            # download and convert video
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([vid_name])

    @intent_handler("Youtubedl.intent")
    def handle_youtubedl_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        vid_name = message.data.get("vid")
        if vid_name is not None:
            if vid_name == "stop":  # clear queue
                self.stop()
                self.speak_dialog("youtubedl_stop")
            elif vid_name == "skip":  # skip currently playing
                self.skip()
                #  self.speak_dialog("youtubedl_stop")
            elif vid_name == "queue":  # check queue
                if len(self.queue):
                    self.log.info("Next in queue is " + self.queue[0])
                    self.speak_dialog("Next in queue is " + self.queue[0])
                else:
                    self.log.info("The play queue is empty.")
                    self.speak_dialog("The play queue is empty.")
            else:
                self.download_vid(vid_name)
                self.log.info("Done downloading video youtubedl.")
        else:
            self.speak_dialog("youtubedl")
        self.log.debug("Done youtubedl.")

    #  @intent_handler(IntentBuilder("YoutubedlStop").require("YoutubedlStopKeyword"))
    #  def handle_youtubedl_stop_intent(self, message):
    #  """ This is an Adapt intent handler, it is triggered by a keyword."""
    #  self.stop()
    #  self.speak_dialog("youtubedl_stop")

    def skip(self):
        self.log.info("Skip playing video youtubedl.")
        # remove current playing
        if self.queue[0]:
            del self.queue[0]
        if self.proc:
            self.proc.terminate()
        if self.vid:
            remove(self.vid)
        # reset vars
        self.vid = None
        self.proc = None

    def stop(self):
        self.log.info("Stop playing video youtubedl.")
        # clear queue
        self.queue = []
        if self.proc:
            self.proc.terminate()
        if self.vid:
            remove(self.vid)
        # reset vars
        self.vid = None
        self.proc = None


def create_skill():
    return YoutubedlSkill()
