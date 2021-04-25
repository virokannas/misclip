# What

This tool will help batch fix synchronized clips in Final Cut Pro X events to have the proper format.

**Use at your own risk. Always make backups before trying tools you find on the Internets.**

# Why

As annoying as it is, if the video clip used in a synchronize clip doesn't have a format that happens to fall into the existing presets, the sync clip ends up having a resolution of 1280x720. This is never a correct assumption but will in many cases appear as if everything is ok (until you bring that clip onto a timeline).

# How

To use the script, simply run:

```
misclip.py <path to fcpxml file>
```

Tthe output file(s) will be suffixed with ```_resized``` so that your original file stays safe.

Or, you can install the "Run misclip" workflow under your ~/Library/Services and use it as a quick action in Finder. Just select all your fcpxml files, right-click and choose "Run misclip" from Quick Actions.

# I have so many questions

Slow down. Here's a simple workflow that might provide the easiest round-trip. Since events can't really be overwritten when doing a roundtrip like this (the change in format marks each clip as as completely new), here's what you can do to ensure the integrity of your project and run the fix for a single event, not the whole project:

1. Choose what you want to be fixed and combine them into neatly packed events. These events should contain all the sync clips as well as the timeline that uses the clips.
2. Export that event as .fcpxml
3. Run that .fcpxml through the tool
4. Import the generated .fcpxml
5. Make sure that all the clips are absolutely correct so that you don't lose any of your precious syncs
6. Rename (or delete) the old event so that you don't ever have to see it again

Or, if you have a workflow with sync clips in one event, the timelines in other, and you just want a quick fix for everything:
1. Make a backup of your library. Seriously.
2. Export the whole library
3. Run the .fcpxml through misclip
4. Import the generated .fcpxml
5. Blow away the old events
