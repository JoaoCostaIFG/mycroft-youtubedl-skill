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
    "format": "bestaudio/best",
    "noplaylist": False,
    "playlist_items": "1, 5",
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # get info
    a = ydl.extract_info(
        "https://www.youtube.com/watch?v=q7DfQMPmJRI&list=PL3htOwmtQv_yHPXNRHNJ-naKnAsvOuclt",
        #  "ytsearch1:tool fear inoculum full album playlist",
        download=False,
        process=True,
        force_generic_extractor=ydl.params.get("force_generic_extractor", False),
    )
    #  print(a)
    # process the search url
    b = ydl.process_ie_result(a, download=False)
    print(b["entries"][0]["n_entries"])

    vid = None
    if "entries" in b:
        print("playlist or list")
        for i in b["entries"]:
            print(i["title"])
        vid = b["entries"][0]["url"]
    else:
        print("single video")
        vid = b["url"]
    print(vid)

    #  print(len(list(a["entries"])))

    #  ydl_opts = {
    #  "default_search": "auto",
    #  "format": "bestaudio/best",
    #  "skip_download": True,
    #  }

    #  # download and convert video
    #  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #  ydl.download(["tool fear inoculum full album playlist"])
