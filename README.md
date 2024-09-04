# TTS Save Game Script Cleaner!

This clears the obnoxious "tcejbo gninwapS" pseudo-virus infecting Tabletop
Simulator objects.

PLEASE FOLLOW THE INSTRUCTIONS, AND ONLY ASK FOR HELP IF YOU ACTUALLY TRIED.
IT IS NOT AS HARD AS YOU THINK. SERIOUSLY STOP PROCRASTINATING AND JUST DO IT.

How to use:
1. Have Python installed: https://www.python.org/downloads/
2. Download [`save_game_script_cleaner.py`](https://raw.githubusercontent.com/khaaarl/tts-save-game-script-cleaner/main/save_game_script_cleaner.py?raw=true) to somewhere on your computer, and double-click it to run. You should see a window with text in it, it should work for a while, then tell you to press enter to exit.

Troubleshooting:
1. If the window doesn't show up or shows up for just a split second, you have some sort of permissions problem specific to your computer, and you might need to google for how to run a python script from the internet.
2. If you run the script on its own, it will attempt to guess your TTS data folder and clean everything in it. If it does not find the correct directory, you can put the preferred path into TTS_DIR_OVERRIDE inside the python script.
3. Alternatively, run this on a particular file or directory. If you're on Windows, after installing Python you can drag your Saves and/or Workshop folder onto this script and it'll run and clean them, or run `python path/to/script.py path/to/Saves` on the command line.

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

A: You can spawn [the detector created by Ziggy Stardust in the workshop mod "Malicious Script Check"](https://steamcommunity.com/sharedfiles/filedetails/?id=3062067951) -- this checks periodically for the virus and may alert you if an infection occurs. Some tables already have this integrated.

Q: How often should I run this python script?

A: For maximum paranoia, you can run this every time you start TTS once TTS has
finished updating workshop mods, just in case one of the mods you were already
subscribed to has updated and contains the virus. But that is probably more
paranoid than most people need so just running it once might be ok. If you did
find the virus in a workshop mod though, please leave a comment, as the mod
author probably does not know.

Q: How does this compare to [CleanerBlock](https://steamcommunity.com/sharedfiles/filedetails/?id=2967684892)?

A: This is more thorough than [CleanerBlock](https://steamcommunity.com/sharedfiles/filedetails/?id=2967684892), as that can't look inside 
attached objects and maybe some other things. For example, if a dude is attached to a base, and both were
infected, the CleanerBlock might clean the base, but the infection on the dude
might remain dormant until he is detached in the future. Also my script can clean out
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

A: Ask in the suspicious-or-malicious-mods-and-scripts channel on the TTS Warhammer 40k discord, or message khaaarl on discord with sufficient info that I can help.
