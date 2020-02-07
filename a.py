from __future__ import unicode_literals
import youtube_dl
from subprocess import Popen, DEVNULL, STDOUT, CalledProcessError
from os import remove


def play_vid(vid):
    return Popen(
        ["mpv", "--vid=no", "--keep-open=no", vid],
        stdin=DEVNULL,
        stdout=DEVNULL,
        stderr=STDOUT,
    )


def youtubedl_hook(msg):
    if msg["status"] == "downloading":
        pass
        #  print("Downloading " + msg["filename"])
    elif msg["status"] == "finished":
        print("Finished downloading " + msg["filename"])
        p = play_vid(msg["filename"])
        p.wait()
    elif msg["status"] == "error":
        print("Error downloading " + msg["filename"])


ydl_opts = {
    "default_search": "auto",
    "quiet": True,
    "format": "bestaudio/best",
    "progress_hooks": [youtubedl_hook],
}


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(
        [
            "https://www.youtube.com/watch?v=xwJ8hsLTsbA&list=PLTad7jqoGMBrWLONVjMDYjoQQppi0MUon"
        ]
    )
