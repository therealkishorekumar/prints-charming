# Prints Charming 📜🖨️

So, here's the deal: I wanted to do something romantic for my partner every morning before work, but I'm also a massive nerd. Naturally, my solution involved a serial thermal receipt printer and an AI model.

Prints Charming is a little Flask app that generates a highly personalized, 4-line love poem every day and spits it out on a thermal printer. It uses Moonshot AI (because why not?) and pulls from a local JSON file full of our inside jokes, recent events, and my general mood.

It's probably over-engineered for "saying good morning", but hey, it works! 

## Features (If you can call them that)
- 🧠 **"Memory" System**: A fancy way of saying there's a JSON file where I dump inside jokes and memories so I don't have to touch the Python code ever again.
- 🤖 **AI Poetry**: Uses Moonshot AI (`moonshot-v1-8k`) via the OpenAI Python SDK. Yes, the SDKs are compatible. 
- 🖨️ **Thermal Printer Integration**: Prints directly to a serial thermal printer (like those little Adafruit ones).
- 🛡️ **Error Handling**: It has retries! Because my network drops at the exact moment it's supposed to print.

## Hardware Stuff
- A machine to run it (I use a Raspberry Pi, but a Mac Mini or an old laptop works too).
- A Serial Thermal Receipt Printer.

## How to Set It Up (Assuming you want to steal this idea)

### 1. Clone it
```bash
git clone https://github.com/your-username/prints-charming.git
cd prints-charming
```

### 2. Secrets & Memories
I've ignored the real files in `.gitignore` so I don't accidentally leak my API keys or my terrible inside jokes to the internet. 

**API Key:**
```bash
cp .env.example .env
```
Throw your Moonshot API Key in there. (Or OpenAI, if you change the base URL back).

**Your Memories:**
```bash
cp memory.example.json memory.json
```
Fill this with your own stuff. The more embarrassingly specific, the better the output.

### 3. Dependencies
```bash
pip install -r requirements.txt
```
*(Use a virtual environment if you're a responsible person. I won't judge if you don't.)*

### 4. Hardware
Make sure your printer is plugged in. The code looks for `/dev/serial0` at `19200` baud. If you're on a Mac or use a USB adapter, you'll need to change that port in `prints_charming.py` (e.g., `/dev/tty.usbserial-...`).

### 5. Running It
Fire up the Flask server:
```bash
python3 prints_charming.py
```

Test it by throwing a POST request at it:
```bash
curl -X POST http://127.0.0.1:5000/print-poem
```

### 6. Scheduling (Making it Automatic)
Because remembering to run a script every morning defeats the entire purpose of automating romance.

**The Linux/Raspberry Pi Way (cron):**
Good ol' reliable cron. Run `crontab -e` and add:
```
0 10 * * * curl -X POST http://127.0.0.1:5000/print-poem
```

**The Mac Mini Way (launchd):**
If you're running this on a Mac, `cron` is basically dead and your Mac will probably be asleep anyway. You'll want to use `launchd` or the built-in Shortcuts app. But honestly? See the next option.

**The Overkill / Smart Home Way (Home Assistant):**
Since it's just a REST endpoint, the absolute best way to trigger this is via Home Assistant or Node-RED. 
Instead of a dumb timer, you can set an automation: *"Trigger the webhook `http://127.0.0.1:5000/print-poem` when motion is detected in the kitchen between 7 AM and 9 AM."*

## Contributing
If you find a way to make this even more unnecessarily complicated, my pull requests are open. 

## License
MIT. Do whatever you want with it, just don't blame me if it prints an essay instead of a haiku.
