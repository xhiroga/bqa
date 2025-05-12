# Contributing

## How to Create a GIF File

### macOS

1. Set Preference > Interface > Language to English.
2. Launch Command + Shift + 5 or QuickTime Player > New Screen Recording.
3. Record your video.
4. Convert the video to GIF: `ffmpeg -i '~/screencapture/Your latest.mov' -r 15 as/s/what-you-did.gif`
5. Add the information to `as/metadata.jsonl`.
6. `python3 scripts/build.py`
