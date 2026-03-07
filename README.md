# Prints Charming 📜🖨️

A thoughtful, automated project that generates a highly a personalized, romantic short poem using OpenAI and prints it on a thermal receipt printer. Originally designed to run every morning before a loved one leaves for work, it weaves in subtle daily life details, memories, and inside jokes for a uniquely personal touch.

## Features
- 🧠 **Structured Memory System**: Easily maintain a list of inside jokes, recent events, and favorite memories without touching any code.
- 🤖 **AI Poetry Generation**: Dynamically constructs a thoughtful prompt for OpenAI (`gpt-3.5-turbo`) tailored specifically for your partner.
- 🖨️ **Thermal Printer Integration**: Outputs directly to an attached serial thermal printer.
- 🛡️ **Robust Error Handling**: Handles API limits and printer connection issues gracefully without crashing the server.

## Hardware Requirements
- A Raspberry Pi (or similar Linux machine with serial capabilities)
- A Serial Thermal Receipt Printer (e.g., Adafruit Mini Thermal Printer)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/prints-charming.git
cd prints-charming
```

### 2. Configure Environment and Memory
This project uses `.env` for secrets and `memory.json` for personalization. **These files are intentionally ignored by git to protect your privacy.**

**Set up your API Key:**
```bash
cp .env.example .env
```
Edit `.env` and add your Moonshot API Key.

**Set up your Personal Memories:**
```bash
cp memory.example.json memory.json
```
Edit `memory.json` and fill it with your own personal details, inside jokes, and current moods. The more specific, the more magical the poems will be.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Make sure to use a virtual environment if preferred!)*

### 4. Hardware Setup
Ensure your thermal printer is connected. By default, the script looks for `/dev/serial0` running at `19200` baud. You may need to edit `prints_charming.py` if your permissions, port, or baud rate differ.

### 5. Running the Application
Start the Flask server:
```bash
python3 prints_charming.py
```

To trigger a print, send a POST request to the endpoint:
```bash
curl -X POST http://127.0.0.1:5000/print-poem
```

### 6. Automation (Cron Job)
To print every day at a specific time (e.g., 10:00 AM), add a cron job:
```bash
crontab -e
```
Add the following line:
```
0 10 * * * curl -X POST http://127.0.0.1:5000/print-poem
```

## Contributing
Feel free to submit pull requests or issues. Keep the magic alive!

## License
MIT License
