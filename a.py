from __future__ import unicode_literals
import youtube_dl


def youtubedl_hook(msg):
    if msg["status"] == "downloading":
        pass
        print("Downloading " + msg["filename"])
    elif msg["status"] == "finished":
        print("Finished downloading " + msg["filename"])
    elif msg["status"] == "error":
        print("Error downloading " + msg["filename"])


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
    "progress_hooks": [youtubedl_hook],
}


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["shine on  your crazy diamond"])
