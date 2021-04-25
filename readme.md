# What

This tool will help batch fix synchronized clips in Final Cut Pro X events to have the proper format.

# Why

As annoying as it is, if the video clip used in a synchronize clip doesn't have a format that happens to fall into the existing presets, the sync clip ends up having a resolution of 1280x720. This is never a correct assumption but will in many cases appear as if everything is ok (until you bring that clip onto a timeline).

# How

To use the script, simply run:

```
misclip.py <path to fcpxml file>
```

Tthe output file(s) will be suffixed with ```_resized``` so that your original file stays safe.

Or, you can install the "Run misclip" workflow under your ~/Library/Services and use it as a quick action in Finder. Just select all your fcpxml files, right-click and choose "Run misclip" from Quick Actions.
