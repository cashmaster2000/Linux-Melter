Kill Stick

Two files. One purpose. Maximum damage.

What is it?

A minimalist, high-impact USB drive containing exactly two Python scripts. No bloat. No dependencies you can’t install in seconds. Just Run.py and attack.py. That’s it. That’s the whole stick.

It’s designed for speed, silence, and finality. Plug it in. Run the command. The target is gone before they finish blinking.

The Files
Run.py

The trigger. The initiator. The "I’m about to do something stupid" button.

Purpose: Initializes the environment, checks connectivity, and launches attack.py.
Features:
Auto-detects target IP/hostname.
Bypasses basic firewall rules (because why not).
Logs everything to /dev/null by default so no one sees what’s happening until it’s too late.
Optional verbose mode (-v) if you want to watch the world burn in real-time.
bash
Download
Copy
python3 Run.py --target 192.168.1.100
attack.py

The muscle. The executor. The "oops" moment.

Purpose: Executes the actual payload. Could be a DDoS, a data wipe, a ransomware encryptor, or a logic bomb. Depends on how you configured it last night.
Features:
Multi-threaded attack vector.
Self-deleting after execution (leaves no trace).
Can be chained: runs Run.py, then attack.py, then wipes its own logs.
Configurable intensity: gentle nudge or full-on server meltdown.
python
Download
Copy
import attack
attack.launch(mode='destructive', duration=300)
How to Use It (In Order)
Plug in the stick.
Open terminal.
Run:
bash
Download
Copy
python3 Run.py
Wait.
Smile.

If you want to get fancy:

bash
Download
Copy
python3 Run.py --stealth --no-log
Why Two Files?

Separation of concerns. Run.py handles the setup and decision-making. attack.py handles the violence. If you want to tweak the attack without touching the launcher, you edit attack.py. If you want to change how the stick connects, you edit Run.py. Clean. Simple. Effective.

Warnings
Test first. Running this on production without testing is like juggling chainsaws while blindfolded. You will drop one.
Backup your data. Or don’t. Maybe you want it gone.
Don’t share the code. Unless you want everyone else having fun with their own Kill Sticks.
License

Unlicense. Do whatever you want. Just don’t blame me when your server cries.

Contributing

Send PRs if you improve either file. But if you break attack.py, I’m using the Kill Stick on your laptop.
