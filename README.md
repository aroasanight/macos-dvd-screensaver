# dvd-screensaver-generator
 
A script to generate a DVD screensaver for macOS 14 and above.

# Instructions for use

1. Download this repository as a .zip then extract into an empty folder.
2. Open terminal, and cd to the directory containing main.py
3. Run `python3 main.py [arguments]` with the arguments explained in the Arguments section.
4. Respond to the replacement prompt with Y or N. If you select NO, scroll to the "Manually installing" section of this readme.
5. Presuming you selected yes, type the number of your least favourite screensaver from the list. Reference `System Settings > Screen Saver` if you're not sure, or just pick one if you never use the Aerial screensavers.
6. Drag the highlighted .mov file to the other finder window that was opened.
7. Head to `System Settings > Screen Saver` and select the screensaver you chose to replace. Make sure your screensaver starts before your screen turns off in `System Settings > Lock Screen`, and I suggest disabling `Show as wallpaper` in `System Settings > Screen Saver` and selecting a different wallpaper in `System Settings > Wallpaper`.
8. Test your screensaver by clicking on the preview at the top of `System Settings > Screen Saver`. If it doesn't work, try a restart, or if it starts downloading the screensaver, run the script again once it's done.

# Arguments

### Syntax

`python3 main.py -v -w=1920 -h=1080 -f=60 -d=60`

### Flags

- -w: width (in pixels)
- -h: height (in pixels)
- -f: fps
- -d: duration (in seconds)

# Manually Installing

- Head to `System Settings > Screen Saver`, and download an Aerial screensaver that you don't like (any of the video ones under the Landscape, Cityscape, Underwater, or Earth categories).
- Open Finder, press cmd+shift+G, and paste in the following file path: `/Library/Application Support/com.apple.idleassetsd/Customer/4KSDR240FPS/`
- Find the video for the screensaver you just downloaded, and copy its file name
- In the directory you ran the script in, you will find a file named `output_video.mov`. Rename it to the file name you just copied.
- Move this new file into `/Library/Application Support/com.apple.idleassetsd/Customer/4KSDR240FPS/`, replacing the old screensaver.
- Restart your Mac if necessary.