# Youtube_dl skill for mycroft

Searches from and downloads a youtube video and plays it.

## About

This skill will download the first match of the inputed song/video name (excluding
playlists) and play its audio.

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
playing, the playback will stop and the new video will be downloaded/played.

## Stop playing

```txt
youtube stop
```

Stops playing the currently playing video (if any).

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
