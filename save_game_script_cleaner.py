#!/usr/bin/env python
"""
TTS Save Game Script Cleaner!

This clears the obnoxious "tcejbo gninwapS" pseudo-virus infecting TTS objects.

PLEASE FOLLOW THE INSTRUCTIONS, AND ONLY ASK FOR HELP IF YOU ACTUALLY TRIED.
IT IS NOT AS HARD AS YOU THINK. SERIOUSLY STOP PROCRASTINATING AND JUST DO IT.

How to use:
1. Have Python installed: https://www.python.org/downloads/
2. Have this script somewhere on your computer. Double-click it to run. You
   should see a window with text in it, it should work for a while, then tell
   you to press enter to exit.
    2a. If the window doesn't show up or shows up for just a split second, you
        have some sort of permissions problem specific to your computer, and
        you might need to google for how to run a python script from the
        internet.
3a. If you run the script on its own, it will attempt to guess your TTS data
    folder and clean everything in it. If it does not find the correct
    directory, you can put the preferred path into TTS_DIR_OVERRIDE.
3b. Alternatively, run this on a particular file or directory. If you're on
    Windows, after installing Python you can drag your Saves and/or Workshop
    folder onto this script and it'll run and clean them, or run
    `python path/to/script.py path/to/Saves` on the command line.

FAQ:

Q: What is the "tcejbo gninwapS" pseudo-virus?
A: It is a TTS lua script that copies itself to every object it can find,
including dice, hands, cards, tables, all sorts of things. It attempts to
contact a website, presumably to download malicious code to execute, but that
website is down right now. If it were to be up again, there could be some
serious security concerns. However, even without those security concerns, the
script itself can sometimes introduce lag/stuttering in games, especially over
time and/or when spawning lots of objects such as the piles of dice in wargames.
Note that if someone brings in a single model with the virus into a multiplayer
game, every other object will become infected. So, everyone in your play group
should get checked.

Q: How can I check for the virus in a game, especially when other people might
join and spawn an infected object?
A: You can spawn the detector created by Ziggy Stardust in the workshop mod
"Malicious Script Check" -- this checks periodically for the virus and may
alert you if an infection occurs. Some tables already have this integrated.
https://steamcommunity.com/sharedfiles/filedetails/?id=3062067951

Q: How often should I run this python script?
A: For maximum paranoia, you can run this every time you start TTS once TTS has
finished updating workshop mods, just in case one of the mods you were already
subscribed to has updated and contains the virus. But that is probably more
paranoid than most people need so just running it once might be ok. If you did
find the virus in a workshop mod though, please leave a comment, as the mod
author probably does not know.

Q: How does this compare to CleanerBlock?
A: This is more thorough than CleanerBlock, as that can't look inside bags or
attached things. For example, if a dude is attached to a base, and both were
infected, the CleanerBlock might clean the base, but the infection on the dude
might remain dormant until he is detached in the future. Also it can clean out
all your files at once: saved games, the local copy of workshop mods, and saved
objects.

Q: Does this also clean out saved objects?
A: Yes. If you run this on your Saves folder (which it will by default), it
will clean your saved objects, yes. The saved objects are also json files in a
subdirectory there, in a similar format to saved games and workshop mods, so
this python script works just as well on them.

Q: How can I tell which files are infected?
A: If you open an infected save file (ends in .json) in a text editor such as
Notepad, you can search (ctrl-F usually) for "glitch" or "WebRequest" or
"tcejbo gninwapS and see the condensed confusing blob of Lua code attached to
all sorts of objects.

Q: Will this mess up existing good Lua scripts?
A: Your objects' good Lua scripts will be preserved. An older version of this
python script did delete good Lua scripts if they were infected by the
malicious Lua script, as it was written in haste to solve the urgent problem.
The current version of this python script does not. So after running this,
Lua scripts should continue to work as expected and you won't need to e.g.
re-yellowscribe armies for 40k.

Q: I have attempted to follow the instructions and still have problems. Where
can I get help?
A: Ask in the suspicious-or-malicious-mods-and-scripts channel on the TTS
Warhammer 40k discord:
https://discord.com/channels/282027517773217793/1123842606883946588
"""
import json
import multiprocessing
import os
import pathlib
import re
import sys
import time
from time import gmtime, strftime


# If your Tabletop Simulator data directory is in some alternative location,
# paste it in the quotes below.
TTS_DIR_OVERRIDE = r""


def tts_default_locations():
    """Attempt to guess the Tabletop Simulator data directory."""
    if sys.platform == "linux" or sys.platform == "linux2":
        return [
            os.path.join(
                str(pathlib.Path.home()),
                ".local",
                "share",
                "Tabletop Simulator",
            )
        ]
    elif sys.platform == "darwin":  # mac osx
        return [
            os.path.join(
                str(pathlib.Path.home()), "Library", "Tabletop Simulator"
            )
        ]
    elif sys.platform == "win32":
        return [
            os.path.join(
                os.environ["USERPROFILE"],
                "Documents",
                "My Games",
                "Tabletop Simulator",
            ),
            os.path.join(
                os.environ["USERPROFILE"],
                "OneDrive",
                "Documents",
                "My Games",
                "Tabletop Simulator",
            ),
        ]
    else:
        return [
            f"couldn't match platform {sys.platform}, so don't know save game location"
        ]


evil_url_re = re.compile(r"obje\.glitch\.me")


def cleanse_script(script):
    """cleanse_script takes a string and returns a cleansed version."""
    # the infection uses a bunch of spaces between good code and its code.
    l = script.split(" " * 150)
    # exclude any parts that match the evil regexp, rejoin legit stuff,
    # clear outer whitespace.
    return (" " * 150).join([s for s in l if not evil_url_re.search(s)]).strip()


def cleanse_obj(obj):
    if isinstance(obj, dict):
        for k, v in dict(obj.items()).items():
            if k == "LuaScript" and evil_url_re.search(v):
                cleansed_script = cleanse_script(v)
                if cleansed_script:
                    obj["LuaScript"] = cleansed_script
                else:
                    del obj["LuaScript"]
            else:
                cleanse_obj(v)
    elif isinstance(obj, list):
        for item in obj:
            cleanse_obj(item)


def retriably_rename(old_path, new_path):
    """Retriably move something from path to path.

    This exists just as a possible workaround for an issue on my
    remote drive.
    """
    for ix in range(5):
        try:
            os.rename(old_path, new_path)
            return
        except PermissionError:
            time.sleep(2.0)
    # last ditch attempt
    os.rename(old_path, new_path)


def read_file(filename):
    infile = open(filename, mode="r", encoding="utf-8")
    intext = infile.read()
    infile.close()
    return intext


def file_contains_virus(filename):
    return bool(
        filename.endswith(".json") and evil_url_re.search(read_file(filename))
    )


def cleanse_file(filename):
    if not file_contains_virus(filename):
        return
    intext = read_file(filename)
    print("Found problem in", filename)
    now = strftime("%Y-%m-%dT%H-%M-%SZ", gmtime())
    backup_filename = f"{filename}-{now}.backup"
    print("Moving to backup location", backup_filename)
    retriably_rename(filename, backup_filename)
    obj = json.loads(intext)
    cleanse_obj(obj)
    tmp_filename = f"{filename}.tmp"
    outfile = open(tmp_filename, mode="w")
    json.dump(obj, outfile, indent=2)
    outfile.close()
    retriably_rename(tmp_filename, filename)
    print("Cleansed", filename)


def cleanse_dir(dirname, pool=None):
    async_results = []
    count = 0
    seen_paths = []
    infected_paths = []
    for root, dirs, files in os.walk(dirname):
        for filename in files:
            if filename.endswith(".json"):
                full_path = os.path.join(root, filename)
                seen_paths.append(full_path)
    print(f"Found {len(seen_paths)} json files to examine.")
    if pool:
        for ix, b in enumerate(pool.map(file_contains_virus, seen_paths)):
            if b:
                infected_paths.append(seen_paths[ix])
    else:
        for path in seen_paths:
            if file_contains_virus(path):
                infected_paths.append(path)

    print(
        f"Examined {len(seen_paths)} json files, and found the pseudo-virus in {len(infected_paths)} of them."
    )
    for path in infected_paths:
        cleanse_file(path)


def cleanse_thing(path, pool=None):
    if os.path.isfile(path):
        cleanse_file(path)
    elif os.path.isdir(path):
        cleanse_dir(path, pool=pool)
    else:
        print("File or directory not found; skipping.")


if __name__ == "__main__":
    things = list(sys.argv[1:])
    if not things:
        if TTS_DIR_OVERRIDE:
            things = [TTS_DIR_OVERRIDE]
            print(
                f"No arguments given, so looking at TTS data dir {TTS_DIR_OVERRIDE}\nYou can change this by editing the script's value in TTS_DIR_OVERRIDE"
            )
        else:
            things = tts_default_locations()
            print(
                f"No arguments given, so guessing at TTS default data dir(s).\nYou can change this by editing the script's value in TTS_DIR_OVERRIDE"
            )
    with multiprocessing.Pool() as pool:
        for item in things:
            print(strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()), "Examining", item)
            cleanse_thing(item, pool=pool)
    print(
        strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()), "Done. Press enter to exit."
    )
    input()
