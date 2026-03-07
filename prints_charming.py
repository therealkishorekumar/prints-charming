from flask import Flask, request, jsonify
from openai import OpenAI
import serial
import time
import os
import json
import logging
from dotenv import load_dotenv

# Set up logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prints_charming.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")

# Initialize the thermal printer
try:
    printer = serial.Serial(
        port="/dev/serial0",   # Or "/dev/ttyAMA0" depending on your Pi
        baudrate=19200,        # Match your printer's baud rate
        timeout=1
    )
    time.sleep(2)  # Let printer initialize
    logger.info("✅ Printer initialized successfully.")
except Exception as e:
    logger.error(f"❌ Printer not available: {e}")
    printer = None

# Initialize Flask app
app = Flask(__name__)

def load_memories():
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load memory.json: {e}")
    return {}

def format_life_details(details_dict):
    """Convert the structured life details into a natural language string for the prompt."""
    if not isinstance(details_dict, dict):
        return ""
    
    parts = []
    for category, items in details_dict.items():
        if items and isinstance(items, list):
            # Filter out the placeholder text
            valid_items = [item for item in items if not item.startswith("Add ")]
            if valid_items:
                formatted_category = category.replace("_", " ")
                parts.append(f"{formatted_category}: {', '.join(valid_items)}")
    
    return "; ".join(parts) if parts else ""

# Generate a short poem using OpenAI with retry logic
def generate_poem(retries=3):
    memories = load_memories()
    details_dict = memories.get("life_details", {})
    details_str = format_life_details(details_dict)
    
    recipient = memories.get('recipient', 'wife')
    tone = memories.get('tone', 'personal and romantic')
    
    prompt = f"Write a short, beautiful 4-line poem for my {recipient}. "
    prompt += f"The tone should be {tone}. "
    if details_str:
        prompt += f"Subtly weave in or be inspired by these details from our life together: {details_str}. "
    prompt += "Keep it to exactly 4 lines, formatting it nicely."
    
    logger.info(f"Generating poem with prompt length: {len(prompt)}")
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are 'Prints Charming', a romantic poet who writes deeply personal and subtle daily poems for a beloved wife."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            poem = response.choices[0].message.content.strip()
            logger.info("✅ Poem generated successfully.")
            return poem
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                logger.error("❌ Failed to generate poem after all retries.")
                raise e

# Send the poem to the thermal printer
def print_poem(poem):
    if not printer:
        logger.warning("❌ Print requested, but printer is not available.")
        return False

    try:
        # Charming header
        printer.write(b"\n  -- Prints Charming --  \n")
        printer.write(b"  " + time.strftime("%A, %b %d").encode('utf-8') + b"  \n\n")
        
        for line in poem.split('\n'):
            printer.write(line.encode('utf-8') + b'\n')
        
        printer.write(b"\n      With love,      \n")
        printer.write(b"      Kishore         \n\n")
        printer.write(b"------------------------\n\n")
        printer.flush()
        logger.info("🖨️ Poem sent to printer successfully.")
        return True
    except Exception as e:
        logger.error(f"❌ Error communicating with printer: {e}")
        return False

# Flask endpoint to trigger the poem print
@app.route('/print-poem', methods=['POST'])
def handle_poem_request():
    logger.info("📡 Poem request received.")
    try:
        poem = generate_poem()
        logger.info(f"📜 Generated Poem:\n{poem}")
        print_success = print_poem(poem)
        
        return jsonify({
            "status": "success", 
            "poem": poem, 
            "printed": print_success
        })
    except Exception as e:
        logger.error(f"❌ Request failed: {e}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    logger.info("Starting Prints Charming server...")
    app.run(host='0.0.0.0', port=5000)
