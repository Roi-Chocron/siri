import google.generativeai as genai
import os
import json
import sys
from actions import extract_between_markers, run_action_from_text, extract_outside_markers

# Your API key here or use environment variable
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyDrjp9-inm2ayqSRe8dxBPq4JOwZz07q_w" # Please insert your key
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
HISTORY_FILE = "gemini_chat_history.json"

# Load existing history or create a new one
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

# Instruction for the language model
INSTRUCTION = (
    "אתה עוזר קולי. כאשר המשתמש מבקש פעולה במחשב, כתוב את הפקודה המתאימה בין הסימנים !@#$ ... !@#$. "
    "הפקודות האפשריות הן:\n"
    "play_song(\"artist_name\", \"song_name\", \"service\") - לדוגמה: play_song(\"עדן בן זקן\", \"מלכת השושנים\", \"Spotify\")\n"
    "stop_song()\n"
    "increase_volume()\n"
    "decrease_brightness()\n"
    "open_website(כתובת_אתר או שם אתר) - לדוג' open_website(\"https://www.google.com\")\n"
    "run_cmd(\"פקודה ב-CMD\") - לדוג' run_cmd(\"dir\") או run_cmd(\"echo hello\")\n"
    "\n"
    "אם המשתמש מבקש פעולה, כתוב תשובה מילולית למשתמש, ואחריה את הפקודה בין הסימנים !@#$ ... !@#$."
)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_message = sys.argv[1]
    else:
        user_message = "שלום, מה שלומך?"
        
    prompt = INSTRUCTION + "\n" + user_message
    history.append({"role": "user", "parts": [{"text": prompt}]})
    
    # Send the history to the model
    response = model.generate_content(history)
    
    # Add the model's response to history
    history.append({"role": "model", "parts": [{"text": response.text}]})
    
    # Save history
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    # Check if there is a command to execute
    command = extract_between_markers(response.text)
    if command:
        # If there is a command, run_action_from_text will handle ALL the printing.
        # It will print the assistant's message AND the action card HTML, separated by a delimiter.
        run_action_from_text(response.text)
    else:
        # If there's no command, just print the plain text response from the model.
        print(extract_outside_markers(response.text))


