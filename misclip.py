#!/usr/bin/env python

from xml.etree import ElementTree as ET
import sys
import os
import shutil

def find_matching_format(syncclip):
    return None

def describe_framerate(fd):
    if "/" in fd:
        den, nom = fd.split("/")
        nom = nom.strip("s")
        return float(int(1.0 / (float(den) / float(nom)) * 1000.0)) / 1000.0
    return 1.0

def format_extents(fmt):
    w = int(fmt.attrib.get("width", "0"))
    h = int(fmt.attrib.get("height", "0"))
    return w, h

def format_surface_area(fmt):
    w, h = format_extents(fmt)
    return w * h

def describe_format(fmt):
    w, h = format_extents(fmt)
    fps = describe_framerate(fmt.attrib.get("frameDuration", "1/1s"))
    return "{}: {}x{} @{}fps".format(fmt.attrib.get("id", "???"), w, h, fps)

def fix_file(fname):
    outfile = os.path.splitext(fname)[0] + "_resized.fcpxml"
    tree = ET.parse(fname)
    root = tree.getroot()
    resources = root.findall("resources")
    all_formats = {}
    for resource in resources:
        formats = resource.findall("format")
        for fmt in formats:
            all_formats[fmt.attrib["id"]] = fmt



    syncclips = root.findall(".//sync-clip")
    print("{} sync clips found.".format(len(syncclips)))
    for sclip in syncclips:
        if "name" not in sclip.attrib:
            continue
        name = sclip.attrib.get("name", "???")
        if "format" not in sclip.attrib:
            print("Sync clip {} doesn't have format!".format(name))
            continue
        fmt = all_formats.get(sclip.attrib["format"], None)
        if fmt is None:
            print("Sync clip {} points to a non-existent format!".format(name))
            continue
        a_fmts = []
        for aclip in sclip.findall(".//asset-clip"):
            if "format" in aclip.attrib:
                possible_format = all_formats.get(aclip.attrib["format"], None)
                if possible_format is not None:
                    if possible_format not in a_fmts:
                        if possible_format.attrib.get("width", "unknown") != "unknown":
                            a_fmts.append(possible_format)
        sel_fmt = None
        if len(a_fmts) == 1:
            sel_fmt = a_fmts[0]
        elif len(a_fmts) > 1:
            sel_fmt = sorted(a_fmts, key=lambda x: format_surface_area(x))[-1]
        if sel_fmt is None:
            print("Couldn't find format replacement basis for sync clip {}.".format(name))
            continue
        if sel_fmt.attrib.get("id", "???") == fmt.attrib.get("id", "???"):
            continue
        print("Sync clip {} is currently set to {}".format(name, describe_format(fmt)))
        print("    Changing to: {}".format(describe_format(sel_fmt)))
        sclip.attrib["format"] = sel_fmt.attrib["id"]

    for event in root.findall(".//event"):
        # rename events
        name = event.attrib.get("name", None)
        if name is None:
            continue

        event.attrib["name"] = "{} resized".format(name)

    print("Writing to {}...".format(outfile))
    outdata = ET.tostring(root)
    open(outfile, "w").write(outdata)

    print("Done.")

if len(sys.argv) < 2:
    print("USAGE: misclip.py <fcpxml files>")
    sys.exit(1)

for fname in sys.argv[1:]:
    if fname.split(".")[-1].lower() != "fcpxml":
        print("Sorry, this tool only works with .fcpxml files ({}).".format(fname))
        continue

    if not os.path.exists(fname):
        print("File not found: {}.".format(fname))
        continue

    fix_file(fname)

