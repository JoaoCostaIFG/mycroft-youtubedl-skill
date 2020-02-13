# Youtube_dl skill for mycroft

Searches for and downloads a youtube video, and queues it for playing.

## About

This skill will download the first match of the inputed song/video name (excluding
playlists) and play its audio.

## Note

Doesn't handle playlists (for now).
This is a quick hack using [youtube-dl](https://github.com/ytdl-org/youtube-dl/)
and [mpv](https://github.com/mpv-player/mpv). If anything breaks/stops working,
try updating **youtube-dl**. The **youtube-dl** Debian package isn't working
for me (don't know why) but the **pip3** one is, so take that into consideration
if this doesn't work.

## Install

If you have msm:

`mycroft-msm install https://github.com/JoaoCostaIFG/mycroft-youtubedl-skill.git`

or

`msm install https://github.com/JoaoCostaIFG/mycroft-youtubedl-skill.git`

You can also install it manually by:

```sh
sudo apt-get install mpv
sudo pip3 install youtube_dl
cd /opt/mycroft/skills
git clone https://github.com/JoaoCostaIFG/mycroft-youtubedl-skill.git
```

## Play video

```txt
youtube "video"
youtube play "video"
youtube start "video"
youtube download "video"
```

Where "video" is the string to search for on Youtube. If a video is currently
playing, the video will be queued.

## Stop playing (clear play queue)

```txt
youtube stop
```

## Skip playing (play next song)

```txt
youtube skip
```

## Check next in queue

```txt
youtube queue
```

## Check currently playing video

```txt
youtube current
```

## Examples

- "Youtube tool lateralus"
- "Youtube play placebo bitter end"
- "Youtube stop"

## Credits

JoaoCostaIFG

## Category

**Music & Audio**
Media
Entertainment

## Tags

#Youtube
#Music

## Thanks

Thank you to my friend [anaines14](https://github.com/anaines14) for the idea,
inspiration and motivation to finish this small skill.
